import csv,json,sys
from pathlib import Path
project=Path('projects/scientific-figure-style-corpus')
sys.path.insert(0,str(project/'scripts'))
from zotero_pipeline import write_csv
manifest=project/'manifests/zotero-private-manifest.csv'
rows=list(csv.DictReader(manifest.open(encoding='utf-8')))
path=project/'manifests/zotero-qa-decisions.csv'
decisions=list(csv.DictReader(path.open(encoding='utf-8')))
checks=json.loads(Path('work/qa/source/source-checks.json').read_text())
checked={r['sample_id']:r for r in checks}
for d in decisions:
    if d['sample_id'] in checked:
        check=checked[d['sample_id']]
        d.update(sha256=check['sha256'],decision='accept')
        d['notes']='Source PDF and rendered crop visually compared 2026-09-11: full figure, matching caption, readable resolution, useful schematic or integrated layout. Private use only; rights not cleared.'
        if check['index']==29:
            d['notes']+=' Minor running-header strip retained; does not obscure the complete figure.'
        if check['index']==134:
            d['notes']+=' Original accepted-manuscript watermark retained.'
for r in rows:
    if r['sample_id'] in checked:
        assert r['sha256']==checked[r['sample_id']]['sha256']
        r['visual_inspection_status']='complete'
        d=next(d for d in decisions if d['sample_id']==r['sample_id'])
        r['notes']=d['notes']
write_csv(path,decisions)
write_csv(manifest,rows)
summary_path=project/'manifests/zotero-ingest-summary.json'
summary=json.loads(summary_path.read_text())
summary['manual_qa_pending']=sum(r['visual_inspection_status']!='complete' for r in rows)
summary['source_visual_qa_complete']=len(checked)
summary['contact_screen_retained']=len(rows)
summary_path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
selection=json.loads(Path('work/qa/selection.json').read_text())
report={'date':'2026-09-11','random_seed':20260911,
    'random_sample_ids':[rows[i]['sample_id'] for i in selection['random']],
    'highest_relevance_sample_ids':[r['sample_id'] for r in rows[:10]],
    'core_journal_sample_ids':{j:[r['sample_id'] for r in rows if r['journal']==j][:3] for j in ['The ISME Journal','Nature Communications','Environmental Science & Technology','Water Research']},
    'source_comparisons':checks,'qa_status':'required sample visual QA passed; remaining rows contact-screened only'}
(project/'manifests/zotero-visual-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Source visual QA complete:',len(checked),'pending:',summary['manual_qa_pending'])
