<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# 006_System-Manifests

## Purpose
Pipeline control, audit logs, registries, and run reports. All pipeline outputs are written here for traceability.

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `tree-snapshots/` | JSON/TXT snapshots of raw source layer |
| `registries/` | CSV file registries tracking all files |
| `runs/` | Timestamped reports for every command |
| `logs/` | Operational logs |

## For AI Agents

### Working In This Directory
- This is the OUTPUT directory - DO NOT edit files here manually
- All pipeline commands write reports here
- Check runs/ folder after running any pipeline command

### Common Patterns
- `latest_*.json` and `latest_*.txt` are symlink-style copies
- Timestamped files: `{timestamp}_{command}_{report}.*`
- Reports are append-only for auditability

### Testing Requirements
- Verify new reports appear after pipeline runs
- Check report structure matches expected format

## Data Flow
All pipeline stages write outputs here:
- scan → tree-snapshots/, registries/
- status → runs/latest_status_report.*
- lint → runs/latest_lint_report.*
- convert → runs/latest_convert_*, registries/
- ocr-execute → runs/latest_ocr_execute_report.*
- reconcile → runs/latest_reconcile_report.*

<!-- MANUAL: -->