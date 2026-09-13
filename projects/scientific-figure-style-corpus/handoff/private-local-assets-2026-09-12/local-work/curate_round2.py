import csv,json
from pathlib import Path
p=Path('projects/scientific-figure-style-corpus/manifests')
rows=list(csv.DictReader((p/'zotero-private-manifest.csv').open(encoding='utf-8')))
old=list(csv.DictReader((p/'zotero-qa-decisions.csv').open(encoding='utf-8')))
reject={2,9,14,19,22,47,48,50,58,59,60,64,71,73,82,91,93,99,105,107,110,113,115,121,122,130,131,135,136,146,151,152,155,157,163,164,165,171,172,177,179}
repairs={41,101,123,133,173}
purposes={
 'environmental_process':[36,40,43,51,87,94],
 'microbial_interaction':[20,25,30,31,37,45,67,77,97,108,120,141,145,174,175],
 'experimental_design':[17,69,75,104,106,117,139,150],
 'comparative_perturbation':[11,21,42,70,100,114,153,166,167],
 'material_microbe_interface':[52,85,127,168],
 'conceptual_overview':[15,27,116,118],
 'multiscale_schematic':[28,86,88,90],
 'integrated_mechanism':[6,32,41,46,68,83,84,92,102,103,126,134],
}
lookup={i:k for k,ids in purposes.items() for i in ids}
merged={r['sample_id']:dict(r,target_primary_purpose='') for r in old}
for i,r in enumerate(rows):
    reason='Ordinary quantitative/genomic/microscopy panels dominate; insufficient schematic learning value.'
    if i in {121,155,157}:reason='Glossy realistic 3D rendering excluded from active 2D/light-2.5D corpus.'
    if i==177:reason='Chemical redox diagram without a microbial/interface learning focus.'
    note=reason if i in reject else 'Contact-sheet visual relevance screening passed; full-resolution source-page QA remains pending.'
    if i in repairs:note+=' Crop flagged for systematic geometry repair and reinspection.'
    merged[r['sample_id']]=dict(sample_id=r['sample_id'],sha256=r['sha256'],decision='reject' if i in reject else 'retain',notes=note,target_primary_purpose=lookup.get(i,''))
with (p/'zotero-qa-decisions.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['sample_id','sha256','decision','notes','target_primary_purpose']);w.writeheader();w.writerows(merged.values())
Path('work/round2-rows.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
print('retained',len(rows)-len(reject),'rejected',len(reject),'repair_indices',sorted(repairs))
