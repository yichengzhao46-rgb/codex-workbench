#!/usr/bin/env python3
"""Build, validate, and query the Unified Scientific Figure Library.

One logical retrieval surface combines:
- active: validated baseline + Stage 1.5 A/B assets
- reference: Codex/Zotero assets retained with provenance/QA/rights metadata

Operations are separated intentionally:
  build     materialize manifests/unified-library-index.csv + summary
  validate  read the materialized index and verify schema/assets/snapshot
  query     read the materialized index only; never mutates the repository
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath

PROJECT_DEFAULT = Path("projects/scientific-figure-style-corpus")

PURPOSES = {
    "conceptual_overview", "microbial_interaction", "mechanistic_pathway",
    "metabolic_pathway", "electron_transfer", "material_microbe_interface",
    "environmental_process", "experimental_design", "comparative_perturbation",
    "integrated_mechanism", "graphical_abstract", "multiscale_zoom",
}
STYLES = {"flat_2d_mechanism", "soft_2_5d_schematic", "pathway_cutaway_2d", "editorial_2d_overview"}
LAYOUTS = {"linear_flow", "two_organism_interaction", "central_hub", "mirrored_comparison", "zoom_in_multiscale", "circular_pathway", "layered_gradient", "evidence_to_model", "other"}
DENSITIES = {"low", "medium", "high"}

UNIFIED_FIELDS = [
    "record_id", "canonical_record_id", "duplicate_of", "library_tier",
    "source_manifest", "source_record_id", "source_type", "journal", "year",
    "article_title", "doi", "article_url", "figure_id",
    "primary_purpose_raw", "primary_purpose", "style_family_raw", "style_family",
    "layout_raw", "layout", "information_density", "classification_source",
    "topics", "asset_path", "sha256", "source_rights_status", "rights_status",
    "rights_override", "redistribution_allowed", "visual_qa_status",
    "active_eligible", "retrieval_enabled", "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=UNIFIED_FIELDS)
        w.writeheader()
        w.writerows(rows)


def first(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def truthy(value: str | bool, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    v = (value or "").strip().lower()
    if v in {"1", "true", "yes", "y"}: return True
    if v in {"0", "false", "no", "n"}: return False
    return default


def bool_text(value: str | bool, default: bool = False) -> str:
    return "true" if truthy(value, default=default) else "false"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower()).strip("_")


def normalize_zotero_asset_path(raw: str, sample_id: str) -> str:
    raw = (raw or "").strip()
    if raw:
        parts = list(PureWindowsPath(raw).parts)
        lower = [p.lower() for p in parts]
        if "zotero" in lower:
            idx = lower.index("zotero")
            suffix = parts[idx + 1:]
            if suffix:
                return Path("assets", "zotero", *suffix).as_posix()
    return f"assets/zotero/__unresolved__/{sample_id}.png"


def canonical_purpose(raw: str, caption: str = "", topics: str = "") -> tuple[str, str]:
    s = slug(raw)
    if s in PURPOSES: return s, "source_annotation"
    text = " ".join([s, slug(caption), slug(topics)])
    rules = [
        ("graphical_abstract", ["graphical_abstract", "toc_graphic"]),
        ("comparative_perturbation", ["perturbation", "comparison", "before_after", "low_o2", "high_o2"]),
        ("electron_transfer", ["electron_transfer", "eet", "diet", "eeu", "electrode", "cytochrome", "mtrcab", "mtr_", "nanowire"]),
        ("material_microbe_interface", ["material_microbe", "mineral", "semiconductor", "biohybrid", "gac", "graphite", "biochar", "interface"]),
        ("environmental_process", ["environmental", "redox_gradient", "spatial_gradient", "methane_seep", "oxic", "anoxic", "sediment", "depth_profile"]),
        ("microbial_interaction", ["microbial_interaction", "cross_feeding", "coculture", "co_culture", "syntroph", "two_organism"]),
        ("metabolic_pathway", ["metabolic_pathway", "metabolism", "cbb", "carbon_fixation", "pathway_network"]),
        ("experimental_design", ["experimental_design", "workflow", "study_design", "experimental_system"]),
        ("integrated_mechanism", ["integrated_mechanism", "evidence_to_model", "mechanism_summary"]),
        ("multiscale_zoom", ["multiscale", "zoom", "cutaway"]),
        ("mechanistic_pathway", ["mechanistic", "mechanism", "pathway"]),
        ("conceptual_overview", ["conceptual", "overview", "architecture"]),
    ]
    for purpose, keys in rules:
        if any(k in text for k in keys): return purpose, "inferred_from_source_text"
    return "conceptual_overview", "fallback_inference"


def canonical_style(raw: str, purpose: str, caption: str = "") -> tuple[str, str]:
    s = slug(raw)
    aliases = {
        "flat_2d_mechanism": "flat_2d_mechanism", "flat_2d_comparison": "flat_2d_mechanism",
        "2d_pathway_cutaway": "pathway_cutaway_2d", "pathway_cutaway_2d": "pathway_cutaway_2d",
        "soft_2_5d_schematic": "soft_2_5d_schematic", "editorial_2d_overview": "editorial_2d_overview",
        "flat_2d_workflow": "editorial_2d_overview", "gradient_profile_schematic": "editorial_2d_overview",
        "2d_environmental_profile": "editorial_2d_overview", "mixed_schematic_data": "flat_2d_mechanism",
        "map_cartographic": "editorial_2d_overview",
    }
    if s in aliases: return aliases[s], "source_annotation" if aliases[s] == s else "canonical_alias"
    text = " ".join([s, slug(caption)])
    if any(k in text for k in ["membrane", "cytochrome", "mtr", "respiratory_chain", "cutaway"]):
        return "pathway_cutaway_2d", "inferred_from_source_text"
    if purpose == "material_microbe_interface": return "soft_2_5d_schematic", "purpose_default"
    if purpose in {"graphical_abstract", "environmental_process", "experimental_design", "conceptual_overview"}:
        return "editorial_2d_overview", "purpose_default"
    return "flat_2d_mechanism", "purpose_default"


def canonical_layout(raw: str, purpose: str, caption: str = "") -> tuple[str, str]:
    s = slug(raw)
    aliases = {
        "linear_flow":"linear_flow", "two_organism_interaction":"two_organism_interaction",
        "central_hub":"central_hub", "mirrored_comparison":"mirrored_comparison",
        "zoom_in_multiscale":"zoom_in_multiscale", "multiscale_zoom":"zoom_in_multiscale",
        "circular_pathway":"circular_pathway", "layered_gradient":"layered_gradient",
        "evidence_to_model":"evidence_to_model",
    }
    if s in aliases: return aliases[s], "source_annotation" if aliases[s] == s else "canonical_alias"
    text = " ".join([s, slug(caption)])
    if any(k in text for k in ["before_after", "comparison", "two_condition", "low_o2", "high_o2", "three_state"]):
        return "mirrored_comparison", "inferred_from_source_text"
    if any(k in text for k in ["depth", "gradient", "oxic", "anoxic", "sediment", "stratification"]):
        return "layered_gradient", "inferred_from_source_text"
    if any(k in text for k in ["zoom", "multiscale", "interface"]): return "zoom_in_multiscale", "inferred_from_source_text"
    defaults = {
        "microbial_interaction":"two_organism_interaction", "comparative_perturbation":"mirrored_comparison",
        "environmental_process":"layered_gradient", "integrated_mechanism":"evidence_to_model",
        "experimental_design":"linear_flow", "material_microbe_interface":"zoom_in_multiscale",
    }
    if purpose in defaults: return defaults[purpose], "purpose_default"
    return "other", "fallback_inference"


def infer_density(explicit: str, purpose: str, caption: str) -> tuple[str, str]:
    s = slug(explicit)
    if s in DENSITIES: return s, "source_annotation"
    if purpose == "graphical_abstract": return "low", "purpose_default"
    n = len((caption or "").split())
    if purpose in {"integrated_mechanism", "metabolic_pathway"} or n >= 180: return "high", "inferred_from_caption"
    if purpose in {"electron_transfer", "material_microbe_interface", "environmental_process", "comparative_perturbation"} or n >= 70:
        return "medium", "inferred_from_caption"
    return "low", "inferred_from_caption"


def merge_classification_sources(*sources: str) -> str:
    priority = ["source_annotation", "canonical_alias", "inferred_from_source_text", "purpose_default", "inferred_from_caption", "fallback_inference"]
    vals = [s for s in sources if s]
    if not vals: return "unspecified"
    return max(vals, key=lambda x: priority.index(x) if x in priority else len(priority))


def load_rights_override(project: Path) -> dict:
    p = project / "manifests" / "rights-overrides.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def active_manifest_paths(project: Path) -> list[Path]:
    return sorted((project / "manifests").glob("stage1_5*_harvested_figures.csv"))


def baseline_active_rows(project: Path) -> list[dict[str, str]]:
    raw = {first(r, "sample_id"): r for r in read_csv(project / "manifests" / "raw-image-manifest.csv")}
    out = []
    for c in read_csv(project / "annotations" / "figure-level-classification-v0.1.csv"):
        if first(c, "style_learning_tier") not in {"A_style_reference", "B_style_reference"}: continue
        sid = first(c, "sample_id")
        r = raw.get(sid)
        if not r: raise SystemExit(f"Baseline active record missing from raw manifest: {sid}")
        out.append({**r, **{f"classification__{k}": v for k, v in c.items()}})
    return out


def base_record() -> dict[str, str]:
    return {k: "" for k in UNIFIED_FIELDS}


def normalize_baseline(row: dict[str, str]) -> dict[str, str]:
    rid = first(row, "sample_id"); caption = first(row, "caption"); topics = first(row, "classification__domain_relevance_to_bath_rp")
    pr = first(row, "classification__primary_purpose"); sr = first(row, "classification__style_family"); lr = first(row, "classification__layout")
    purpose, ps = canonical_purpose(pr, caption, topics); style, ss = canonical_style(sr, purpose, caption); layout, ls = canonical_layout(lr, purpose, caption)
    density, ds = infer_density(first(row, "classification__information_density"), purpose, caption)
    r = base_record(); rights = first(row, "rights_status", "license")
    r.update({
        "record_id":f"ACTIVE::{rid}::baseline", "library_tier":"active",
        "source_manifest":"manifests/raw-image-manifest.csv + annotations/figure-level-classification-v0.1.csv",
        "source_record_id":rid, "source_type":"stage1_baseline_raw_corpus", "journal":first(row,"journal"), "year":first(row,"year"),
        "article_title":first(row,"article_title"), "doi":first(row,"doi"), "article_url":first(row,"article_url"), "figure_id":first(row,"figure_id"),
        "primary_purpose_raw":pr, "primary_purpose":purpose, "style_family_raw":sr, "style_family":style, "layout_raw":lr, "layout":layout,
        "information_density":density, "classification_source":merge_classification_sources(ps,ss,ls,ds), "topics":topics,
        "asset_path":first(row,"asset_path"), "sha256":first(row,"sha256").lower(), "source_rights_status":rights, "rights_status":rights,
        "redistribution_allowed":"true", "visual_qa_status":first(row,"inspection_status") or "classified", "active_eligible":"true", "retrieval_enabled":"true",
        "notes":";".join(x for x in [first(row,"classification__style_learning_tier"), first(row,"classification__qa_caveats"), caption] if x),
    }); return r


def normalize_active(row: dict[str, str], source: Path) -> dict[str, str]:
    rid = first(row,"sample_id","candidate_id","figure_id") or Path(first(row,"asset_path") or "unknown").stem
    figure = first(row,"figure_number","figure_id"); caption = first(row,"caption"); topics = first(row,"topics","domain_relevance_to_bath_rp")
    if figure and not figure.lower().startswith("fig") and figure.isdigit(): figure = f"Figure {figure}"
    pr = first(row,"primary_purpose"); sr = first(row,"style_family"); lr = first(row,"layout_archetype","layout")
    purpose, ps = canonical_purpose(pr,caption,topics); style, ss = canonical_style(sr,purpose,caption); layout, ls = canonical_layout(lr,purpose,caption)
    density, ds = infer_density(first(row,"information_density"),purpose,caption); rights = first(row,"rights_status","license")
    r = base_record(); r.update({
        "record_id":f"ACTIVE::{rid}::{figure or 'figure'}", "library_tier":"active", "source_manifest":source.as_posix(), "source_record_id":rid,
        "source_type":first(row,"source_type") or "stage1_5_public_harvest", "journal":first(row,"journal"), "year":first(row,"year"),
        "article_title":first(row,"article_title","title"), "doi":first(row,"doi"), "article_url":first(row,"article_url"), "figure_id":figure,
        "primary_purpose_raw":pr, "primary_purpose":purpose, "style_family_raw":sr, "style_family":style, "layout_raw":lr, "layout":layout,
        "information_density":density, "classification_source":merge_classification_sources(ps,ss,ls,ds), "topics":topics,
        "asset_path":first(row,"asset_path"), "sha256":first(row,"sha256").lower(), "source_rights_status":rights, "rights_status":rights,
        "redistribution_allowed":"true", "visual_qa_status":first(row,"visual_qa","inspection_status") or "validated", "active_eligible":"true", "retrieval_enabled":"true",
        "notes":first(row,"notes","caption"),
    }); return r


def normalize_zotero(row: dict[str, str], source: Path, override: dict) -> dict[str, str]:
    rid = first(row,"sample_id"); caption = first(row,"caption"); topics = first(row,"topics"); pr = first(row,"target_primary_purpose")
    purpose, ps = canonical_purpose(pr,caption,topics); style, ss = canonical_style("",purpose,caption); layout, ls = canonical_layout("",purpose,caption)
    density, ds = infer_density("",purpose,caption); src_rights = first(row,"license_status") or "reference_only"
    applies = bool(override.get("applies_to_all_rows")) and override.get("applies_to_manifest") in {source.name, source.as_posix()}
    rights = override.get("effective_rights_status","") if applies else src_rights
    redist = bool(override.get("redistribution_allowed")) if applies else truthy(first(row,"redistribution_allowed"),False)
    r = base_record(); r.update({
        "record_id":f"ZOTERO::{rid}", "library_tier":"reference", "source_manifest":source.as_posix(), "source_record_id":rid,
        "source_type":first(row,"source_type") or "zotero_pdf", "journal":first(row,"journal"), "year":first(row,"year"),
        "article_title":first(row,"article_title"), "doi":first(row,"doi"), "figure_id":first(row,"figure_id"),
        "primary_purpose_raw":pr, "primary_purpose":purpose, "style_family":style, "layout":layout, "information_density":density,
        "classification_source":merge_classification_sources(ps,ss,ls,ds), "topics":topics,
        "asset_path":normalize_zotero_asset_path(first(row,"asset_path"),rid), "sha256":first(row,"sha256").lower(),
        "source_rights_status":src_rights, "rights_status":rights, "rights_override":override.get("override_id","") if applies else "",
        "redistribution_allowed":bool_text(redist), "visual_qa_status":first(row,"visual_inspection_status") or "pending",
        "active_eligible":"false", "retrieval_enabled":"true", "notes":first(row,"notes","caption"),
    }); return r


def dedupe(records: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    ordered = sorted(records,key=lambda r:(0 if r["library_tier"]=="active" else 1,r["record_id"])); by_sha={}; by_asset={}; dup=0
    for row in ordered:
        canonical = by_sha.get(row["sha256"],"") if row["sha256"] else ""
        if not canonical and row["asset_path"]: canonical = by_asset.get(row["asset_path"],"")
        if canonical:
            row["duplicate_of"] = canonical; row["canonical_record_id"] = canonical; dup += 1
        else:
            row["canonical_record_id"] = row["record_id"]
            if row["sha256"]: by_sha[row["sha256"]] = row["record_id"]
            if row["asset_path"]: by_asset[row["asset_path"]] = row["record_id"]
    return sorted(ordered,key=lambda r:(r["library_tier"],r["record_id"])),dup


def build_records(project: Path) -> tuple[list[dict[str, str]], dict]:
    records=[]; baseline=baseline_active_rows(project); records.extend(normalize_baseline(r) for r in baseline)
    sources=active_manifest_paths(project)
    for source in sources: records.extend(normalize_active(r,source.relative_to(project)) for r in read_csv(source))
    zs=project/"manifests"/"zotero-private-manifest.csv"; zrows=read_csv(zs); override=load_rights_override(project)
    records.extend(normalize_zotero(r,zs.relative_to(project),override) for r in zrows); records,dup=dedupe(records)
    canonical=[r for r in records if not r["duplicate_of"]]; active=[r for r in canonical if r["library_tier"]=="active"]; ref=[r for r in canonical if r["library_tier"]=="reference"]
    summary={
        "schema_version":2,"library":"unified_scientific_figure_library","generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "source_row_count":len(records),"canonical_record_count_exact_dedup":len(canonical),"exact_duplicate_alias_rows":dup,
        "active_canonical_records":len(active),"reference_canonical_records":len(ref),"baseline_active_records":len(baseline),
        "stage1_5_source_manifests":[p.name for p in sources],"zotero_source_rows":len(zrows),
        "tier_counts":dict(Counter(r["library_tier"] for r in canonical)),"purpose_counts":dict(Counter(r["primary_purpose"] for r in canonical)),
        "style_counts":dict(Counter(r["style_family"] for r in canonical)),"layout_counts":dict(Counter(r["layout"] for r in canonical)),
        "density_counts":dict(Counter(r["information_density"] for r in canonical)),"classification_source_counts":dict(Counter(r["classification_source"] for r in canonical)),
        "reference_visual_qa_status_counts":dict(Counter(r["visual_qa_status"] or "unspecified" for r in ref)),
        "redistribution_allowed_counts":dict(Counter(r["redistribution_allowed"] for r in canonical)),"cross_tier_perceptual_deduplication":"not_run","retrieval_surface":"unified",
    }; return records,summary


def materialize(project: Path,index_output: Path|None=None,summary_output: Path|None=None)->dict:
    rows,summary=build_records(project); ip=index_output or project/"manifests"/"unified-library-index.csv"; sp=summary_output or project/"manifests"/"unified-library-summary.json"
    write_csv(ip,rows); sp.parent.mkdir(parents=True,exist_ok=True); sp.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return summary


def load_index(project: Path,index_path: Path|None=None)->list[dict[str,str]]:
    p=index_path or project/"manifests"/"unified-library-index.csv"
    if not p.exists(): raise SystemExit(f"Unified index is missing: {p}. Run `unified_library.py build` first.")
    rows=read_csv(p)
    if not rows: raise SystemExit(f"Unified index is empty: {p}")
    return rows


def sha256_file(path: Path)->str:
    h=hashlib.sha256();
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()


def validate_records(project:Path,rows:list[dict[str,str]],check_assets:bool,strict_snapshot:bool)->dict:
    errors=[]; warnings=[]; canonical=[r for r in rows if not r.get("duplicate_of")]
    for r in canonical:
        if r.get("primary_purpose") not in PURPOSES: errors.append(f"invalid purpose {r.get('record_id')}: {r.get('primary_purpose')}")
        if r.get("style_family") not in STYLES: errors.append(f"invalid style {r.get('record_id')}: {r.get('style_family')}")
        if r.get("layout") not in LAYOUTS: errors.append(f"invalid layout {r.get('record_id')}: {r.get('layout')}")
        if r.get("information_density") not in DENSITIES: errors.append(f"invalid density {r.get('record_id')}: {r.get('information_density')}")
        if not r.get("asset_path"): errors.append(f"missing asset_path: {r.get('record_id')}")
        if not r.get("sha256"): errors.append(f"missing sha256: {r.get('record_id')}")
        if check_assets and r.get("asset_path"):
            p=project/r["asset_path"]
            if not p.exists(): errors.append(f"missing asset: {r.get('record_id')} -> {r['asset_path']}")
            elif r.get("sha256") and sha256_file(p)!=r["sha256"]: errors.append(f"checksum mismatch: {r.get('record_id')} -> {r['asset_path']}")
    actual={"source_rows":len(rows),"active":sum(1 for r in canonical if r.get("library_tier")=="active"),"reference":sum(1 for r in canonical if r.get("library_tier")=="reference")}
    snap={"source_rows":235,"active":96,"reference":139}
    if actual!=snap: (errors if strict_snapshot else warnings).append(f"current snapshot changed: expected {snap}, actual {actual}")
    return {"validation_passed":not errors,"canonical_records":len(canonical),"source_rows":len(rows),"active_canonical_records":actual["active"],"reference_canonical_records":actual["reference"],"exact_duplicate_alias_rows":len(rows)-len(canonical),"check_assets":check_assets,"strict_snapshot":strict_snapshot,"errors":errors,"warnings":warnings}


def tokenize(text:str)->list[str]: return [t for t in re.split(r"[^a-z0-9_+.-]+",text.lower()) if t]


def query_records(rows:list[dict[str,str]],text:str="",purpose:str="",layout:str="",style_family:str="",density:str="",topic:str="",tier:str="",public_reuse_only:bool=False,qa_complete_only:bool=False)->list[dict[str,str]]:
    terms=tokenize(text); ranked=[]
    for row in rows:
        if row.get("duplicate_of") or not truthy(row.get("retrieval_enabled"),True): continue
        if tier and row.get("library_tier")!=tier: continue
        if public_reuse_only and not truthy(row.get("redistribution_allowed")): continue
        if qa_complete_only and row.get("visual_qa_status","").lower() not in {"complete","validated","direct_visual_qa_then_aws_scan_source_media_harvested","classified"}: continue
        if purpose and row.get("primary_purpose")!=purpose: continue
        if layout and row.get("layout")!=layout: continue
        if style_family and row.get("style_family")!=style_family: continue
        if density and row.get("information_density")!=density: continue
        if topic and topic.lower() not in (row.get("topics") or "").lower(): continue
        hay=" ".join(row.get(k,"") for k in ("journal","article_title","primary_purpose_raw","primary_purpose","style_family_raw","style_family","layout_raw","layout","information_density","topics","notes")).lower()
        lexical=sum(1 for term in terms if term in hay); structured=sum([3 if purpose else 0,2 if layout else 0,2 if style_family else 0,1 if density else 0,2 if topic else 0])
        if terms and lexical==0 and structured==0: continue
        score=float(lexical+structured)+(0.25 if row.get("library_tier")=="active" else 0)+(0.10 if row.get("visual_qa_status","").lower() in {"complete","validated","direct_visual_qa_then_aws_scan_source_media_harvested","classified"} else 0)
        ranked.append((score,row))
    ranked.sort(key=lambda x:(-x[0],x[1].get("record_id",""))); return [r for _,r in ranked]


def parse_args()->argparse.Namespace:
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",type=Path,default=PROJECT_DEFAULT); sub=ap.add_subparsers(dest="command")
    b=sub.add_parser("build"); b.add_argument("--index-output",type=Path); b.add_argument("--summary-output",type=Path)
    v=sub.add_parser("validate"); v.add_argument("--index",type=Path); v.add_argument("--check-assets",action="store_true"); v.add_argument("--strict-snapshot",action="store_true"); v.add_argument("--report",type=Path)
    q=sub.add_parser("query"); q.add_argument("--index",type=Path); q.add_argument("--text",default=""); q.add_argument("--purpose",choices=sorted(PURPOSES),default=""); q.add_argument("--layout",choices=sorted(LAYOUTS),default=""); q.add_argument("--style-family",choices=sorted(STYLES),default=""); q.add_argument("--density",choices=sorted(DENSITIES),default=""); q.add_argument("--topic",default=""); q.add_argument("--tier",choices=["active","reference"],default=""); q.add_argument("--public-reuse-only",action="store_true"); q.add_argument("--qa-complete-only",action="store_true"); q.add_argument("--limit",type=int,default=20)
    return ap.parse_args()


def main()->int:
    args=parse_args(); cmd=args.command or "build"; project=args.project_root.resolve()
    if cmd=="build": print(json.dumps(materialize(project,getattr(args,"index_output",None),getattr(args,"summary_output",None)),ensure_ascii=False,indent=2)); return 0
    if cmd=="validate":
        result=validate_records(project,load_index(project,getattr(args,"index",None)),args.check_assets,args.strict_snapshot)
        if args.report: args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result["validation_passed"] else 2
    if cmd=="query":
        hits=query_records(load_index(project,getattr(args,"index",None)),text=args.text,purpose=args.purpose,layout=args.layout,style_family=args.style_family,density=args.density,topic=args.topic,tier=args.tier,public_reuse_only=args.public_reuse_only,qa_complete_only=args.qa_complete_only)[:args.limit]
        print(json.dumps(hits,ensure_ascii=False,indent=2)); return 0
    raise SystemExit(f"Unknown command: {cmd}")

if __name__=="__main__": raise SystemExit(main())
