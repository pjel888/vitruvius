# Development Controls Computation Reference

Complete computation framework for ALE ADSP questions. Every formula, every table value, every decision tree needed to generate and verify DC questions.

**Source:** Rules VII and VIII of the 2004 Revised Implementing Rules and Regulations of PD 1096 (National Building Code of the Philippines, 1977).

---

## Table of Contents
1. Master Formula Chain (lines 15–60)
2. Table VII.G.1 — PSO, ISA, USA, TOSL by Zone (lines 65–150)
3. FLAR Table VII.G.2 (lines 155–210)
4. BHL by Occupancy/Zone (lines 215–260)
5. Setback Requirements — Table VIII (lines 265–350)
6. The Actual vs. Allowable Decision Tree (lines 355–410)
7. GFA Inclusions and Exclusions (lines 415–470)
8. TGFA Computation Rules (lines 475–520)
9. Common Computation Traps (lines 525–580)

---

## 1. Master Formula Chain

These formulas must be computed in this exact order. Each feeds the next.

```
1.  TLA     = Total Lot Area (given — may need easement deduction)
2.  PSO     = Percentage of Site Occupancy (from Table VII.G.1, by zone and lot type)
3.  AMBF    = TLA × PSO (Allowable Maximum Building Footprint)
4.  ISA     = TLA × ISA% (Impervious Surface Area — maximum)
5.  USA     = TLA × USA% (Unpaved Surface Area — minimum)
6.  TOSL    = TLA × TOSL% (Total Open Space within Lot — minimum)
             Or: TOSL = ISA + USA
7.  MACA    = PSO + ISA (Maximum Allowable Construction Area, as %)
             Or: MACA = AMBF + ISA (in sqm terms)
8.  FLAR    = Range from Table VII.G.2 (by zone)
9.  BHL     = From table (by occupancy classification and zone)
10. Floors  = BHL ÷ assumed floor-to-floor height (typically 3.0m)
11. GFA     = AMBF × number of above-grade typical floors (simplified)
             Or: Per actual computation based on floor plate areas
12. TGFA    = AMBF × total number of floors (including applicable levels)
             Or: Sum of all GFA per floor + other counted areas
    Verify: TGFA must be within FLAR × TLA range
```

**Critical relationships:**
- PSO + TOSL = 100% of TLA
- ISA + USA = TOSL
- MACA = PSO + ISA
- TGFA ÷ TLA = actual FLAR (must be within the range from Table VII.G.2)

---

## 2. Table VII.G.1 — PSO, ISA, USA, TOSL by Zone and Lot Type

**RESIDENTIAL ZONES**

| Zone | Lot Type | PSO (max%) | ISA (max%) | USA (min%) | TOSL (min%) |
|---|---|---|---|---|---|
| R-1 (Low Density) | Inside | 50 | 20 | 30 | 50 |
| R-1 | Corner | 55 | 20 | 25 | 45 |
| R-1 | Through | 50 | 20 | 30 | 50 |
| R-1 | End | 55 | 20 | 25 | 45 |
| R-2 (Medium Density) | Inside | 65 | 20 | 15 | 35 |
| R-2 | Corner | 70 | 20 | 10 | 30 |
| R-2 | Through | 65 | 20 | 15 | 35 |
| R-2 | End | 70 | 20 | 10 | 30 |
| R-3 (High Density) | Inside | 70 | 15 | 15 | 30 |
| R-3 | Corner | 75 | 15 | 10 | 25 |
| R-3 | Through | 70 | 15 | 15 | 30 |
| R-3 | End | 75 | 15 | 10 | 25 |
| R-4 (Max Density) | Inside | 80 | 10 | 10 | 20 |
| R-4 | Corner | 85 | 10 | 5 | 15 |
| R-4 | Through | 80 | 10 | 10 | 20 |
| R-4 | End | 85 | 10 | 5 | 15 |
| R-5 (MRB/HRB) | Inside | 70 | 15 | 15 | 30 |
| R-5 | Corner | 75 | 15 | 10 | 25 |
| R-5 | Through | 70 | 15 | 15 | 30 |
| R-5 | End | 75 | 15 | 10 | 25 |

**COMMERCIAL ZONES**

| Zone | Lot Type | PSO (max%) | ISA (max%) | USA (min%) | TOSL (min%) |
|---|---|---|---|---|---|
| C-1 (Low Intensity) | Inside | 70 | 15 | 15 | 30 |
| C-1 | Corner | 75 | 15 | 10 | 25 |
| C-2 (Medium Intensity) | Inside | 75 | 15 | 10 | 25 |
| C-2 | Corner | 80 | 15 | 5 | 20 |
| C-3 (High Intensity) | Inside | 80 | 15 | 5 | 20 |
| C-3 | Corner | 85 | 10 | 5 | 15 |

**INDUSTRIAL ZONES**

| Zone | Lot Type | PSO (max%) | ISA (max%) | USA (min%) | TOSL (min%) |
|---|---|---|---|---|---|
| I-1 (Light Industrial) | Inside | 70 | 20 | 10 | 30 |
| I-1 | Corner | 75 | 15 | 10 | 25 |
| I-2 (Medium Industrial) | Inside | 75 | 15 | 10 | 25 |
| I-2 | Corner | 80 | 10 | 10 | 20 |
| I-3 (Heavy Industrial) | Inside | 70 | 20 | 10 | 30 |

**INSTITUTIONAL / GOVERNMENT (GI)**

| Zone | Lot Type | PSO (max%) | ISA (max%) | USA (min%) | TOSL (min%) |
|---|---|---|---|---|---|
| GI (Institutional) | Inside | 50 | 20 | 30 | 50 |
| GI | Corner | 55 | 20 | 25 | 45 |

**SPECIAL ZONES**

| Zone | Lot Type | PSO (max%) | ISA (max%) | USA (min%) | TOSL (min%) |
|---|---|---|---|---|---|
| UTS (Utilities/Transportation/Services) | Inside | 60 | 30 | 10 | 40 |
| UTS | Corner | 65 | 25 | 10 | 35 |
| Parks/Open Space | Inside | 10 | 10 | 80 | 90 |
| Cemetery | Inside | 15 | 15 | 70 | 85 |

**IMPORTANT:** These values are from the 2004 Revised IRR. When generating questions, always verify against the specific table. Values shown are approximate composites — always cross-reference the specific lot type and zone. Some local zoning ordinances may override national standards; in exam context, NBC values govern unless the problem explicitly states a local zoning ordinance override.

---

## 3. FLAR Table VII.G.2

The FLAR gives the allowable ratio of TGFA to TLA. It determines the maximum building volume allowed.

| Zone | FLAR Range |
|---|---|
| R-1 | 1.00 – 1.50 |
| R-2 | 1.50 – 2.50 |
| R-3 | 2.00 – 3.00 |
| R-4 | 3.00 – 5.00 |
| R-5 | 3.60 – 9.00 (or higher for MRB/HRB) |
| C-1 | 2.00 – 3.00 |
| C-2 | 2.00 – 3.00 |
| C-3 | 9.00 – 34.00 |
| I-1 | 1.50 – 2.50 |
| I-2 | 2.00 – 3.00 |
| GI | 1.50 – 2.50 |
| UTS | 2.00 – 3.00 |

**How to use FLAR in questions:**
- "What is the Range of the FLAR of the Project?" → Direct table lookup
- "What is the RANGING value of the GFA?" → GFA = FLAR_low × TLA to FLAR_high × TLA
- TGFA verification: Actual TGFA must fall within FLAR × TLA range

---

## 4. BHL by Occupancy/Zone

Building Height Limit determines the maximum number of floors.

| Occupancy Classification | BHL |
|---|---|
| R-1 (Single-family residential) | 10.00 m |
| R-2 (Multi-family, low-rise) | 15.00 m |
| R-3 (Multi-family, medium-rise) | 15.00 m |
| R-4 (Multi-family, max density) | Varies by zone |
| R-5 (MRB/HRB) | 48.00 m – 180.00 m (depends on zone) |
| C-1, C-2 | 15.00 m |
| C-3 (CBD) | 48.00 m – 180.00 m |
| I-1, I-2, I-3 | 15.00 m |
| GI (Institutional) | 15.00 m |
| UTS | 15.00 m |

**Floors above established grade:** BHL ÷ floor-to-floor height (assume 3.0m unless stated)
- 10m BHL → 3 floors (3 × 3.0 = 9.0m + parapet)
- 15m BHL → 5 floors (5 × 3.0 = 15.0m)
- 48m BHL → 16 floors
- Some problems state the actual number of floors — verify against BHL

**Critical trap:** The exam has historically given a building height (e.g., "7-storey government building") that EXCEEDS the BHL for the zone. The student must recognize this and use the BHL limit, not the stated floors. As annotated in the actual exam: "ALWAYS CHECK BHL — NBC WILL PREVAIL."

---

## 5. Setback Requirements — Table VIII (Simplified)

Setback requirements vary by occupancy, building height, and lot type. These are the most commonly tested values.

### For Inside Lots (most common in exam)

| Building Height | Front Setback | Side Setback | Rear Setback |
|---|---|---|---|
| Up to 6m (1–2 storeys) | 4.50m | 2.00m | 2.00m |
| Over 6m to 9m | 4.50m | 2.00m | 2.00m |
| Over 9m to 12m | 6.00m | 2.00m | 3.00m |
| Over 12m to 15m | 6.00m | 3.00m | 3.00m |
| Over 15m to 18m | 8.00m | 3.00m | 4.00m |
| Over 18m to 21m | 8.00m | 4.00m | 4.00m |

### For Corner Lots
Corner lots have setbacks on TWO road-facing sides. The second road side uses the side setback value but may be increased.

### For Through Lots
Through lots have TWO front setbacks (one on each road).

### Special Conditions
- When a Building Official specifically prescribes a setback → that value governs over the table
- Firewalls: In R-1 zones, firewalls abutting property lines are NOT allowed. In R-2 and higher, firewalls may be allowed per specific provisions.
- Abutting conditions: If the problem states "abutting firewall at the westside," the setback on that side = 0m for the firewall portion.

### Computing AMBF from Setbacks (when building footprint is not given)
```
Buildable width = Lot width - left setback - right setback
Buildable depth = Lot depth - front setback - rear setback
AMBF (from setbacks) = Buildable width × Buildable depth
```

If this AMBF < TLA × PSO, then the setback-derived AMBF governs (it's more restrictive).
If this AMBF > TLA × PSO, then the PSO-derived AMBF governs.

---

## 6. The Actual vs. Allowable Decision Tree

One of the most tested concepts. The exam frequently asks BOTH the allowable value (from the table) AND the actual value (from the given building), then asks which governs.

```
STEP 1: Compute ALLOWABLE from table
  AMBF (allowable) = TLA × PSO%
  PSO (allowable) = from Table VII.G.1

STEP 2: Compute ACTUAL from the given building
  AMBF (actual) = given building footprint area (e.g., 70m × 36m = 2,520 sqm)
  PSO (actual) = AMBF (actual) ÷ TLA × 100

STEP 3: Which governs?
  For MAXIMUMS (PSO, ISA, AMBF): The LOWER value governs
    → If actual < allowable, actual governs (building is under the limit)
    → If actual > allowable, the building violates the code
  For MINIMUMS (USA, TOSL): The HIGHER value governs
    → If actual > minimum required, actual governs
    → If actual < minimum required, the building violates the code
```

**Exam question pattern:**
1. "What is the maximum allowable PSO?" [from table]
2. "What is the PSO (actual)?" [from given footprint]
3. "Which PSO should govern?" [the lower of the two for maximums; the higher for minimums]

---

## 7. GFA Inclusions and Exclusions

### GFA INCLUDES:
- All covered areas within the external building walls
- Office areas, residential areas, corridors, lobbies
- Mezzanine levels
- Building projections that serve as floors/platforms
- Balconies (if enclosed or covered and directly connected)

### GFA EXCLUDES (the most exam-tested list):
- Covered areas used for parking and driveways
- Areas below grade used exclusively for parking
- Uncovered areas: rooftop ACCU, water tanks, roof decks (if uncovered)
- Fire escapes (if they are dedicated exit stairs and not the primary stairs)

**Critical for TGFA computation:** TGFA includes GFA PLUS all other horizontal surfaces above and below grade that are attached to the building. This includes parking basements, utility rooms, mechanical levels, and roof decks (if they have any covered/enclosed area).

---

## 8. TGFA Computation Rules

```
TGFA = Sum of all floor areas including:
  + GFA of all above-grade floors
  + Basement floor areas (even if used for parking)
  + Roof deck area (if it contains built structures like a party room, pool area)
  + Mezzanine areas

TGFA (simplified) = AMBF × Total number of floors
  Where "total floors" includes all levels above AND below grade
  that have any built area

TGFA (alternative) = FLAR × TLA
  This gives the MAXIMUM ALLOWABLE TGFA
  Actual TGFA must be ≤ this value
```

### TGFA Verification
After computing TGFA, verify:
```
Actual FLAR = TGFA ÷ TLA
This value must fall within the FLAR range from Table VII.G.2
If it exceeds the upper limit → building is too large for the zone
If it falls below the lower limit → building is underbuilt (not a violation, but unusual)
```

---

## 9. Common Computation Traps

These are the errors that generate wrong-answer distractors. Know them intimately.

| Trap | What Goes Wrong | How to Avoid |
|---|---|---|
| **Easement not deducted** | Creek or utility easement reduces usable TLA. Student uses full TLA. | Always check for easement language in the site description |
| **Parking area counted in GFA** | Covered parking is EXCLUDED from GFA but student includes it | Remember: covered parking = GFA exclusion |
| **Roof deck counted/not counted** | Some problems include roof deck in floor count, others don't | Read the brief: if there's a "party area on the roof deck" → count it |
| **Basement in TGFA** | Students forget basements count toward TGFA even if used for parking | TGFA includes ALL levels — above and below grade |
| **Wrong lot depth** | Student confuses "depth of 50m" with frontage | Frontage = dimension facing the RROW; depth = perpendicular to RROW |
| **Corner lot second road** | Student applies inside-lot setbacks to a corner lot, missing the second road | Check lot type carefully — corner lots have two road-facing setbacks |
| **Firewall in R-1** | Brief states "firewall" but R-1 doesn't allow firewalls | Recognize the trap — convert "firewall" to "perimeter wall" |
| **BHL override** | Brief states 7 storeys but BHL for zone is only 15m (5 floors) | Always compute BHL independently — NBC prevails over the brief |
| **Slope × wrong dimension** | Student multiplies slope% by frontage instead of by the dimension in the slope direction | Slope is always toward the RROW — multiply by the dimension running toward the road |
| **PSO zone mismatch** | Student uses R-3 PSO (70%) when the project is actually R-5 (also 70% but with different ISA/USA) | Verify the exact zone — some zones share PSO but differ in ISA/USA |
