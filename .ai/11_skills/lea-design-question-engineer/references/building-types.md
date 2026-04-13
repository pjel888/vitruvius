# Building Types Reference — ALE ADSP

Complete building type catalog for generating exam-grade ADSP scenarios. Every building type the ALE tests, its spatial DNA, zone classification, and the traps specific to each type.

**Source:** ALE Syllabus — Architectural Design and Site Planning; PD 1096 Occupancy Classifications; actual exam problems (2009–2025).

---

## Table of Contents
1. Category A: Residential (lines 20–120)
2. Category B: Commercial & Business (lines 125–210)
3. Category C: Industrial & Agricultural (lines 215–280)
4. Category D: Public & Government / Institutional (lines 285–370)
5. Category E: Transportation & Service / UTS (lines 375–440)
6. Category F: Complex Projects (lines 445–490)
7. Exam Frequency Analysis (lines 495–530)
8. Scenario Generation Guide by Type (lines 535–600)

---

## 1. Category A: Residential

### A1. Single-Family Residence (R-1)
**Zone:** R-1 (Low Density Residential)
**Typical lot:** 800–1,500 sqm through lot or inside lot
**Floors:** 1–3 storeys (BHL: 10m)
**PSO:** 50% inside / 55% corner

**Spatial DNA:** The program revolves around the family's daily life — public zone (living, dining, kitchen), private zone (bedrooms, T&B), service zone (maid's room, laundry, carport). The client's profession often introduces a special room (office library, home studio).

**Exam brief patterns:**
- Client description establishes family size and lifestyle → determines bedroom count and special spaces
- Features list gives exact areas per room in sqm
- Carport for X cars → vehicular access and driveway computation
- "Observe proper setbacks" = standard setback table applies
- Lot orientation and RROW position given

**Type-specific traps:**
- **Firewall in R-1:** R-1 zones do not allow firewalls abutting property lines. If the brief says "firewall," the correct interpretation is "perimeter wall." Students who compute setback = 0 on the firewall side get the AMBF wrong.
- **Through lot dual frontage:** A through lot has RROW on two sides → two front setbacks, which significantly reduces buildable depth.
- **Custom setback for carport:** Client may request one side setback increased to 6m for carport access → changes AMBF from setback computation.

**Tested since 2009:** Lawyer's House (R-1), various custom residences

---

### A2. Multi-Family Housing — Quadruplex / Rowhouse (R-2)
**Zone:** R-2 (Medium Density)
**Typical lot:** 1,500–3,000 sqm
**Floors:** 1–2 storeys (BHL: 15m)
**PSO:** 65% inside / 70% corner

**Spatial DNA:** Repetitive modular units sharing party walls. The lot is subdivided into equal divisions. Common firewalls between units. Court/patio between groups of 4 units. Each unit is typically 100–150 sqm with identical programs.

**Type-specific traps:**
- **Lot subdivision math:** Total lot ÷ number of units = area per unit. Students miss that the division must account for shared courts and common areas.
- **Court minimum width:** NBCP prescribes minimum court dimensions for quadruplexes (1.50m). Students confuse this with corridor width.
- **Firewall allowed:** R-2 allows common firewalls between units, unlike R-1.

**Tested since 2009:** Quadruplex for Executive Employees

---

### A3. Condominium — Low/Mid-Rise (R-3 to R-4)
**Zone:** R-3 (High Density) or R-4 (Maximum Density)
**Typical lot:** 800–2,000 sqm
**Floors:** 4–5 storeys (BHL: 15m)
**PSO:** R-3: 70% inside / R-4: 80% inside

**Spatial DNA:** Stacked residential units served by a central corridor, stairs, and fire escapes at both ends. Roof deck often includes party area. Parking at front or basement. Design objective often: "maximize profit" → maximize number of saleable units within code constraints.

**Type-specific traps:**
- **"Maximize profit" directive:** This means less floor plate = more units = more revenue. Students sometimes interpret this as "build the biggest building possible."
- **Roof deck party area:** If the roof deck has a 200sqm party area, it counts as a floor in TGFA.
- **Corridor width:** 2m wide corridor with fire escape at both ends — standard for residential condos.
- **Laundry/drying cages:** Small areas (3 sqm each) with minimum dimension 1.20m — tests dimensional awareness.

**Tested since 2009:** R-3 Condominium (4-storey), various

---

### A4. Condominium — High-Rise (R-5)
**Zone:** R-5 (MRB/HRB)
**Typical lot:** 1,000–3,000 sqm
**Floors:** 8–20+ storeys (BHL: 48m–180m)
**PSO:** 70% inside / 75% corner

**Spatial DNA:** Tower on a podium. Open court as focal point. Basement parking (2–3 levels). Elevator computation becomes relevant (rule of thumb: 1 elevator per 80 units). Mix of unit sizes per floor. Sidewalk and RROW interface.

**Type-specific traps:**
- **Open court in the middle:** Reduces buildable footprint — students forget to subtract court area from AMBF.
- **Basement parking in TGFA:** Two basement levels still count in TGFA computation.
- **FLAR for R-5:** Range is 3.60–9.00, much higher than R-1 to R-3. Students use wrong FLAR.
- **Elevator ratio question:** 88 units ÷ 80 = 1.1 → minimum 2 elevators.

**Tested since 2009:** R-5 Condominium (12-storey)

---

## 2. Category B: Commercial & Business

### B1. Office Building / Office Condominium (C-2 to C-3)
**Zone:** C-2 or C-3
**Typical lot:** 1,000–2,000 sqm
**Floors:** 5–8+ storeys
**PSO:** C-2: 75% / C-3: 80%

**Spatial DNA:** Ground floor = commercial tenant (bank, retail) + lobby/ramp access. Upper floors = repetitive office units with common toilets per floor. Basement parking (multi-level). Mechanical/electrical rooms tucked under ramp. The building is essentially a revenue machine — every sqm of leasable area matters.

**Type-specific traps:**
- **Ground floor mixed use:** Bank at ground floor + office above = questions about specific area allocations.
- **3-level basement with ramp:** Ramp computation and parking slot count across multiple basement floors.
- **Creek at rear:** Easement from creek reduces usable lot area — students forget to deduct.
- **FLAR for C-3:** Range is 9.00–34.00 — dramatically different from residential. Students use wrong range.

**Tested since 2009:** Medium-Rise Office Condominium (C-3, 8-storey)

---

### B2. Restaurant / Food Service (C-1 to C-2)
**Zone:** C-1 or C-2
**Typical lot:** 2,000–5,000 sqm
**Floors:** 1–2 storeys

**Spatial DNA:** Front = parking, sidewalk, outdoor dining. Middle = indoor dining (continuous strip). Rear = individual enclosed kitchens. Driveways wrap around the building on sides and rear. Grease trap required for kitchen drainage.

**Type-specific traps:**
- **8% slope:** Much steeper than typical 2–3%. Significantly affects elevation computations.
- **Parking exceeds NBC minimum:** Brief says "for greater market acceptance, parking should EXCEED NBC requirements" — changes the computation target.
- **Kitchen estimating questions:** Tile count, CHB partition count, concrete volume, paint coverage — the restaurant type generates heavy estimating question sets.
- **Occupant load for commercial kitchens:** 18.60 sqm/person (not the dining area rate).

**Tested since 2009:** Restaurant Plaza (C-2, 8% slope)

---

### B3. Mixed-Use / Hotel / Market
**Zone:** C-1 to C-3
Not heavily represented in known exam sets but listed in syllabus. Generate scenarios with commercial ground floor + residential/office above.

---

## 3. Category C: Industrial & Agricultural

### C1. Car Repair Shop / Small-Scale Industrial (I-1)
**Zone:** I-1 (Light Industrial)
**Typical lot:** 2,000–3,000 sqm
**Floors:** 1–2 storeys (BHL: 15m)
**PSO:** 70% inside

**Spatial DNA:** Two wings separated by an unroofed driveway. Each wing has 3 divisions of equal area. Reception/parking → work area → storage/rest. The driveway must accommodate vehicle turning. The program is defined by the number of cars the facility must handle simultaneously.

**Type-specific traps:**
- **Building Official prescribed setback:** The brief states a specific front setback (e.g., 6.0m) prescribed by the Building Official — this overrides the table value.
- **Actual vs. allowable PSO:** The building footprint (two wings + driveway) may produce a PSO different from the table maximum.
- **"Which PSO should govern?"** — The actual PSO if it's lower, or the table maximum if the actual exceeds it.
- **Car accommodation requirement:** "Must accommodate 18 cars at any given time" — tests space planning, not just code compliance.

**Tested since 2009:** Car Repair Shop (I-1)

---

### C2. Large-Scale Industrial / Manufacturing (I-2, I-3)
Listed in syllabus but less common in known exam sets. Generate with industrial park context, larger lots, heavier structural questions.

---

## 4. Category D: Public & Government / Institutional

### D1. Government Building (GI)
**Zone:** GI (Government/Institutional)
**Typical lot:** 1,000–2,000 sqm
**Floors:** 3–5 storeys (BHL: 15m)
**PSO:** 50% inside / 55% corner

**Spatial DNA:** Lobby + main hall + branch offices + service areas. The brief specifies percentage allocations of the AMBF (e.g., lobby = 20%, main hall = 67%, service = remainder). Open parking at one side, often specified as percentage of TLA. Specific directional placements (e.g., "parking at the western side").

**Type-specific traps:**
- **BHL vs. stated floors:** The exam historically gave 7-storey government building, but BHL for GI is 15m (5 floors). NBC prevails. Students who accept the stated 7 floors get every computation wrong.
- **Parking as % of TLA:** "Open parking shall comprise 53% of the TLA" — this is a huge constraint that leaves very little buildable area, changing the AMBF computation.
- **Low PSO:** GI has only 50% PSO (same as R-1) — much lower than commercial. Students who assume higher PSO oversize the building.

**Tested since 2009:** 5-Storey Government Building (GI), City Council Hall (GI corner lot)

---

### D2. City Council Hall / Legislative Building (GI Corner Lot)
**Zone:** GI
**Typical lot:** 1,000–1,500 sqm corner lot
**Floors:** 3–5 storeys (BHL: 15m)
**PSO:** 55% corner

**Spatial DNA:** Specific civic program — councilor offices (14), gallery (capacity-driven), main hall at a specific corner (50% of AMBF), lounge (25% of AMBF), hearing room, lobby (10%). The corner lot adds a second RROW interface with potentially different RROW widths.

**Type-specific traps:**
- **Corner lot with two different RROW widths:** 20m RROW on front, 15m RROW on north side → different sidewalk and setback requirements per side.
- **Percentage allocations from AMBF:** Students who compute percentages from TLA or GFA instead of AMBF get wrong areas.
- **Gallery capacity:** "Accommodate 40 persons" → tests occupant load calculations.

**Tested since 2009:** City Council Hall (GI corner lot)

---

### D3. School / Hospital / Religious / Recreational
Listed in syllabus. Generate with institutional zone parameters, specific occupancy loads, and accessibility requirements.

---

## 5. Category E: Transportation & Service / UTS

### E1. Bus Terminal (UTS)
**Zone:** UTS (Utilities/Transportation/Services)
**Typical lot:** 3,000–6,000 sqm
**Floors:** 1–2 storeys (BHL: 15m)
**PSO:** 60% inside

**Spatial DNA:** Large open bus parking area (the dominant footprint), waiting area (capacity-driven), rentable lockers, food court, restaurant, maintenance shed. Abutting firewall on one side. The bus parking area alone can be 3,000+ sqm.

**Type-specific traps:**
- **Bus parking not counted as "building":** The open-air bus parking (60m × 50m) is not a roofed structure — does it count in PSO? This distinction tests understanding of PSO definition.
- **Abutting firewall:** Reduces setback to 0 on that side — changes AMBF.
- **Tile procurement question:** "How many boxes must the contractor procure?" — tests material estimation with commercial packaging (tiles per box).
- **"Berm" definition question:** Tests vocabulary knowledge mid-scenario.

**Tested since 2009:** Bus Terminal with Firewall (UTS)

---

### E2. Parking Building (UTS)
**Zone:** UTS
**Typical lot:** 3,000–6,000 sqm
**Floors:** 3–5 storeys

**Spatial DNA:** Multi-storey structure designed to accommodate X cars per floor. Building footprint given as dimensions (70m × 36m). Ramps at specific locations. The building footprint is smaller than the lot — the "actual" AMBF is less than the "allowable."

**Type-specific traps:**
- **"Depth of 50m" is NOT frontage:** Students confuse "depth" with "frontage." The frontage is derived from TLA ÷ depth (or vice versa).
- **Ramp location:** "Ramps located 20m from both sides" — spatial planning question.
- **Actual PSO ≠ allowable PSO:** Given building footprint (70m × 36m = 2,520 sqm) on a 5,350 sqm lot → actual PSO = 47%. Allowable might be 60%. The lower governs.

**Tested since 2009:** Parking Building (UTS, 3-storey)

---

## 6. Category F: Complex Projects

Multi-building combinations on a single site. These appear as the hardest scenarios in the exam and involve master planning, site circulation, and multiple building type codes applied to a single lot.

Not heavily represented in known exam problem sets but listed in the syllabus. Generate by combining two building types on one site (e.g., commercial podium + residential tower, or campus with multiple institutional buildings).

---

## 7. Exam Frequency Analysis

Based on actual exam problems documented from 2009–2024:

| Building Type | Frequency | Difficulty Level |
|---|---|---|
| Single-family Residence (R-1) | Very High | Foundational |
| Condominium (R-3 to R-5) | Very High | Intermediate to Advanced |
| Quadruplex/Rowhouse (R-2) | Medium | Foundational to Intermediate |
| Office Condominium (C-3) | High | Advanced |
| Restaurant/Commercial (C-2) | Medium | Advanced (estimating-heavy) |
| Government Building (GI) | High | Intermediate (BHL trap) |
| Bus Terminal (UTS) | Medium | Intermediate |
| Parking Building (UTS) | Medium | Intermediate |
| Industrial (I-1) | Medium | Intermediate |
| Condominium Interiors | Low-Medium | Interiors-focused |
| Complex/Multi-building | Low | Advanced |

**Strategic generation priority:** Residential (R-1 through R-5) and Government (GI) scenarios should make up ~60% of question sets. Commercial (C-2/C-3) and Transportation (UTS) should make up ~30%. Industrial and Complex for the remaining ~10%.

---

## 8. Scenario Generation Guide by Type

When generating a new scenario for a specific building type:

### Step 1: Select Parameters
- Choose zone classification
- Choose lot type (inside, corner, through, end)
- Set TLA (within realistic range for the type)
- Set frontage dimension
- Set slope percentage (1.5%–8%) and direction
- Set RROW width (10m–40m)
- Choose number of floors (verify against BHL)

### Step 2: Design the Building Program
- Define the primary spaces and their areas/percentages
- Include at least one capacity-based requirement (seats, cars, persons)
- Include at least one directional placement ("lobby at the northwest corner")
- Include at least one percentage allocation from AMBF

### Step 3: Embed the Traps
- Include at least 1 trap per scenario that tests actual vs. allowable
- Include at least 1 trap per scenario that tests a common misconception for the type
- For advanced scenarios: include a BHL conflict or an easement deduction

### Step 4: Compute the Full Solution BEFORE Writing Questions
- Run the entire DC chain from TLA to TGFA
- Verify every number resolves to exactly one correct answer
- Document every step — this becomes the answer key

### Step 5: Write Questions Following the Mandatory Sequence
- DC questions first (8–12)
- SP questions next (2–4)
- ZN / BD / SC / AI / ES / PK interspersed (remaining)
- Engineer distractors from the named error patterns
