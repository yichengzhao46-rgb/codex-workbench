# Validation — 2026-10-03

## Scope

Package the already-developed PR-EXP-Workflow v1 as an additive Workbench project. No existing workflow is replaced; no model training, skill installation, continuous background scouting or GitHub merge is performed.

## Evidence

- Fig. 3.1a iterations establish white space, soft equipment colors, short serum-bottle closures, separate sampling, TCP kit and DCW filter weighing, qPCR/spectrophotometer differentiation, green Bath–RP labels, and equal Growth/RP pigment heading hierarchy with non-bold measurement symbols.
- Fig. 3.2 provides a parallel-route case. An incorrect labeling-to-EA–IRMS connection in an earlier preview was corrected. This is a recorded failure mode, not evidence of universal workflow reliability.
- The 130 × 56 mm TIFF export was decoded and verified against its source PNG: 6142 × 2646 px, 1200 dpi on both axes, RGB, LZW, identical decoded pixels. See export_verification.json.
- Repository packaging checks: JSON parse, relative Markdown links, example dimensions and SHA256, all changes confined to this new project directory.
- No software test suite added: this is a documentation/example addition, with artifact checks targeted to actual packaging risks.

## Limitations

- Case-derived and experimental. No independent forward validation on an unrelated workflow yet.
- Generated raster text is not verified Arial; no editable vector-text guarantee.
- A 1200 dpi resampled export does not create native detail or prove all labels meet final-print-size readability requirements.
- Third-party reference metadata is inherited from the earlier source package; this PR does not represent a new literature search or rights audit.
- Example images are raster previews, not editable source. Fig. 3.2 remains a draft and must not override the current typography/palette rules.

## Compact route receipt

- Objective: submit the existing experimental-workflow method as a GitHub PR.
- Initial/final route: Codex; GitHub is the packaging/provenance destination.
- Reroutes: none.
- Repository: codex-workbench, independent feature branch from main.
- Primary validation: operating-method packaging plus scientific-route and visual-contract checks.
- Completion: additive commit, reviewed changed-file list and Draft PR; no merge.

## Promotion recommendation

Reusable lesson identified. Keep experimental in Workbench until independent forward validation, user review and explicit promotion to codex-playbook.
