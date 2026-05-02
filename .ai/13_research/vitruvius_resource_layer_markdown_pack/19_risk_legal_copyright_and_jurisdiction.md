# 19 — Risk, Legal, Copyright, and Jurisdiction Notes

## Important disclaimer for implementation

The resource layer should help users find references. It should not present itself as legal, code-compliance, or professional engineering advice.

AEC references often depend on jurisdiction, project type, authority having jurisdiction, adopted code edition, contract documents, professional judgment, site conditions, local standards, and owner requirements.

## Copyright risks

Do not copy long excerpts from copyrighted books or standards, redistribute PDFs without rights, link pirated copies as accepted sources, upload restricted local PDFs to external APIs without permission, expose local restricted files publicly, or store large chunks of copyrighted text for display.

Safer practices:

- store metadata,
- store page/chapter references,
- store very short previews only where allowed,
- link to official landing pages,
- note access restrictions,
- keep local files local,
- use human review for ambiguous copies.

## Standards and codes

Standards/codes may be paywalled, copyrighted, adopted differently by jurisdiction, edition-specific, modified by local amendments, or not universally applicable.

For Rule nodes:

- store jurisdiction/context,
- store edition/year,
- distinguish binding code from professional guidance,
- avoid copying standard text,
- link official landing pages where possible,
- use human review for trusted status.

## Jurisdiction-sensitive examples

Always include context for accessibility route requirements, fire separation rules, egress width/capacity, structural load criteria, wind/seismic design criteria, flood design elevation, stormwater discharge rules, parking/access requirements, and building code provisions.

## Source access types

Use clear access states: `open_access`, `public_web`, `preview_only`, `paywalled`, `local_only`, `restricted`, and `unknown`.

## Local file risks

If Vitruvius is a web app, local file paths can reveal sensitive server structure. Do not expose raw filesystem paths unless safe. Prefer backend resource viewer, sanitized file names, permission checks, local resource badges, and local-only access notes.

## External API risks

External APIs may change rate limits, require keys, return noisy metadata, contain duplicates, return outdated editions, expose preview links only, or have licensing constraints. Always treat API output as candidate data.

## Kimi/AI review risks

Kimi can help, but can also be wrong. Do not treat Kimi as final authority. For high-risk claims, require human review or keep as `needs_review`.

## High-risk node categories

Use stricter review for structural safety, life safety, fire protection, accessibility compliance, legal/code rules, geotechnical/foundation design, flood/seismic/wind hazards, public health, emergency access, and occupational safety.

## Recommended UI caveats

Jurisdiction-sensitive card:

```text
Jurisdiction/context-sensitive. Confirm applicable local code, project requirements, and professional guidance before use.
```

Paywalled/restricted standard:

```text
Official source identified. Full text may require authorized access.
```

AI-reviewed only:

```text
AI-reviewed candidate. Human review recommended for compliance-critical use.
```

## Rejection flags

Reject or require human review if source is an unofficial PDF of a paywalled standard, broken link, mismatched title/identifier, suspicious mirror domain, missing author/organization for high-impact claim, blog used for code/engineering rule, wrong jurisdiction, or product manual used as general design authority.
