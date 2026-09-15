#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
SCRIPT_DIR=Path(__file__).resolve().parent;sys.path.insert(0,str(SCRIPT_DIR))
import build_raw_corpus as b
import harvest_stage1_5 as h
FIELDS=['candidate_id','year','journal','article_url','figure_number','style_learning_tier','primary_purpose','style_family','layout_archetype','domain_relevance_to_bath_rp','rights_status','license','figure_id','caption','source_media_url','asset_path','content_type','size_bytes','sha256','inspection_status']
def truthy(v): return str(v).lower() in {'true','1','yes','y'}
def active(path):
 if not path.exists(): return 0
 return sum(r.get('style_learning_tier') in {'A_style_reference','B_style_reference'} for r in csv.DictReader(path.open(encoding='utf-8',newline='')))
def fnum(fig,ordinal):
 cap=h.caption_text(fig);m=re.search(r'^\s*Fig(?:ure)?\.?\s*(\d+)',cap,re.I)
 if m:return int(m.group(1))
 m=re.search(r'(\d+)',str(fig.get('id') or ''));return int(m.group(1)) if m else ordinal
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',default='projects/scientific-figure-style-corpus');ap.add_argument('--selection',default='projects/scientific-figure-style-corpus/annotations/stage1_5_wave3_figure_screening.csv');a=ap.parse_args()
 root=Path(a.project_root).resolve();sel=Path(a.selection).resolve();assets=root/'assets/stage1_5';manifest=root/'manifests/stage1_5_wave3_harvested_figures.csv';report=root/'validation/stage1_5_wave3_harvest_report.json';status=root/'validation/stage1_5_status.json';assets.mkdir(parents=True,exist_ok=True);manifest.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
 rows=list(csv.DictReader(sel.open(encoding='utf-8',newline='')));selected=[r for r in rows if truthy(r['public_mirror'])];s=requests.Session();s.headers.update({'User-Agent':b.USER_AGENT,'Accept-Language':'en-US,en;q=0.8'});out=[];fail=[];cache={}
 for r in selected:
  try:
   if r['rights_status']!='public_mirror_allowed_cc_by':raise RuntimeError('rights not mirror-compatible')
   url=r['article_url'];cid=r['candidate_id'];n=int(r['figure_number'])
   if url not in cache:
    soup=BeautifulSoup(b.http_get(s,url).text,'html.parser');allowed,lic,lic_url=b.detect_license(soup)
    if not allowed:raise RuntimeError(f'license not allowed: {lic}')
    figs=list(soup.find_all('figure')) or list(soup.find_all('div',class_=re.compile(r'\bfig\b',re.I)));cache[url]=(figs,lic)
   figs,lic=cache[url];target=next((fig for i,fig in enumerate(figs,1) if fnum(fig,i)==n),None)
   if target is None:raise RuntimeError('figure not found')
   cap=h.caption_text(target);risk=h.third_party_reason(cap)
   if risk:raise RuntimeError(f'third-party risk: {risk}')
   pm=re.search(r'/articles/(PMC\d+)/',url,re.I);pmcid=pm.group(1).upper() if pm else ''
   data,media,ctype=b.resolve_image_bytes(s,h.preferred_image_candidates(target,url,pmcid),pmcid,15_000_000);ext=b.ext_from_response(media,ctype);d=assets/cid;d.mkdir(parents=True,exist_ok=True);p=d/f'{cid}_fig{n}{ext}';p.write_bytes(data);sha=hashlib.sha256(data).hexdigest()
   out.append({'candidate_id':cid,'year':r['year'],'journal':r['journal'],'article_url':url,'figure_number':str(n),'style_learning_tier':r['style_learning_tier'],'primary_purpose':r['primary_purpose'],'style_family':r['style_family'],'layout_archetype':r['layout_archetype'],'domain_relevance_to_bath_rp':r['domain_relevance_to_bath_rp'],'rights_status':r['rights_status'],'license':lic,'figure_id':str(target.get('id') or f'fig{n}'),'caption':cap,'source_media_url':media,'asset_path':str(p.relative_to(root)),'content_type':ctype,'size_bytes':str(len(data)),'sha256':sha,'inspection_status':'direct_contact_sheet_screened_then_harvested'})
  except Exception as e:fail.append({'candidate_id':r.get('candidate_id'),'figure_number':r.get('figure_number'),'error':str(e)})
 with manifest.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(out)
 rep={'wave':3,'screened_figure_rows':len(rows),'public_mirror_selected':len(selected),'harvested_assets':len(out),'failed_or_rejected':len(fail),'tier_counts':dict(Counter(x['style_learning_tier'] for x in out)),'failures':fail};report.write_text(json.dumps(rep,indent=2,ensure_ascii=False),encoding='utf-8')
 w1=active(root/'manifests/stage1_5_harvested_figures.csv');w2=active(root/'manifests/stage1_5_wave2_harvested_figures.csv');w3=active(manifest);st={'stage':'1.5_recent_targeted_refinement','stage1_ab_baseline':42,'wave1_active_ab_added':w1,'wave2_active_ab_added':w2,'wave3_active_ab_added':w3,'current_ab_after_wave3':42+w1+w2+w3,'target_ab_range':[80,100],'target_new_figures_range':[40,60],'wave3_screened_figures':len(rows),'wave3_public_assets':len(out),'wave3_validation':'passed' if len(out)==len(selected) and not fail else 'failed','next_action':'expand wave4 targeted OA candidates until A+B active set reaches 80–100'};status.write_text(json.dumps(st,indent=2),encoding='utf-8');print(json.dumps(rep,indent=2));print(json.dumps(st,indent=2));return 0 if len(out)==len(selected) and out else 2
if __name__=='__main__':raise SystemExit(main())
