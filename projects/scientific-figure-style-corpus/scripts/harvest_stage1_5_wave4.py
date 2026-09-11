#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,re,sys,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse
import requests
SCRIPT_DIR=Path(__file__).resolve().parent;sys.path.insert(0,str(SCRIPT_DIR))
import scan_stage1_5_wave2_oa_package as aws
FIELDS=['candidate_id','year','journal','article_url','figure_number','style_learning_tier','primary_purpose','style_family','layout_archetype','domain_relevance_to_bath_rp','rights_status','license','cloud_version','figure_id','caption','source_media_url','asset_path','content_type','size_bytes','sha256','inspection_status']
def truthy(v):return str(v).strip().lower() in {'1','true','yes','y'}
def active(path):
 if not path.exists():return 0
 return sum(r.get('style_learning_tier') in {'A_style_reference','B_style_reference'} for r in csv.DictReader(path.open(encoding='utf-8',newline='')))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',default='projects/scientific-figure-style-corpus');ap.add_argument('--selection',default='projects/scientific-figure-style-corpus/annotations/stage1_5_wave4_figure_screening.csv');a=ap.parse_args()
 root=Path(a.project_root).resolve();sel=Path(a.selection).resolve();assets=root/'assets/stage1_5';manifest=root/'manifests/stage1_5_wave4_harvested_figures.csv';report=root/'validation/stage1_5_wave4_harvest_report.json';status=root/'validation/stage1_5_status.json';finalv=root/'validation/stage1_5_wave4_final_validation.json';assets.mkdir(parents=True,exist_ok=True);manifest.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
 rows=list(csv.DictReader(sel.open(encoding='utf-8',newline='')));selected=[r for r in rows if truthy(r['public_mirror'])];s=requests.Session();s.headers.update({'User-Agent':'codex-workbench-stage1.5-wave4/0.1','Accept-Language':'en-US,en;q=0.8'});out=[];fail=[];cache={}
 for r in selected:
  cid=r['candidate_id'];n=int(r['figure_number']);url=r['article_url']
  try:
   if r['rights_status']!='public_mirror_allowed_cc_by':raise RuntimeError('rights not mirror-compatible')
   m=re.search(r'(PMC\d+)',url,re.I)
   if not m:raise RuntimeError('missing PMCID')
   pmcid=m.group(1).upper()
   if pmcid not in cache:
    version,meta=aws.choose_version(s,pmcid);allowed,lic=aws.allowed_license(meta)
    if not allowed:raise RuntimeError(f'AWS license not allowed: {lic}')
    xml_url=aws.as_https(str(meta.get('xml_url') or ''))
    if not xml_url:raise RuntimeError('missing xml_url')
    xr=s.get(xml_url,timeout=60);xr.raise_for_status();article=ET.fromstring(xr.content);mmap=aws.media_map(meta);cache[pmcid]=(version,article,mmap,lic)
   version,article,mmap,lic=cache[pmcid];target=None
   for ordinal,fig in enumerate(article.findall('.//fig'),1):
    label=aws.txt(fig.find('label'));mm=re.search(r'(\d+)',label);num=int(mm.group(1)) if mm else ordinal
    if num==n:target=fig;break
   if target is None:raise RuntimeError(f'figure {n} not found')
   cap=aws.txt(target.find('caption'));risk=aws.risk(cap)
   if risk:raise RuntimeError(f'third-party risk: {risk}')
   graphic=target.find('graphic');href=graphic.attrib.get(aws.XLINK,'') if graphic is not None else '';media=aws.find_media(mmap,href)
   if not media:raise RuntimeError('no media URL')
   ir=s.get(media,timeout=60);ir.raise_for_status();data=ir.content
   if not data:raise RuntimeError('empty media response')
   suffix=PurePosixPath(urlparse(media).path).suffix.lower() or '.img';d=assets/cid;d.mkdir(parents=True,exist_ok=True);p=d/f'{cid}_fig{n}{suffix}';p.write_bytes(data);sha=hashlib.sha256(data).hexdigest()
   out.append({'candidate_id':cid,'year':r['year'],'journal':r['journal'],'article_url':url,'figure_number':str(n),'style_learning_tier':r['style_learning_tier'],'primary_purpose':r['primary_purpose'],'style_family':r['style_family'],'layout_archetype':r['layout_archetype'],'domain_relevance_to_bath_rp':r['domain_relevance_to_bath_rp'],'rights_status':r['rights_status'],'license':lic,'cloud_version':version,'figure_id':target.attrib.get('id',f'fig{n}'),'caption':cap,'source_media_url':media,'asset_path':str(p.relative_to(root)),'content_type':ir.headers.get('Content-Type',''),'size_bytes':str(len(data)),'sha256':sha,'inspection_status':'direct_contact_sheet_screened_then_aws_harvested'})
  except Exception as e:fail.append({'candidate_id':cid,'figure_number':str(n),'error':str(e)})
 with manifest.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(out)
 hashes=[x['sha256'] for x in out];duplicates=sorted({x for x in hashes if hashes.count(x)>1});ok=len(out)==len(selected) and not fail and not duplicates
 rep={'wave':4,'screened_figure_rows':len(rows),'public_mirror_selected':len(selected),'harvested_assets':len(out),'failed_or_rejected':len(fail),'tier_counts':dict(Counter(x['style_learning_tier'] for x in out)),'duplicate_hashes':duplicates,'failures':fail};report.write_text(json.dumps(rep,indent=2,ensure_ascii=False),encoding='utf-8')
 w1=active(root/'manifests/stage1_5_harvested_figures.csv');w2=active(root/'manifests/stage1_5_wave2_harvested_figures.csv');w3=active(root/'manifests/stage1_5_wave3_harvested_figures.csv');w4=active(manifest);total=42+w1+w2+w3+w4
 st={'stage':'1.5_recent_targeted_refinement','stage1_ab_baseline':42,'wave1_active_ab_added':w1,'wave2_active_ab_added':w2,'wave3_active_ab_added':w3,'wave4_active_ab_added':w4,'current_ab_after_wave4':total,'target_ab_range':[80,100],'wave4_screened_figures':len(rows),'wave4_public_assets':len(out),'wave4_validation':'passed' if ok else 'failed','next_action':'continue wave5 targeted OA refinement' if total<80 else 'active A+B target reached; perform corpus-level balance QA'};status.write_text(json.dumps(st,indent=2),encoding='utf-8');finalv.write_text(json.dumps({'validated_assets':len(out),'selected_assets':len(selected),'checksum_validation':'passed' if ok else 'failed','duplicate_hashes':duplicates,'manifest_complete':len(out)==len(selected),'validation_passed':ok},indent=2),encoding='utf-8');print(json.dumps(rep,indent=2));print(json.dumps(st,indent=2));return 0 if ok and out else 2
if __name__=='__main__':raise SystemExit(main())
