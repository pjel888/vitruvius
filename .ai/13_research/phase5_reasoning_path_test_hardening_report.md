# Phase 5 Reasoning Path Test Hardening Report

Date: 2026-05-03T02:45:00+08:00

## Changes to `api/graphReasoningPaths.test.ts`

### 1. Duplicate Base Edge Test Normalization Fix

- Uses `normalizedBaseEdges` instead of raw `baseEdges` for key comparison
- Added regression assertion proving old raw-field assumption was broken

### 2. Phase 5 Gap-Closure Exact Edge Assertions

Added exact edge ID assertions to all 3 gap-closure tests:

| Test | Exact Edge Asserted |
|------|---------------------|
| Structural Engineering → Materials | `source=VTN-DOM-0000029, target=VTN-DOM-0002477, type=INFORMS` |
| Mechanical Systems → Thermal Comfort | `source=VTN-DOM-0000004, target=VTN-DOM-0002510, type=AFFECTS` |
| Fire Protection → Egress | `source=VTN-DOM-0000056, target=VTN-DOM-0000058, type=CONSTRAINS` |
| Fire Protection → Egress (reverse) | `source=VTN-DOM-0000058, target=VTN-DOM-0000056, type=REQUIRES` |

### 3. Drainage Path Hardening

**Before**: `hasOutgoingEdge(drainage, 'DISCHARGES_TO') || hasOutgoingEdge(drainage, 'DRAINS_TO')`

**After**: Asserts **both** edges independently:
- `hasOutgoingEdge(drainage, 'DRAINS_TO')` → true
- `hasOutgoingEdge(drainage, 'DISCHARGES_TO')` → true

Also asserts exact admitted edges:
- `source=VTN-DOM-0000025, target=VTN-DOM-0002899, type=DRAINS_TO`
- `source=VTN-DOM-0000025, target=VTN-DOM-0002896, type=DISCHARGES_TO`

### 4. Underrepresented Family Semantic Assertions

Added semantic checks beyond count thresholds:

| Family | Semantic Check |
|--------|----------------|
| DRAINS_TO | Drainage node (VTN-DOM-0000025) is a source |
| CONNECTS_TO | Rationale mentions "interface" or "connect" |
| REQUIRES | Rationale mentions "require" or "depend" |
| COLLECTS | Rationale mentions "collect" or "convey" |

### 5. Existing Regression Tests Preserved

- No active CROSS_DOMAIN_EQUIVALENT
- Sendai Mediatheque / Toyo Ito HAS_FACET visibility
- Deep/Shallow Foundations distinction
- Building Envelope taxonomy children

## Test Count

- **Before remediation**: 18 tests
- **After remediation**: 18 tests (same count, stronger assertions)
- **All pass**: 18/18
