# Import private-local-assets.zip into the figure corpus

The user has confirmed that the packaged figures are authorized for repository redistribution.

## Package invariants

- package: `private-local-assets.zip`
- SHA-256: `b29f63e9d8feeccb2f80987609d712455289303969241ca7aad55c6415a3eac4`
- expected PNG assets: `139`
- packaged entries: `205`

## Import

From the repository root on branch `feat/figure-style-corpus-v0.1`:

```powershell
python projects/scientific-figure-style-corpus/scripts/import_zotero_private_assets.py C:\path\to\private-local-assets.zip
```

The importer verifies the package hash, verifies all 139 PNG SHA-256 values against `zotero-private-manifest.csv`, and then writes:

- PNG assets to `projects/scientific-figure-style-corpus/assets/zotero/<journal>/<item-key>/...png`
- provenance manifest to `projects/scientific-figure-style-corpus/manifests/zotero-private-manifest.csv`
- non-PNG QA/handoff material to `projects/scientific-figure-style-corpus/handoff/private-local-assets-2026-09-12/`

After the importer succeeds, inspect `git status` and commit the generated files on the same Draft PR branch. Do not merge PR #20 as part of this import.
