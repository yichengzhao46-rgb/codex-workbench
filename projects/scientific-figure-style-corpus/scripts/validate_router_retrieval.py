#!/usr/bin/env python3
"""End-to-end retrieval validation for the Unified Scientific Figure Library."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from unified_library import load_index, query_records, validate_records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path("projects/scientific-figure-style-corpus"))
    ap.add_argument("--cases", type=Path, default=Path("projects/scientific-figure-style-corpus/validation/router-retrieval-test-cases.json"))
    ap.add_argument("--report", type=Path, default=Path("projects/scientific-figure-style-corpus/validation/router-retrieval-validation.json"))
    ap.add_argument("--top-k", type=int, default=8)
    args = ap.parse_args()

    project = args.project_root.resolve()
    rows = load_index(project)
    integrity = validate_records(project, rows, check_assets=True, strict_snapshot=True)
    cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]

    results = []
    failures = []
    for case in cases:
        hits = query_records(rows, text=case["text"])[: args.top_k]
        purposes = {r["primary_purpose"] for r in hits}
        styles = {r["style_family"] for r in hits}
        layouts = {r["layout"] for r in hits}
        active_hits = [r for r in hits if r["library_tier"] == "active"]
        reference_hits = [r for r in hits if r["library_tier"] == "reference"]
        purpose_ok = bool(purposes.intersection(case["expected_purposes"]))
        style_ok = bool(styles.intersection(case["expected_styles"]))
        layout_ok = bool(layouts.intersection(case["expected_layouts"]))
        enough_hits = len(hits) >= 3
        active_ok = len(active_hits) >= 1
        passed = purpose_ok and style_ok and layout_ok and enough_hits and active_ok
        item = {
            "id": case["id"],
            "request": case["request"],
            "query_text": case["text"],
            "passed": passed,
            "checks": {
                "purpose_match": purpose_ok,
                "style_match": style_ok,
                "layout_match": layout_ok,
                "at_least_3_hits": enough_hits,
                "at_least_1_active_hit": active_ok,
            },
            "hit_counts": {
                "total": len(hits),
                "active": len(active_hits),
                "reference": len(reference_hits),
            },
            "top_hits": [
                {
                    "record_id": r["record_id"],
                    "tier": r["library_tier"],
                    "journal": r["journal"],
                    "year": r["year"],
                    "article_title": r["article_title"],
                    "figure_id": r["figure_id"],
                    "primary_purpose": r["primary_purpose"],
                    "style_family": r["style_family"],
                    "layout": r["layout"],
                    "asset_path": r["asset_path"],
                    "classification_source": r["classification_source"],
                }
                for r in hits[:5]
            ],
        }
        results.append(item)
        if not passed:
            failures.append(case["id"])

    report = {
        "schema_version": 1,
        "library_integrity": integrity,
        "case_count": len(cases),
        "passed_cases": sum(1 for r in results if r["passed"]),
        "failed_cases": failures,
        "validation_passed": integrity["validation_passed"] and not failures,
        "cases": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["validation_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
