# Phase 6K Promotion Preview API Report

**Date:** 2026-05-03
**Status:** Implemented
**Route:** `POST /resources/review/external-candidates/:candidateId/promotion-preview`

---

## Route Handler

```ts
app.post('/resources/review/external-candidates/:candidateId/promotion-preview', (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const registry = loadExternalCandidateRegistry(repoRoot);
    const candidate = registry.candidates.find((cand) => cand.candidateId === candidateId);
    if (!candidate) {
      return c.json({ error: { message: `Candidate not found: ${candidateId}` } }, 404);
    }
    const preview = buildExternalCandidatePromotionPreview(candidate);
    return c.json(preview);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});
```

## Safety Checklist

| Check | Status |
|---|---|
| requireLocalDevAdmin gate | ✅ Yes |
| Read-only | ✅ Yes — no writes |
| No registry mutation | ✅ Yes |
| No transaction manifest | ✅ Yes |
| No resource creation | ✅ Yes |
| No nodeResourceLink creation | ✅ Yes |
| No review decision creation | ✅ Yes |
| No external verification | ✅ Yes |
| No graph/canonical mutation | ✅ Yes |
| No learner exposure | ✅ Yes |

## Response Codes

| Code | Condition |
|---|---|
| 200 | Preview returned successfully |
| 404 | Candidate not found |
| 4xx | Gate closed or invalid input |

## No Promotion Apply Route

No `POST /resources/review/external-candidates/:candidateId/promotion-apply` route exists.
Promotion apply remains unimplemented and unauthorized.
