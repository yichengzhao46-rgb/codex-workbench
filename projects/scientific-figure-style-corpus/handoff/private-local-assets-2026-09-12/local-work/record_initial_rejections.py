import csv
from pathlib import Path
p=Path('projects/scientific-figure-style-corpus/manifests')
rows=list(csv.DictReader((p/'zotero-private-manifest.csv').open(encoding='utf-8')))
reject={
2:'Routine bar/line panels dominate; small bottle cartoon adds insufficient design value.',
9:'Routine quantitative growth/metabolite plots dominate; excluded from primary schematic corpus.',
29:'Routine line/bar statistics; no substantive schematic in extracted figure.',
32:'Routine electrochemical characterization; standard setup is insufficient additional value.',
35:'Data and specimen panels dominate; small electrode layout has limited corpus value.',
36:'Routine isotope time courses with small workflow; stronger design examples retained.',
38:'Dense electrochemical characterization dominates; stronger interface schematics preferred.',
39:'Heatmap/electrochemical plots dominate; small cartoon does not justify full-figure inclusion.',
41:'Routine phylogenetic tree; caption matching gave a false visual-design signal.',
53:'Data/microscopy-dominated comparison; not retained as schematic exemplar.',
55:'Simple ATP bar chart with generic pathway; limited design value.',
56:'Specimen photographs dominate; limited conceptual-schematic value.',
57:'Routine quantitative composition panels dominate; retain the other mechanism figure.',
61:'Routine phylogeny and electrochemical data dominate.',
63:'Glossy realistic 3D/water texture; outside active 2D/light-2.5D style preference.',
64:'Glossy dense 3D montage; outside active restrained 2D/light-2.5D corpus.',
71:'Routine activity/stability plots and microscopy dominate.',
76:'Genome ring map; excluded routine genomics visual.',
80:'Routine differential-expression/quantitative panels dominate.',
82:'Simple protein-domain cartoon; weak mechanism/layout learning value.',
89:'Routine metabolomics pie/bar/heatmap; no substantive schematic.',
90:'Routine chemical characterization plots dominate.',
92:'Ordinary line/bar graph; false signal from caption mention of a different figure.',
94:'Routine treatment time series and bar graphs dominate.'}
with (p/'zotero-qa-decisions.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['sample_id','sha256','decision','notes']);w.writeheader()
    for i,reason in reject.items():
        r=rows[i];w.writerow(dict(sample_id=r['sample_id'],sha256=r['sha256'],decision='reject',notes=reason))
print(len(reject))
