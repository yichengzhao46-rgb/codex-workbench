# Project Artifact Cleanup Skill — Controlled Forward Validation

## Result

**PASS — controlled classification/workflow validation.**

No destructive filesystem action was performed. This validation tests whether the proposed Skill's rules classify a mixed research/project directory safely and whether its approval boundaries are sufficient.

## Expected classification outcome

| Path | Expected | Skill outcome |
| --- | --- | --- |
| `report/Confirmation_Report_v3.docx` | KEEP | KEEP |
| `report/Confirmation_Report_v2.docx` | ARCHIVE | ARCHIVE |
| `report/Confirmation_Report_preview.pdf` | SAFE-DELETE | SAFE-DELETE |
| `report/rendered/page_01.png` | SAFE-DELETE | SAFE-DELETE |
| `report/rendered/page_02.png` | SAFE-DELETE | SAFE-DELETE |
| `figures/Fig3.opju` | KEEP | KEEP |
| `figures/Fig3_600dpi.tif` | KEEP | KEEP |
| `figures/Fig3_preview.png` | SAFE-DELETE | SAFE-DELETE |
| `figures/Fig3_old.ai` | ARCHIVE | ARCHIVE |
| `data/raw_riboflavin.xlsx` | KEEP | KEEP |
| `data/riboflavin_summary.csv` | KEEP | KEEP |
| `data/riboflavin_summary_copy.csv` | REVIEW | REVIEW |
| `scripts/analyze_riboflavin.py` | KEEP | KEEP |
| `tests/reference_output.json` | KEEP | KEEP |
| `scratch/debug_output.csv` | SAFE-DELETE | SAFE-DELETE |
| `tmp/~$Confirmation_Report_v3.docx` | SAFE-DELETE | SAFE-DELETE |
| `notes/old_results.txt` | KEEP | KEEP |
| `unknown/sample_backup.csv` | REVIEW | REVIEW |
| `.gitignore` | KEEP | KEEP |
| `README.md` | KEEP | KEEP |

## Acceptance checks

- [x] Zero current/source/raw files classified SAFE-DELETE.
- [x] All obvious preview/render/temp/debug artifacts classified SAFE-DELETE.
- [x] Superseded editable research sources classified ARCHIVE rather than deleted.
- [x] Apparent duplicate without verified provenance classified REVIEW.
- [x] Backup-like filename without verified recoverability classified REVIEW.
- [x] Untracked raw research data classified KEEP.
- [x] Tracked regression fixture classified KEEP despite output-like name.
- [x] Old-looking but referenced file classified KEEP.
- [x] First pass remains read-only.
- [x] SAFE-DELETE action defaults to reversible staging.
- [x] Permanent deletion requires a second manifest and explicit approval.
- [x] Changed-since-review files are removed from the deletion set.
- [x] `git clean -fdx` and broad `rm -rf *` behavior are explicitly prohibited.
- [x] Exact-file deletion negative control does not require project-wide cleanup ceremony.

## Failure modes successfully blocked

### 1. `untracked = disposable`

Blocked. The raw spreadsheet remains KEEP even though it is untracked.

### 2. `old filename = delete`

Blocked. `old_results.txt` remains KEEP because it is referenced, and `Fig3_old.ai` is ARCHIVE because it retains provenance/editability value.

### 3. `copy/backup filename = duplicate`

Blocked. Both uncertain copy/backup cases remain REVIEW until provenance and reconstructability are established.

### 4. `generated-looking file = disposable`

Blocked for the tracked regression fixture. File role/dependency overrides naming heuristics.

### 5. first-pass permanent deletion

Blocked by the dry-run → approval → staging → post-clean verification → final deletion manifest sequence.

## External benchmark adaptation

The proposed Skill uses three external patterns as design constraints rather than implementations:

1. **Git dry-run / interactive cleanup principle** — inspect candidates before destructive cleanup; adapted into a richer project inventory because Git tracking state alone is not enough to decide scientific value.
2. **Recoverable Trash principle** — separate reversible removal from permanent deletion; adapted to `_cleanup_staging/YYYY-MM-DD/` with a final manifest.
3. **Research-data provenance principle** — raw/source research data and meaningful prior versions require retention/archival judgment rather than generic deletion heuristics.

Rejected:

- automatically deleting all ignored/untracked files;
- filename-only heuristics;
- immediately permanently deleting a first-pass candidate list;
- treating every superseded research document as disposable.

## Evidence boundary

This is **controlled manifest-level validation**, not a real filesystem run. It establishes that the instruction set handles the designed high-risk classification cases correctly, but does not yet verify:

- real path traversal or symlink behavior;
- filesystem permissions/locked files;
- Windows/macOS/Linux Trash behavior;
- Git submodules/worktrees;
- hidden files beyond the explicit manifest;
- dependency detection in a large real research directory;
- actual space calculation;
- recovery after a staged move.

## Promotion recommendation

Promote from `experimental` to **validated / controlled-forward-validated once**, but do not call it stable yet.

A real low-risk folder cleanup should be the next validation. The first real use should stop after dry-run unless the user separately approves staging. If that case succeeds without false deletions, the Skill can be reconsidered for `stable / forward-validated once` within a bounded workspace-cleanup scope.
