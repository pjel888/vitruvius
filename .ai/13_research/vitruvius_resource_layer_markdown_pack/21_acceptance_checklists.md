# 21 — Acceptance Checklists

## Infrastructure checklist

- [ ] Resource model exists.
- [ ] NodeResourceLink model exists.
- [ ] SourceFamily registry exists.
- [ ] Candidate/accepted/rejected state exists.
- [ ] ResourceCheck or equivalent verification log exists.
- [ ] Local resources can be represented.
- [ ] Online resources can be represented.
- [ ] DOI/ISBN/canonical URL/local hash fields exist.
- [ ] Jurisdiction/scope field exists.
- [ ] Access type field exists.
- [ ] Verification status field exists.

## Sidebar checklist

- [ ] Eligible node click opens sidebar resource section.
- [ ] Concept node can show resources.
- [ ] Rule node can show primary source and jurisdiction warning.
- [ ] Evidence node can show evidence source.
- [ ] Document node can show metadata.
- [ ] Empty state works.
- [ ] Zero resources does not crash.
- [ ] One resource renders correctly.
- [ ] Many resources render and sort correctly.
- [ ] Rejected resources hidden by default.
- [ ] Candidate resources hidden by default.
- [ ] Badges show type/authority/verification/access.
- [ ] Rationale shown.
- [ ] Page/chapter/section refs shown where available.
- [ ] Local/online distinction visible.

## Verification checklist

- [ ] Accepted resource has title.
- [ ] Accepted resource has type.
- [ ] Accepted resource has authority.
- [ ] Accepted resource has access type.
- [ ] Accepted external source has URL/DOI/identifier.
- [ ] Accepted local source has path/hash.
- [ ] Broken external links not accepted.
- [ ] Missing local files not accepted.
- [ ] Duplicate DOI resources detected.
- [ ] Duplicate ISBN resources detected.
- [ ] Duplicate canonical URL resources detected.
- [ ] Duplicate local file hash resources detected.
- [ ] Score values constrained to 0..1.
- [ ] Rationale required for accepted links.

## Rule node checklist

- [ ] Rule node has accepted source.
- [ ] Rule source is high-authority or explicitly marked as lower-confidence guidance.
- [ ] Jurisdiction/context present when code-like.
- [ ] Edition/year captured when relevant.
- [ ] Relationship type is `governs` or appropriate equivalent.
- [ ] Human review recommended for compliance-critical rules.
- [ ] UI warning appears for jurisdiction-sensitive rule.

## Procedure node checklist

- [ ] Procedure node has source that actually describes procedure/method.
- [ ] Lifecycle phase present if supported.
- [ ] Inputs/outputs present if supported.
- [ ] Relationship type is `provides_procedure` or equivalent.

## Evidence node checklist

- [ ] Evidence node has evidence-bearing source.
- [ ] DOI/stable ID captured where available.
- [ ] Source is academic/professional/report/local evidence, not generic webpage.
- [ ] Claim summary present.
- [ ] Limitations/caveats present if known.

## Document node checklist

- [ ] Document node corresponds to Resource record.
- [ ] Title present.
- [ ] Author/organization/publisher present where available.
- [ ] Year/edition present where available.
- [ ] Identifier/local hash/canonical URL present.
- [ ] Access/copyright notes present.
- [ ] Linked concepts/rules/procedures/evidence present.

## Kimi review checklist

- [ ] Kimi reviewed at least one candidate batch.
- [ ] Kimi decisions logged.
- [ ] Accepted Kimi suggestions implemented or documented.
- [ ] Rejected Kimi suggestions documented with reason.
- [ ] Kimi-rejected candidates not accepted.
- [ ] Kimi flagged jurisdiction concerns where applicable.

## Metrics checklist

- [ ] Total resources reported.
- [ ] Total links reported.
- [ ] Links by status reported.
- [ ] Resources by type reported.
- [ ] Resources by authority reported.
- [ ] Coverage by eligible node type reported.
- [ ] High-priority node coverage reported.
- [ ] Duplicate/broken source counts reported.
- [ ] Kimi/human review counts reported.
- [ ] Quality score reported.

## Final acceptance

The implementation is acceptable when validation passes, sidebar works, at least a pilot set of high-priority nodes has accepted resources, no accepted source is obviously broken or placeholder, Rule nodes are not trusted without sources/context, Kimi review is integrated into the loop, and remaining gaps are documented.
