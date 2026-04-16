# Human Inbox — Current Pending Decisions

Edit this file only.
Do not create new files.
Do not add sections.
Replace placeholder text only after the `YOUR_*` labels and the reviewer/status fields.
The computer will fill the timestamp automatically.

---

## Packet: ra9514-relationship-admission-2026-04-16
STATUS: answered
REVIEWER: Philip Lewis
OVERALL_NOTES: <optional summary of your thinking>
MACHINE_INTENT: I am deciding whether these 2 staged RA-9514 relationships should be admitted into the official scoped graph or kept out because they may be misleading.

### Item ra9514-suspect-1
HUMAN_READABLE_QUESTION: Does this evidence really show that the RA-9514 Fire Code IRR is governing the concept of yards, or is this a bad match that should stay out?
RELATIONSHIP_ID: rel-irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines-governs-concept-yards
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: The evidence snippet appears to discuss storage areas and automatic extinguishing rather than a clear governing statement about `yards`.
WHAT_APPROVE_MEANS: This relationship will be admitted into the official dataset manifest and included in future official scoped graph builds.
WHAT_REJECT_MEANS: This relationship will stay out of the official manifest and remain only as a rejected/staged artifact.
EVIDENCE_FILE: 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514-v2/relationships/rel-irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines-governs-concept-yards.md
YOUR_DECISION: reject
YOUR_NOTES: The relationship is not supported by the nature of RA 9514 IRR content. The Fire Code focuses on fire safety systems, hazardous storage, suppression, and life safety requirements, not zoning concepts like “yards” in a governing sense.

### Item ra9514-suspect-2
HUMAN_READABLE_QUESTION: Does this evidence really support the idea that means of egress requires occupancy classification here, or is that too abstract / indirect and should stay out?
RELATIONSHIP_ID: rel-concept-means-of-egress-requires-concept-occupancy-classification
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: The evidence may be too indirect and the concept-to-concept abstraction may be overreaching for this source slice.
WHAT_APPROVE_MEANS: This relationship will be admitted into the official dataset manifest and included in future official scoped graph builds.
WHAT_REJECT_MEANS: This relationship will stay out of the official manifest and remain only as a rejected/staged artifact.
EVIDENCE_FILE: 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514-v2/relationships/rel-concept-means-of-egress-requires-concept-occupancy-classification.md
YOUR_DECISION: defer
YOUR_NOTES: This is structurally plausible but currently under-evidenced.

There is a real-world dependency:

Means of egress design varies by occupancy classification (capacity, hazard level, exit widths, travel distance).
RA 9514 clearly defines both concepts and ties them operationally (egress rules depend on occupancy type) .

However, the relationship as stated (“requires”) is too strong unless explicitly codified.

Root issue:

Likely true at a system level
Not proven at a textual clause level

What’s needed to approve:

A clause explicitly linking egress requirements to occupancy classification (not just both existing in the same framework)

Conclusion:

Not wrong
Not yet provable
→ Keep out of official graph until stronger evidence exists
