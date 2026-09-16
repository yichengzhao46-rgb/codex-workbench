# Validation report

Validated 2026-09-16. Authoritative object: the bounded community-reference-scouting package. Project key: CODEX; primary class: PR-OPS, with source/rights and reference-image QA checks. This is a source-only project, not an installed skill or a production scientific figure.

## Checks performed

| Check | Result | Evidence / scope |
| --- | --- | --- |
| JSON identity, required fields and cross-references | PASS | 18 sources, 20 candidate rules, 10 image records |
| Rights gating | PASS | All 4 saved PNGs have CC BY 4.0 records, attribution, change statements and specific review notes |
| Binary/source integrity | PASS | Four PNG signatures, dimensions, byte counts and SHA256 values match their manifests |
| Untracked assets within the package | PASS | Asset directory contains exactly the four public-mirror entries |
| Link-only separation | PASS | Six records contain no local asset path, byte count or download URL |
| Sensitive URL parameters | PASS | No signed download credentials or app-sharing tokens in manifest data |
| Markdown relative links | PASS | Local references resolve; this is a structural check, not full external-link monitoring |
| Direct reference-image QA | PASS for inspection | Four saved images and one browser-only BioRender infographic inspected; specific weaknesses retained in visual notes |
| Negative gate tests | PASS | 8 cases rejected: unknown source, blocked source supporting rule, unlicensed mirror, bad hash, path escape, link-only copy, automatic PR20 approval, sensitive sharing URL |
| Change isolation | PASS | New files only under projects/community-reference-scouting; base main at e3d30727c56520fcbecc952d4b425895e59448f2 |
| Git whitespace/diff check | PASS | git diff --cached --check; staged scope and rights/interface diff reviewed |
| PR20 read-only snapshot | PASS | Re-read before publication: c4dea1b31db6b022e73e29967a0f02c959e39bcb, Draft / open / unmerged; no writes issued to PR20 |

## Reproduce

```sh
python projects/community-reference-scouting/scripts/validate.py --self-test
git diff --check
```

The first command prints PASS with 18 sources, 20 rules, 10 reference records, 4 public assets and 8 negative cases rejected. It uses only Python's standard library and does not access the network or write files.

## Limits and next validation

- Source access is recorded individually. Xiaohongshu/ Zhihu remain blocked; the Chinese YouTube video has metadata-only coverage; the Nature profile has partial public text.
- The four source PNGs were visually inspected as references; this does not mean all design features should be copied. See [visual review](../evidence/visual-review.md).
- Browser-only reference screenshots were not saved or republished. No claims of full visual QA for uninspected linked images.
- Markdown is source/link checked; no PDF or publication-layout rendering was produced or claimed.
- User selection, a real manuscript figure trial, independent reader feedback and PR20 ingestion are pending. No candidate was promoted.
- Automated checks cannot establish copyright ownership or scientific validity. Rights statements and evidence ceilings are documented for review.

## Rollback and promotion

Close the Draft PR before merge, or revert its isolated commit after an explicitly authorized merge. No existing files, installed skills, PR20 IDs, Zotero inputs or global instructions need restoration. No codex-playbook promotion is proposed until a real task validates the workflow.
