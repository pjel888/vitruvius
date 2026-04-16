# 2026-04-16 Human Review Packet Validation

## Purpose
Validate the repo-local file-based human review loop for Ralph/OMX escalation points.

## Artifacts created
- `/.ai/14_human_inbox/README.md`
- `/.ai/14_human_inbox/template.request.json`
- `/.ai/14_human_inbox/template.response.json`
- live packet pair for the current RA-9514 relationship review question:
  - `/.ai/14_human_inbox/2026-04-16_ra9514-relationship-admission.request.json`
  - `/.ai/14_human_inbox/2026-04-16_ra9514-relationship-admission.response.json`

## Validation performed
- JSON parse validation for:
  - template request
  - template response
  - live RA-9514 request
  - live RA-9514 response
- queue/index validation for:
  - `/.ai/14_human_inbox/index.json`
  - `/.ai/14_human_inbox/CURRENT_PENDING.md`
- request/response split verified:
  - request packet is immutable guidance/evidence
  - response packet is the only file the reviewer needs to edit

## Result
The file-based human approval loop is now repo-local, auditable, and reusable for future Ralph checkpoints.

## Reviewer instructions
When a human decision is needed:
1. read the `*.request.json`
2. edit only the paired `*.response.json`
3. set `status` to `answered`
4. fill reviewer, timestamp, notes, and item decisions
5. tell Codex/Ralph that the response file is ready

## Current convenience files
- Queue index: `/.ai/14_human_inbox/index.json`
- Human-facing queue summary: `/.ai/14_human_inbox/CURRENT_PENDING.md`

## Single-file human response flow (latest refinement)
- Human-facing workflow is now reduced to **one editable file only**: `/.ai/14_human_inbox/ANSWER_HERE.md`
- `CURRENT_PENDING.md` is now only a pointer to `ANSWER_HERE.md`
- `README.md` now gives the same one-file instruction
- `index.json` now carries `human_edit_file` pointing to `/.ai/14_human_inbox/ANSWER_HERE.md`

Fresh validation evidence:
- `ANSWER_HERE.md` exists and contains the current pending packet/questions
- `CURRENT_PENDING.md` points only to `ANSWER_HERE.md`
- `README.md` tells the reviewer not to create files or edit JSON
- `index.json` reports `pending_count = 1` and `human_edit_file = .ai/14_human_inbox/ANSWER_HERE.md`

## One-file human answer format refinements
- The human-facing file no longer asks the human to enter a timestamp; the computer will fill that automatically later.
- The human-facing file now includes more context for each item:
  - `MACHINE_INTENT`
  - `HUMAN_READABLE_QUESTION`
  - `WHAT_APPROVE_MEANS`
  - `WHAT_REJECT_MEANS`
- A parser now tolerates these explanatory fields while still validating the final human decisions.

Fresh validation evidence:
- `ANSWER_HERE.md` updated to include machine intent + human-readable wording
- `scripts/tests/test_human_inbox.py` updated for the new single-file format
