# P1 Packet Snapshot Rebase Kimi Review

Last updated: 2026-05-02T07:20:07Z

## Prompt summary

Kimi was asked to review the P1 custody snapshot rebase plan after three P1 packets were consumed by steward-approved admissions: Deep Foundations and Shallow Foundations reciprocal `CROSS_DOMAIN_ALIGNMENT`, plus Buildings metadata-only `DISAMBIGUATED_KEEP_SEPARATE`.

## Accepted suggestions

- Refresh current packet source snapshots and packet hashes against the new graph/canonical state.
- Preserve old reviewed packet hashes and source snapshot hashes as historical review evidence.
- Add explicit lineage fields showing old hash -> current hash carry-forward.
- Mark carried-forward reviews with a caveat: the Kimi review was not rerun and is not a new ontology review.
- Link consumed packets to exact approval IDs, decision IDs, and admitted relationship IDs.
- Treat consumed packets as closed by admission/disambiguation metadata while retaining audit history.
- Re-sign refreshed payloads only when a real HMAC key exists; do not copy old signatures onto new payloads.
- Use UI wording such as `review carried forward`, `consumed by steward admission`, and `snapshot refreshed`.

## Rejected suggestions / risks not accepted

- Overwriting old hashes without lineage.
- Creating a fake new Kimi review during rebase.
- Carrying old HMAC signatures onto refreshed packet payloads.
- Presenting carried-forward review as steward approval, ontology truth, source truth, merge safety, alias authority, redirect authority, or tombstone authority.
- Reopening consumed/admitted packets as unresolved duplicate work.

## Deferred suggestions

- Fresh Kimi ontology review for each changed packet.
- HMAC-signed regeneration until a real packet HMAC key is configured.
- Broader P1 triage/admission work after the custody rebase is validated.

## Implementation response

Accepted guidance was implemented through explicit rebase lineage, carried-forward review metadata, consumed packet status, and validation metrics. No rejected risk was implemented. Deferred items remain in the next-action backlog.
