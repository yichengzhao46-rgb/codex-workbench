#!/usr/bin/env python3
"""Stable Style Router adapter for the Unified Scientific Figure Library."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from unified_library import DENSITIES, LAYOUTS, PURPOSES, STYLES, load_index, query_records

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",type=Path,default=Path("projects/scientific-figure-style-corpus")); ap.add_argument("--text",default=""); ap.add_argument("--purpose",choices=sorted(PURPOSES),default=""); ap.add_argument("--layout",choices=sorted(LAYOUTS),default=""); ap.add_argument("--style-family",choices=sorted(STYLES),default=""); ap.add_argument("--density",choices=sorted(DENSITIES),default=""); ap.add_argument("--topic",default=""); ap.add_argument("--tier",choices=["active","reference"],default=""); ap.add_argument("--public-reuse-only",action="store_true"); ap.add_argument("--qa-complete-only",action="store_true"); ap.add_argument("--limit",type=int,default=8); a=ap.parse_args()
    project=a.project_root.resolve(); rows=load_index(project); hits=query_records(rows,text=a.text,purpose=a.purpose,layout=a.layout,style_family=a.style_family,density_value=a.density,topic=a.topic,tier=a.tier,public_reuse_only=a.public_reuse_only,qa_complete_only=a.qa_complete_only)[:a.limit]
    payload={"schema_version":1,"library":"unified_scientific_figure_library","query":{"text":a.text,"purpose":a.purpose,"layout":a.layout,"style_family":a.style_family,"density":a.density,"topic":a.topic,"tier":a.tier,"public_reuse_only":a.public_reuse_only,"qa_complete_only":a.qa_complete_only},"result_count":len(hits),"results":[{"record_id":r["record_id"],"tier":r["library_tier"],"journal":r["journal"],"year":r["year"],"article_title":r["article_title"],"figure_id":r["figure_id"],"primary_purpose":r["primary_purpose"],"style_family":r["style_family"],"layout":r["layout"],"information_density":r["information_density"],"topics":r["topics"],"asset_path":r["asset_path"],"visual_qa_status":r["visual_qa_status"],"redistribution_allowed":r["redistribution_allowed"],"classification_source":r["classification_source"]} for r in hits]}
    print(json.dumps(payload,ensure_ascii=False,indent=2)); return 0 if hits else 3
if __name__=="__main__": raise SystemExit(main())
