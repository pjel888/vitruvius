---
name: extract-magic-strings
description: Extracts magic strings, hardcoded routes, status enums, and config into centralized constants. Use when refactoring for DRY, adding new routes, or consolidating string/enum usage in Cerebro.
---

# Extract Magic Strings

## When to Use

- Refactoring for DRY
- Adding or changing routes
- Consolidating status enums or config values
- Before introducing a new string literal that may be reused

## Instructions

### 1. Routes

- Use `src/lib/routes.ts` (primary) or `src/lib/constants/routes.ts` (additional feature routes).
- Define: `PUBLIC_PATHS`, `LOGIN_PATH`, `DASHBOARD_PATH`, `SETTINGS_PATH`, `QUIZ_PATH`, `QUIZ_SESSION_PATH(id)`, `SESSIONS_PATH`, `REVIEW_PATH`, `LIBRARY_PATH`, and other app routes.
- Replace: `redirect("/login")`, `redirect("/dashboard")`, `href="/dashboard/..."`, `pathname === "/..."`, `router.push(...)` with constants (e.g. `ROUTES.LOGIN`, `ROUTES.DASHBOARD`).
- Middleware, layout, pages, and server actions must all use the same route constants for auth redirects.

### 2. Status and enums

- Use types from `src/types/` (e.g. `src/types/app.ts` with `SessionStatus`, `OnboardingStep`, or domain-specific types in `src/types/dashboard.ts`, `src/types/quiz-config.ts`, etc.).
- Add const arrays or utilities in `src/lib/constants/` (e.g. `src/lib/constants/mastery.ts`, `src/lib/constants/testing-modes.ts`) for iteration/validation.
- Do not use ad-hoc string literals like `"in_progress"` or `"completed"` in multiple places; reference the type or constant.

### 3. Config

- Add feature-specific constants to `src/lib/constants/` directory (e.g. `src/lib/constants/testing-modes.ts`, `src/lib/constants/readiness.ts`) for feature flags, limits, and domain-specific config.
- Use `src/lib/utils/constants.ts` for app-wide utilities.
- Keep one canonical definition per value.

### 4. Finding candidates

Grep patterns:

- `redirect\(['\"]/`
- `href=['\"]/`
- `pathname === ['\"]/`
- `['\"]in_progress['\"]`, `['\"]completed['\"]`

Replace usages; keep one canonical definition per value.
