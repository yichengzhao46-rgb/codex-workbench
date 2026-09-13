#!/usr/bin/env python3
"""Build, validate, and query the Unified Scientific Figure Library."""
from __future__ import annotations

import argparse, csv, hashlib, json, re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath

PROJECT_DEFAULT = Path("projects/scientific-figure-style-corpus")
PURPOSES = {"conceptual_overview","microbial_interaction","mechanistic_pathway","metabolic_pathway","electron_transfer","material_microbe_interface","environmental_process","experimental_design","comparative_perturbation","integrated_mechanism","graphical_abstract","multiscale_zoom"}
STYLES = {"flat_2d_mechanism","soft_2_5d_schematic","pathway_cutaway_2d","editorial_2d_overview"}
LAYOUTS = {"linear_flow","two_organism_interaction","central_hub","mirrored_comparison","zoom_in_multiscale","circular_pathway","layered_gradient","evidence_to_model","other"}
DENSITIES = {"low","medium","high"}
FIELDS = ["record_id","canonical_record_id","duplicate_of","library_tier","source_manifest","source_record_id","source_type","journal","year","article_title","doi","article_url","figure_id","primary_purpose_raw","primary_purpose","style_family_raw","style_family","layout_raw","layout","information_density","classification_source","topics","asset_path","sha256","source_rights_status","rights_status","rights_override","redistribution_allowed","visual_qa_status","active_eligible","retrieval_enabled","notes"]


def read_csv(path: Path):
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))

def first(row,*keys):
    for key in keys:
        v=(row.get(key) or "").strip()
        if v: return v
    return ""

def truthy(v,default=False):
    if isinstance(v,bool): return v
    s=(v or "").strip().lower()
    if s in {"1","true","yes","y"}: return True
    if s in {"0","false","no","n"}: return False
    return default

def slug(v): return re.sub(r"[^a-z0-9]+","_",(v or "").strip().lower()).strip("_")
def base(): return {k:"" for k in FIELDS}

def canon_purpose(raw,caption="",topics=""):
    s=slug(raw)
    if s in PURPOSES: return s,"source_annotation"
    text=" ".join([s,slug(caption),slug(topics)])
    rules=[
        ("graphical_abstract",["graphical_abstract","toc_graphic"]),
        ("comparative_perturbation",["perturbation","comparison","before_after","low_o2","high_o2"]),
        ("electron_transfer",["electron_transfer","eet","diet","eeu","electrode","cytochrome","mtrcab","mtr_","nanowire"]),
        ("material_microbe_interface",["material_microbe","mineral","semiconductor","biohybrid","gac","graphite","biochar","interface"]),
        ("environmental_process",["environmental","redox_gradient","spatial_gradient","methane_seep","oxic","anoxic","sediment","depth_profile"]),
        ("microbial_interaction",["microbial_interaction","cross_feeding","coculture","co_culture","syntroph","two_organism"]),
        ("metabolic_pathway",["metabolic_pathway","metabolism","cbb","carbon_fixation","pathway_network"]),
        ("experimental_design",["experimental_design","workflow","study_design","experimental_system"]),
        ("integrated_mechanism",["integrated_mechanism","evidence_to_model","mechanism_summary"]),
        ("multiscale_zoom",["multiscale","zoom","cutaway"]),
        ("mechanistic_pathway",["mechanistic","mechanism","pathway"]),
        ("conceptual_overview",["conceptual","overview","architecture"]),
    ]
    for out,keys in rules:
        if any(k in text for k in keys): return out,"inferred_from_source_text"
    return "conceptual_overview","fallback_inference"

def canon_style(raw,purpose,caption=""):
    s=slug(raw); aliases={"flat_2d_mechanism":"flat_2d_mechanism","flat_2d_comparison":"flat_2d_mechanism","2d_pathway_cutaway":"pathway_cutaway_2d","pathway_cutaway_2d":"pathway_cutaway_2d","soft_2_5d_schematic":"soft_2_5d_schematic","editorial_2d_overview":"editorial_2d_overview","flat_2d_workflow":"editorial_2d_overview","gradient_profile_schematic":"editorial_2d_overview","2d_environmental_profile":"editorial_2d_overview","mixed_schematic_data":"flat_2d_mechanism","map_cartographic":"editorial_2d_overview"}
    if s in aliases: return aliases[s],"source_annotation" if aliases[s]==s else "canonical_alias"
    text=" ".join([s,slug(caption)])
    if any(k in text for k in ["membrane","cytochrome","mtr","respiratory_chain","cutaway"]): return "pathway_cutaway_2d","inferred_from_source_text"
    if purpose=="material_microbe_interface": return "soft_2_5d_schematic","purpose_default"
    if purpose in {"graphical_abstract","environmental_process","experimental_design","conceptual_overview"}: return "editorial_2d_overview","purpose_default"
    return "flat_2d_mechanism","purpose_default"

def canon_layout(raw,purpose,caption=""):
    s=slug(raw); aliases={"linear_flow":"linear_flow","two_organism_interaction":"two_organism_interaction","central_hub":"central_hub","mirrored_comparison":"mirrored_comparison","zoom_in_multiscale":"zoom_in_multiscale","multiscale_zoom":"zoom_in_multiscale","circular_pathway":"circular_pathway","layered_gradient":"layered_gradient","evidence_to_model":"evidence_to_model"}
    if s in aliases: return aliases[s],"source_annotation" if aliases[s]==s else "canonical_alias"
    text=" ".join([s,slug(caption)])
    if any(k in text for k in ["before_after","comparison","two_condition","low_o2","high_o2","three_state"]): return "mirrored_comparison","inferred_from_source_text"
    if any(k in text for k in ["depth","gradient","oxic","anoxic","sediment","stratification"]): return "layered_gradient","inferred_from_source_text"
    if any(k in text for k in ["zoom","multiscale","interface"]): return "zoom_in_multiscale","inferred_from_source_text"
    defaults={"microbial_interaction":"two_organism_interaction","comparative_perturbation":"mirrored_comparison","environmental_process":"layered_gradient","integrated_mechanism":"evidence_to_model","experimental_design":"linear_flow","material_microbe_interface":"zoom_in_multiscale"}
    return (defaults[purpose],"purpose_default") if purpose in defaults else ("other","fallback_inference")
def density(raw,purpose,caption):
    s=slug(raw)
    if s in DENSITIES: return s,"source_annotation"
    if purpose=="graphical_abstract": return "low","purpose_default"
    n=len((caption or "").split())
    if purpose in {"integrated_mechanism","metabolic_pathway"} or n>=180: return "high","inferred_from_caption"
    if purpose in {"electron_transfer","material_microbe_interface","environmental_process","comparative_perturbation"} or n>=70: return "medium","inferred_from_caption"
    return "low","inferred_from_caption"
def class_source(*vals):
    order=["source_annotation","canonical_alias","inferred_from_source_text","purpose_default","inferred_from_caption","fallback_inference"]
    vals=[v for v in vals if v]
    return max(vals,key=lambda x: order.index(x) if x in order else len(order)) if vals else "unspecified"

def baseline_rows(project):
    raw={first(r,"sample_id"):r for r in read_csv(project/"manifests/raw-image-manifest.csv")}; out=[]
    for c in read_csv(project/"annotations/figure-level-classification-v0.1.csv"):
        if first(c,"style_learning_tier") not in {"A_style_reference","B_style_reference"}: continue
        sid=first(c,"sample_id")
        if sid not in raw: raise SystemExit(f"Baseline active record missing from raw manifest: {sid}")
        out.append({**raw[sid],**{f"classification__{k}":v for k,v in c.items()}})
    return out

def norm_baseline(row):
    rid=first(row,"sample_id"); cap=first(row,"caption"); topics=first(row,"classification__domain_relevance_to_bath_rp"); pr=first(row,"classification__primary_purpose"); sr=first(row,"classification__style_family"); lr=first(row,"classification__layout")
    p,ps=canon_purpose(pr,cap,topics); s,ss=canon_style(sr,p,cap); l,ls=canon_layout(lr,p,cap); d,ds=density(first(row,"classification__information_density"),p,cap); rights=first(row,"rights_status","license")
    r=base(); r.update({"record_id":f"ACTIVE::{rid}::baseline","library_tier":"active","source_manifest":"manifests/raw-image-manifest.csv + annotations/figure-level-classification-v0.1.csv","source_record_id":rid,"source_type":"stage1_baseline_raw_corpus","journal":first(row,"journal"),"year":first(row,"year"),"article_title":first(row,"article_title"),"doi":first(row,"doi"),"article_url":first(row,"article_url"),"figure_id":first(row,"figure_id"),"primary_purpose_raw":pr,"primary_purpose":p,"style_family_raw":sr,"style_family":s,"layout_raw":lr,"layout":l,"information_density":d,"classification_source":class_source(ps,ss,ls,ds),"topics":topics,"asset_path":first(row,"asset_path"),"sha256":first(row,"sha256").lower(),"source_rights_status":rights,"rights_status":rights,"redistribution_allowed":"true","visual_qa_status":first(row,"inspection_status") or "classified","active_eligible":"true","retrieval_enabled":"true","notes":";".join(x for x in [first(row,"classification__style_learning_tier"),first(row,"classification__qa_caveats"),cap] if x)}); return r

def norm_active(row,source):
    rid=first(row,"sample_id","candidate_id","figure_id") or Path(first(row,"asset_path") or "unknown").stem; fig=first(row,"figure_number","figure_id"); cap=first(row,"caption"); topics=first(row,"topics","domain_relevance_to_bath_rp")
    if fig and not fig.lower().startswith("fig") and fig.isdigit(): fig=f"Figure {fig}"
    pr=first(row,"primary_purpose"); sr=first(row,"style_family"); lr=first(row,"layout_archetype","layout"); p,ps=canon_purpose(pr,cap,topics); s,ss=canon_style(sr,p,cap); l,ls=canon_layout(lr,p,cap); d,ds=density(first(row,"information_density"),p,cap); rights=first(row,"rights_status","license")
    r=base(); r.update({"record_id":f"ACTIVE::{rid}::{fig or 'figure'}","library_tier":"active","source_manifest":source.as_posix(),"source_record_id":rid,"source_type":first(row,"source_type") or "stage1_5_public_harvest","journal":first(row,"journal"),"year":first(row,"year"),"article_title":first(row,"article_title","title"),"doi":first(row,"doi"),"article_url":first(row,"article_url"),"figure_id":fig,"primary_purpose_raw":pr,"primary_purpose":p,"style_family_raw":sr,"style_family":s,"layout_raw":lr,"layout":l,"information_density":d,"classification_source":class_source(ps,ss,ls,ds),"topics":topics,"asset_path":first(row,"asset_path"),"sha256":first(row,"sha256").lower(),"source_rights_status":rights,"rights_status":rights,"redistribution_allowed":"true","visual_qa_status":first(row,"visual_qa","inspection_status") or "validated","active_eligible":"true","retrieval_enabled":"true","notes":first(row,"notes","caption")}); return r

def zotero_asset_map(project):
    root=project/"assets/zotero"; out={}
    if root.exists():
        for p in root.rglob("*.png"): out.setdefault(p.stem,p.relative_to(project).as_posix())
    return out

def manifest_zotero_path(raw,sid):
    parts=list(PureWindowsPath((raw or "").strip()).parts); low=[p.lower() for p in parts]
    if "zotero" in low:
        suf=parts[low.index("zotero")+1:]
        if suf: return Path("assets","zotero",*suf).as_posix()
    return f"assets/zotero/__unresolved__/{sid}.png"
def norm_zotero(row,source,asset_map,override):
    rid=first(row,"sample_id"); cap=first(row,"caption"); topics=first(row,"topics"); pr=first(row,"target_primary_purpose"); p,ps=canon_purpose(pr,cap,topics); s,ss=canon_style("",p,cap); l,ls=canon_layout("",p,cap); d,ds=density("",p,cap)
    src=first(row,"license_status") or "reference_only"; applies=bool(override.get("applies_to_all_rows")) and override.get("applies_to_manifest") in {source.name,source.as_posix()}; rights=override.get("effective_rights_status",src) if applies else src; redist=bool(override.get("redistribution_allowed")) if applies else truthy(first(row,"redistribution_allowed"),False)
    r=base(); r.update({"record_id":f"ZOTERO::{rid}","library_tier":"reference","source_manifest":source.as_posix(),"source_record_id":rid,"source_type":first(row,"source_type") or "zotero_pdf","journal":first(row,"journal"),"year":first(row,"year"),"article_title":first(row,"article_title"),"doi":first(row,"doi"),"figure_id":first(row,"figure_id"),"primary_purpose_raw":pr,"primary_purpose":p,"style_family":s,"layout":l,"information_density":d,"classification_source":class_source(ps,ss,ls,ds),"topics":topics,"asset_path":asset_map.get(rid,manifest_zotero_path(first(row,"asset_path"),rid)),"sha256":first(row,"sha256").lower(),"source_rights_status":src,"rights_status":rights,"rights_override":override.get("override_id","") if applies else "","redistribution_allowed":"true" if redist else "false","visual_qa_status":first(row,"visual_inspection_status") or "pending","active_eligible":"false","retrieval_enabled":"true","notes":first(row,"notes","caption")}); return r

def dedupe(rows):
    ordered=sorted(rows,key=lambda r:(0 if r["library_tier"]=="active" else 1,r["record_id"])); by_sha={}; by_path={}; n=0
    for r in ordered:
        c=by_sha.get(r["sha256"],"") if r["sha256"] else ""
        if not c and r["asset_path"]: c=by_path.get(r["asset_path"],"")
        if c: r["duplicate_of"]=c; r["canonical_record_id"]=c; n+=1
        else:
            r["canonical_record_id"]=r["record_id"]
            if r["sha256"]: by_sha[r["sha256"]]=r["record_id"]
            if r["asset_path"]: by_path[r["asset_path"]]=r["record_id"]
    return sorted(ordered,key=lambda r:(r["library_tier"],r["record_id"])),n

def load_override(project):
    p=project/"manifests/rights-overrides.json"; return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
def build_records(project):
    rows=[norm_baseline(r) for r in baseline_rows(project)]; manifests=sorted((project/"manifests").glob("stage1_5*_harvested_figures.csv"))
    for m in manifests: rows.extend(norm_active(r,m.relative_to(project)) for r in read_csv(m))
    zs=project/"manifests/zotero-private-manifest.csv"; zrows=read_csv(zs); amap=zotero_asset_map(project); ov=load_override(project); rows.extend(norm_zotero(r,zs.relative_to(project),amap,ov) for r in zrows); rows,dups=dedupe(rows)
    canon=[r for r in rows if not r["duplicate_of"]]; source_tiers=Counter(r["library_tier"] for r in rows); canon_tiers=Counter(r["library_tier"] for r in canon)
    summary={"schema_version":3,"library":"unified_scientific_figure_library","generated_at_utc":datetime.now(timezone.utc).isoformat(),"source_row_count":len(rows),"source_tier_counts":dict(source_tiers),"canonical_record_count_exact_dedup":len(canon),"canonical_tier_counts":dict(canon_tiers),"exact_duplicate_alias_rows":dups,"baseline_active_records":len(baseline_rows(project)),"stage1_5_source_manifests":[m.name for m in manifests],"zotero_source_rows":len(zrows),"purpose_counts":dict(Counter(r["primary_purpose"] for r in canon)),"style_counts":dict(Counter(r["style_family"] for r in canon)),"layout_counts":dict(Counter(r["layout"] for r in canon)),"density_counts":dict(Counter(r["information_density"] for r in canon)),"reference_visual_qa_status_counts":dict(Counter(r["visual_qa_status"] for r in canon if r["library_tier"]=="reference")),"cross_tier_perceptual_deduplication":"not_run","retrieval_surface":"unified"}
    return rows,summary

def materialize(project,index_output=None,summary_output=None):
    rows,summary=build_records(project); ip=index_output or project/"manifests/unified-library-index.csv"; sp=summary_output or project/"manifests/unified-library-summary.json"; ip.parent.mkdir(parents=True,exist_ok=True)
    with ip.open("w",encoding="utf-8",newline="") as f: w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    sp.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return summary

def load_index(project,index=None):
    p=index or project/"manifests/unified-library-index.csv"
    if not p.exists(): raise SystemExit(f"Unified index missing: {p}. Run build first.")
    rows=read_csv(p)
    if not rows: raise SystemExit(f"Unified index empty: {p}")
    return rows
def file_sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def expected_snapshot(project):
    p=project/"manifests/library-registry.json"
    if not p.exists(): return {}
    return json.loads(p.read_text(encoding="utf-8")).get("snapshot",{})
def validate_records(project,rows,check_assets=False,strict_snapshot=False):
    errors=[]; warnings=[]; canon=[r for r in rows if not r.get("duplicate_of")]
    for r in canon:
        if r.get("primary_purpose") not in PURPOSES: errors.append(f"invalid purpose {r.get('record_id')}: {r.get('primary_purpose')}")
        if r.get("style_family") not in STYLES: errors.append(f"invalid style {r.get('record_id')}: {r.get('style_family')}")
        if r.get("layout") not in LAYOUTS: errors.append(f"invalid layout {r.get('record_id')}: {r.get('layout')}")
        if r.get("information_density") not in DENSITIES: errors.append(f"invalid density {r.get('record_id')}: {r.get('information_density')}")
        if not r.get("asset_path") or not r.get("sha256"): errors.append(f"missing asset metadata: {r.get('record_id')}"); continue
        if check_assets:
            p=project/r["asset_path"]
            if not p.exists(): errors.append(f"missing asset: {r.get('record_id')} -> {r['asset_path']}")
            elif file_sha(p)!=r["sha256"]: errors.append(f"checksum mismatch: {r.get('record_id')} -> {r['asset_path']}")
    actual={"source_rows":len(rows),"active_source_records":sum(r["library_tier"]=="active" for r in rows),"reference_source_records":sum(r["library_tier"]=="reference" for r in rows),"canonical_records":len(canon),"active_canonical_records":sum(r["library_tier"]=="active" for r in canon),"reference_canonical_records":sum(r["library_tier"]=="reference" for r in canon),"exact_duplicate_alias_rows":len(rows)-len(canon)}
    exp=expected_snapshot(project)
    if exp:
        mismatches={k:{"expected":v,"actual":actual.get(k)} for k,v in exp.items() if k in actual and actual.get(k)!=v}
        if mismatches: (errors if strict_snapshot else warnings).append(f"snapshot mismatch: {mismatches}")
    return {"validation_passed":not errors,**actual,"check_assets":check_assets,"strict_snapshot":strict_snapshot,"errors":errors,"warnings":warnings}
def tokenize(text): return [x for x in re.split(r"[^a-z0-9_+.-]+",text.lower()) if x]
def query_records(rows,text="",purpose="",layout="",style_family="",density_value="",topic="",tier="",public_reuse_only=False,qa_complete_only=False):
    terms=tokenize(text); ranked=[]
    for r in rows:
        if r.get("duplicate_of") or not truthy(r.get("retrieval_enabled"),True): continue
        if tier and r["library_tier"]!=tier: continue
        if public_reuse_only and not truthy(r.get("redistribution_allowed")): continue
        if qa_complete_only and r.get("visual_qa_status","").lower() not in {"complete","validated","direct_visual_qa_then_aws_scan_source_media_harvested","classified"}: continue
        if purpose and r["primary_purpose"]!=purpose: continue
        if layout and r["layout"]!=layout: continue
        if style_family and r["style_family"]!=style_family: continue
        if density_value and r["information_density"]!=density_value: continue
        if topic and topic.lower() not in (r.get("topics") or "").lower(): continue
        hay=" ".join(r.get(k,"") for k in ["journal","article_title","primary_purpose_raw","primary_purpose","style_family_raw","style_family","layout_raw","layout","information_density","topics","notes"]).lower(); lexical=sum(t in hay for t in terms)
        if terms and lexical==0: continue
        score=float(lexical)+(0.25 if r["library_tier"]=="active" else 0)+(0.1 if r.get("visual_qa_status","").lower() in {"complete","validated","direct_visual_qa_then_aws_scan_source_media_harvested","classified"} else 0); ranked.append((score,r))
    ranked.sort(key=lambda x:(-x[0],x[1]["record_id"])); return [r for _,r in ranked]
def args_parser():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",type=Path,default=PROJECT_DEFAULT); sub=ap.add_subparsers(dest="command")
    b=sub.add_parser("build"); b.add_argument("--index-output",type=Path); b.add_argument("--summary-output",type=Path)
    v=sub.add_parser("validate"); v.add_argument("--index",type=Path); v.add_argument("--check-assets",action="store_true"); v.add_argument("--strict-snapshot",action="store_true"); v.add_argument("--report",type=Path)
    q=sub.add_parser("query"); q.add_argument("--index",type=Path); q.add_argument("--text",default=""); q.add_argument("--purpose",choices=sorted(PURPOSES),default=""); q.add_argument("--layout",choices=sorted(LAYOUTS),default=""); q.add_argument("--style-family",choices=sorted(STYLES),default=""); q.add_argument("--density",choices=sorted(DENSITIES),default=""); q.add_argument("--topic",default=""); q.add_argument("--tier",choices=["active","reference"],default=""); q.add_argument("--public-reuse-only",action="store_true"); q.add_argument("--qa-complete-only",action="store_true"); q.add_argument("--limit",type=int,default=20); return ap

def main():
    a=args_parser().parse_args(); cmd=a.command or "build"; project=a.project_root.resolve()
    if cmd=="build": print(json.dumps(materialize(project,getattr(a,"index_output",None),getattr(a,"summary_output",None)),ensure_ascii=False,indent=2)); return 0
    if cmd=="validate":
        result=validate_records(project,load_index(project,getattr(a,"index",None)),a.check_assets,a.strict_snapshot)
        if a.report: a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result["validation_passed"] else 2
    hits=query_records(load_index(project,getattr(a,"index",None)),text=a.text,purpose=a.purpose,layout=a.layout,style_family=a.style_family,density_value=a.density,topic=a.topic,tier=a.tier,public_reuse_only=a.public_reuse_only,qa_complete_only=a.qa_complete_only)[:a.limit]; print(json.dumps(hits,ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
