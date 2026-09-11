# Zotero figure ingestion

## Purpose

Import high-value scientific figures from PDFs already downloaded in the user's local Zotero library into the same scientific-figure corpus used by the raw-image database.

The importer is deliberately local and rights-aware:

- Zotero is read-only;
- PDFs are never modified;
- extracted figures from publisher-copyright PDFs stay in a private local asset directory;
- GitHub may store the manifest/metadata, but private figure assets must not be committed unless redistribution rights are verified separately.

## Script

`projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py`

## Default selection logic

### Core journals

- The ISME Journal
- Nature Communications
- Environmental Science & Technology
- Water Research

### Secondary accepted journals

Includes high-value related sources such as Nature Microbiology, Science Advances, Nature Water, Energy & Environmental Science, ES&T Letters, Environmental Science & Ecotechnology, Microbiome, mBio, Applied and Environmental Microbiology, and selected environmental-engineering journals.

Other journals can be admitted with `--allow-other-journals`, but they must pass a project-topic relevance threshold.

### Figure priority

The importer scores captions for:

- schematic / conceptual overview;
- mechanism / pathway;
- microbial interaction / cross-feeding / syntrophy;
- EET / EEU / DIET / electron transfer;
- material–microbe / mineral / electrode / conductive interface;
- methane oxidation / methanotrophy;
- dark or inorganic carbon fixation;
- oxygen limitation / microoxic–anoxic / redox gradients;
- experimental design and workflow.

Routine quantitative plots are down-weighted.

## Default output

Private figures:

`~/scientific-figure-corpus-private/zotero/`

Manifest:

`projects/scientific-figure-style-corpus/manifests/zotero-private-manifest.csv`

Every record includes:

- Zotero item key;
- attachment key;
- journal and journal tier;
- article title, year, DOI;
- figure ID and PDF page;
- caption;
- relevance score;
- inferred figure purpose;
- private asset path;
- pixel dimensions;
- SHA256;
- redistribution status;
- visual-inspection status.

## Run

From the repository root:

```bash
python -m pip install pymupdf
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --max-figures 100 \
  --max-per-article 3
```

The script attempts to locate the Zotero data directory automatically. If needed, pass it explicitly:

```bash
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --zotero-root "C:/Users/<USER>/Zotero"
```

To include strongly relevant papers outside the accepted journal list:

```bash
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --allow-other-journals
```

## Corpus counting rule

A Zotero-derived image may count toward the **private research corpus** once the file has been rendered, SHA256 recorded, and the source article/figure identified.

It does **not** count toward the public mirrored-image corpus unless redistribution rights for that figure are separately verified.

## Manual QA still required

Automated PDF crop extraction is a first-pass ingestion step. Before element extraction or Style Router training, inspect each retained figure for:

1. crop completeness;
2. correct figure/caption pairing;
3. actual visual relevance;
4. duplicate or near-duplicate panels;
5. whether the figure is a publisher-owned original or third-party reproduced material;
6. suitability for 2D/2.5D style learning.
