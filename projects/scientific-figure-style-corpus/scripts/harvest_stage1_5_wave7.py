#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,json,re,sys,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse
import requests
SCRIPT_DIR=Path(__file__).resolve().parent;sys.path.insert(0,str(SCRIPT_DIR))
import scan_stage1_5_wave2_oa_package as aws
ROOT=Path('projects/scientific-figure-style-corpus')
SELECTED={
 ('S15-056','1'):('B_style_reference','EET kinetic comparison','flat 2D comparison','three-route comparison','high'),
 ('S15-056','3'):('A_style_reference','transmembrane EET mechanism','2D pathway cutaway','membrane electron-potential pathway','high'),
 ('S15-057','4'):('A_style_reference','electrode-microbe EET mechanism','flat 2D mechanism','three-state electrode interface','high'),
 ('S15-057','5'):('B_style_reference','electrode-biofilm response mechanism','editorial 2D overview','four-column before-after mechanism','medium'),
 ('S15-059','4'):('A_style_reference','mineral-linked EET pathway','2D pathway cutaway','mineral-to-membrane electron-flow architecture','high'),
 ('S15-062','3'):('B_style_reference','environmental redox gradient','gradient profile schematic','depth-resolved oxic-suboxic profile','medium'),
 ('S15-063','9'):('B_style_reference','environmental spatial gradient','2D environmental profile','transect-depth redox heatmap','medium'),
 ('S15-063','10'):('A_style_reference','environmental methane-seep architecture','editorial 2D overview','layered geochemical-zone reconstruction','high'),
}
MFIELDS=['candidate_id','year','journal','article_url','figure_number','style_learning_tier','primary_purpose','style_family','layout_archetype','domain_relevance_to_bath_rp','rights_status','license','cloud_version','figure_id','caption','source_media_url','asset_path','content_type','size_bytes','sha256','inspection_status']
def active(p):
 if not p.exists(): return 0
 return sum(r.get('style_learning_tier') in {'A_style_reference','B_style_reference'} for r in csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 scan=ROOT/'validation/stage1_5_wave7_scan/stage1_5_wave7_all_figures.csv'; rows=list(csv.DictReader(scan.open(encoding='utf-8',newline='')))
 ann=ROOT/'annotations/stage1_5_wave7_figure_screening.csv'; ann.parent.mkdir(parents=True,exist_ok=True)
 af=['candidate_id','year','journal','article_title','article_url','figure_number','style_learning_tier','decision','public_mirror','rights_status','license','primary_purpose','style_family','layout_archetype','domain_relevance_to_bath_rp','visual_qa_note']; classified=[]
 for r in rows:
  key=(r['candidate_id'],r['figure_number']); resolved=r['image_resolved'].lower()=='true'; lic=r['license']
  if key in SELECTED:
   tier,purpose,style,layout,rel=SELECTED[key]; dec='A' if tier.startswith('A_') else 'B'; pub='true'; rights='public_mirror_allowed_cc_by'; note='Direct visual QA: retained for genuinely distinct visual grammar.'
  elif not resolved or lic!='CC BY':
   tier='exclude';dec='exclude';pub='false';rights='reference_only_restrictive_or_unresolved';purpose='reference only';style='not active';layout='not active';rel='low';note='Restrictive/unresolved or no direct preview; not harvested.'
  elif int(r['caption_score'])>=4:
   tier='C_context_reference';dec='C';pub='false';rights='public_source_not_selected';purpose='contextual EET/material/environmental evidence';style='mixed_or_data_heavy';layout='context only';rel='medium';note='Direct visual QA: relevant but redundant, data-heavy, microscopy-heavy, or weaker than selected reference.'
  else:
   tier='exclude';dec='exclude';pub='false';rights='public_source_not_selected';purpose='low-value for style corpus';style='not active';layout='not active';rel='low';note='Direct visual QA: low transfer value or ordinary data/micrograph grammar.'
  classified.append({k:v for k,v in dict(r,style_learning_tier=tier,decision=dec,public_mirror=pub,rights_status=rights,primary_purpose=purpose,style_family=style,layout_archetype=layout,domain_relevance_to_bath_rp=rel,visual_qa_note=note).items() if k in af})
 with ann.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=af);w.writeheader();w.writerows(classified)
 selected=[r for r in classified if r['public_mirror']=='true']; assets=ROOT/'assets/stage1_5'; assets.mkdir(parents=True,exist_ok=True); out=[];fail=[];cache={};s=requests.Session();s.headers.update({'User-Agent':'codex-workbench-wave7/0.1'})
 for r in selected:
  try:
   pmcid=re.search(r'(PMC\d+)',r['article_url'],re.I).group(1).upper()
   if pmcid not in cache:
    version,meta=aws.choose_version(s,pmcid);allowed,lic=aws.allowed_license(meta)
    if not allowed: raise RuntimeError('license not mirror-compatible')
    xr=s.get(aws.as_https(str(meta.get('xml_url') or '')),timeout=60);xr.raise_for_status();cache[pmcid]=(version,ET.fromstring(xr.content),aws.media_map(meta),lic)
   version,article,mmap,lic=cache[pmcid]; n=int(r['figure_number']); target=None
   for ordinal,fig in enumerate(article.findall('.//fig'),1):
    label=aws.txt(fig.find('label'));m=re.search(r'(\d+)',label);num=int(m.group(1)) if m else ordinal
    if num==n:target=fig;break
   if target is None: raise RuntimeError('figure not found')
   cap=aws.txt(target.find('caption'))
   if aws.risk(cap): raise RuntimeError('third-party risk')
   g=target.find('graphic');href=g.attrib.get(aws.XLINK,'') if g is not None else '';media=aws.find_media(mmap,href)
   if not media: raise RuntimeError('no media URL')
   ir=s.get(media,timeout=60);ir.raise_for_status();data=ir.content;suffix=PurePosixPath(urlparse(media).path).suffix.lower() or '.img';p=assets/r['candidate_id']/f"{r['candidate_id']}_fig{n}{suffix}";p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);sha=hashlib.sha256(data).hexdigest()
   out.append({'candidate_id':r['candidate_id'],'year':r['year'],'journal':r['journal'],'article_url':r['article_url'],'figure_number':str(n),'style_learning_tier':r['style_learning_tier'],'primary_purpose':r['primary_purpose'],'style_family':r['style_family'],'layout_archetype':r['layout_archetype'],'domain_relevance_to_bath_rp':r['domain_relevance_to_bath_rp'],'rights_status':r['rights_status'],'license':lic,'cloud_version':version,'figure_id':target.attrib.get('id',f'fig{n}'),'caption':cap,'source_media_url':media,'asset_path':str(p.relative_to(ROOT)),'content_type':ir.headers.get('Content-Type',''),'size_bytes':str(len(data)),'sha256':sha,'inspection_status':'direct_visual_QA_then_AWS_harvested'})
  except Exception as e:fail.append({'candidate_id':r['candidate_id'],'figure_number':r['figure_number'],'error':str(e)})
 manifest=ROOT/'manifests/stage1_5_wave7_harvested_figures.csv';
 with manifest.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=MFIELDS);w.writeheader();w.writerows(out)
 prior={}
 for i in range(1,7):
  name='stage1_5_harvested_figures.csv' if i==1 else f'stage1_5_wave{i}_harvested_figures.csv';p=ROOT/'manifests'/name
  if p.exists():
   for x in csv.DictReader(p.open(encoding='utf-8',newline='')):
    if x.get('sha256'):prior.setdefault(x['sha256'],[]).append(name+':'+x.get('candidate_id','')+':fig'+x.get('figure_number',''))
 hashes=[x['sha256'] for x in out];within=sorted({h for h in hashes if hashes.count(h)>1});cross=[{'sha256':x['sha256'],'wave7':x['candidate_id']+':fig'+x['figure_number'],'prior':prior[x['sha256']]} for x in out if x['sha256'] in prior];file_errors=[]
 for x in out:
  p=ROOT/x['asset_path']
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:file_errors.append(x['asset_path'])
 ok=len(out)==len(selected) and not fail and not within and not cross and not file_errors
 names=['stage1_5_harvested_figures.csv']+[f'stage1_5_wave{i}_harvested_figures.csv' for i in range(2,8)];counts=[active(ROOT/'manifests'/n) for n in names];total=42+sum(counts)
 report={'wave':7,'screened_figure_rows':len(rows),'classification_counts':dict(Counter(r['decision'] for r in classified)),'selected_assets':len(selected),'harvested_assets':len(out),'failures':fail,'within_wave_duplicate_hashes':within,'cross_wave_duplicates':cross,'file_validation_errors':file_errors};(ROOT/'validation/stage1_5_wave7_harvest_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 final={'validated_assets':len(out),'selected_assets':len(selected),'checksum_validation':'passed' if not file_errors else 'failed','within_wave_duplicate_hashes':within,'cross_wave_duplicates':cross,'manifest_complete':len(out)==len(selected),'validation_passed':ok,'active_ab_total':total};(ROOT/'validation/stage1_5_wave7_final_validation.json').write_text(json.dumps(final,indent=2),encoding='utf-8')
 status={'stage':'1.5_recent_targeted_refinement','stage1_ab_baseline':42,'wave_active_ab_added':counts,'current_ab_after_wave7':total,'target_ab_range':[96,100],'wave7_validation':'passed' if ok else 'failed','next_action':'corpus-level balance QA' if ok and total>=96 else 'continue targeted refinement'};(ROOT/'validation/stage1_5_status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));print(json.dumps(final,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
