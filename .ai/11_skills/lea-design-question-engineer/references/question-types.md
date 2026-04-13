# Question Types Reference — ALE ADSP

Complete specification for all 8 ADSP question types. Every question you write must belong to exactly one type. This document provides the stem patterns, answer structures, distractor engineering, and examples for each.

---

## Table of Contents
1. DC — Development Controls (lines 20–150)
2. SP — Site Planning (lines 155–230)
3. ZN — Space Planning / Zoning (lines 235–300)
4. BD — Building Design Knowledge (lines 305–370)
5. SC — Structural Applied to Design (lines 375–430)
6. AI — Architectural Interiors (lines 435–510)
7. ES — Estimating (lines 515–590)
8. PK — Parking & Vehicular (lines 595–650)

---

## 1. DC — Development Controls

The computational backbone of every ADSP scenario. These questions test whether the candidate can derive allowable building parameters from a given site using Rules VII and VIII of the 2004 Revised IRR.

### Mandatory DC Question Sequence
DC questions MUST appear in this order within a scenario because each computation feeds the next:

1. **AMBF** (Allowable Maximum Building Footprint) — always first
2. **PSO** (Percentage of Site Occupancy) — maximum allowable, then actual
3. **ISA** (Impervious Surface Area) — maximum allowable
4. **USA** (Unpaved Surface Area) — minimum required
5. **TOSL** (Total Open Space within Lot) — minimum required
6. **MACA** (Maximum Allowable Construction Area)
7. **FLAR** (Floor-to-Lot Area Ratio) — range from table
8. **BHL** (Building Height Limit)
9. **Floors above established grade** — derived from BHL
10. **GFA** (Gross Floor Area) — maximum allowable, then actual
11. **TGFA** (Total Gross Floor Area)

### Stem Patterns

**Direct computation:**
- "What is the AMBF of the Project?"
- "What is the maximum allowable PSO of the Project?"
- "What is the TGFA?"

**Actual vs. allowable:**
- "What is the PSO (actual)?"
- "What is the AMBF (actual)?" [when building footprint is given and is less than allowable]
- "Which PSO should govern?" [the lower of actual or allowable]

**Definitional:**
- "Under Rule VII of the Revised IRR of the 1977 NBCP, what is meant by PSO?"
- "Under Rule VII of the Revised IRR of the 1977 NBCP, what is meant by AMBF?"

**Ranging:**
- "What is the Range of the FLAR of the Project?"
- "What is the RANGING value of the GFA?"

### Answer Format
All DC answers are numerical with units. Format: `X sqm`, `X%`, `Xm`, or `X.XX to X.XX`.

### Distractor Engineering for DC Questions

| Error Pattern | Example |
|---|---|
| Wrong PSO from adjacent zone row | Question: R-2 inside lot (PSO = 70%). Distractor uses R-1 value (50%) or R-3 value (80%) |
| Forgot easement deduction | TLA = 1,350 sqm but lot has a 100sqm creek easement. Student uses 1,350 instead of 1,250 |
| Actual vs. allowable confusion | AMBF (allowable) = 680 sqm, but building footprint given as 453.60 sqm. Wrong answer uses 680 as "actual" |
| FLAR range from wrong table row | Used the FLAR for C-2 when the project is C-3 |
| BHL for wrong occupancy | Applied residential BHL (10m) to a government building (should be 15m) |
| Depth mistaken for frontage | Given: "frontage 40m" and "depth 50m" — student swaps them in setback computation |
| GFA includes excluded areas | Student includes covered parking in GFA when it should be excluded |
| TGFA floor count wrong | Student counts only above-grade floors, missing the roof deck or basement |

### Example DC Question

```
163. What is the AMBF of the Project?
  a. 680 sqm       [CORRECT: TLA × PSO = 1,360 × 50% = 680]
  b. 972 sqm        [Error: used 1,360 × 70% — wrong PSO for institutional]
  c. 816 sqm        [Error: used 1,360 × 60% — PSO for different zone]
  d. 952 sqm        [Error: used 1,360 × 70% then subtracted something]
```

---

## 2. SP — Site Planning

Tests the candidate's ability to read site conditions and apply setback, slope, and access requirements.

### Stem Patterns
- "What is the minimum side setback required for the project?"
- "What is the minimum rear setback as per NBCP?"
- "What is the depth of the lot?" [derived from TLA and frontage]
- "What is the difference in height between the highest and lowest points of the lot?" [slope × depth or length]
- "Which shall be considered as the established grade elevation when measuring building height if the edges of the building footprint running perpendicular to the RROW has a difference in elevation of more than 3.0m?"
- "For the 20-meter wide RROW fronting the property, what is the minimum sidewalk width required by the NBC?"

### Computation Patterns
- **Lot depth:** TLA ÷ frontage = depth
- **Elevation difference:** slope% × lot dimension in direction of slope
- **Established grade:** If elevation difference > 3.0m along building perpendicular to RROW → average of lowest and highest. If ≤ 3.0m → lowest elevation.
- **Sidewalk width:** Fraction of RROW width per NBC table
- **Setback values:** Per Table VIII, varies by occupancy classification, building height, and lot type (inside/corner/through/end)

### Distractor Engineering for SP Questions
- Apply inside-lot setbacks to a corner lot (corner lots have additional setback on the second road side)
- Confuse front setback with side setback
- Use slope percentage incorrectly (multiply by wrong dimension)
- Apply the wrong occupancy classification for setback lookup
- Ignore the zoning ordinance override when a Building Official has specifically prescribed a setback

---

## 3. ZN — Space Planning / Zoning

Tests spatial allocation, adjacency relationships, and program distribution within the building footprint.

### Stem Patterns
- "The lobby shall occupy 20% of the AMBF. What is the lobby area?"
- "If the Councilor's Main Hall occupies 50% of the AMBF, what is its area?"
- "An occupied space between building lines and lot lines other than a yard; free, open and unobstructed by appendages from the ground upward. What is this?" [Court]
- "What is the maximum building footprint resulting from the minimum required setbacks and the open court in the middle?"
- "Under the NBCP, what is the minimum width of the court of a Quadruplex?"

### Answer Format
Area values in sqm, or identification of architectural elements/spaces.

### Distractor Engineering for ZN Questions
- Calculate percentage from TLA instead of AMBF
- Calculate percentage from GFA instead of AMBF
- Confuse "court" with "atrium" or "dispersal area"
- Apply residential court minimums to a commercial building

---

## 4. BD — Building Design Knowledge

Tests knowledge of code provisions, occupancy classifications, design standards, and building type-specific requirements.

### Stem Patterns
- "Which Rule under the 2004 Revised IRR of the 1977 NBCP prescribes that for each type of building use/occupancy, the TGFA shall be the product of the BHL and the AMBF?" [Rule VII]
- "Which Section under Rule VII of the 2004 Revised IRR deals with parking?" [Sec. 707]
- "How many floors above established grade is allowed for this kind of development?"
- "A common rule of thumb in determining the estimated number of elevators during the initial design process for the design of condominiums." [1:80 units or 1:100 units]
- "According to BP 344, what is the ideal height of grab bars in an accessible toilet stall?"
- "According to RA 9514, what is the maximum riser height for new stairs?"

### Distractor Engineering for BD Questions
- Adjacent Rule number (Rule VI instead of Rule VII)
- Adjacent section number (Sec. 706 instead of Sec. 707)
- Outdated code values (pre-2024 IRR for BP 344)
- Rule of thumb variations (1:60 vs 1:80 vs 1:100 for elevator ratio)

---

## 5. SC — Structural Applied to Design

Tests structural knowledge as it applies to architectural design decisions — not pure engineering computation, but enough to make informed design choices.

### Stem Patterns
- "If incremental setback is applied on two sides of the building, what is the floor area of the 8th Floor?"
- "Compute the roof area for a 2-meter high gable roof mounted on the deck (9th floor level) enclosed by parapet."
- "Compute the weight of steel angle to be used for the truss with vertical webs at 1.0m intervals."
- "What is the weight of the concrete?" [given wall dimensions and concrete density 2400 kg/cu.m]
- "Which of the following structural elements can be erected along a side or rear property line?"

### Distractor Engineering for SC Questions
- Wrong density value for concrete (2300 vs 2400 kg/cu.m)
- Forgot to account for incremental setback reducing floor area
- Computed gable roof as flat roof
- Wrong steel section weight per linear meter

---

## 6. AI — Architectural Interiors

Tests furniture dimensions, finish material knowledge, interior spatial standards, and architectural interior classifications.

### Stem Patterns
- "What is the dimension of a twin size bed?" [0.90m × 1.90m or 38" × 76"]
- "Ideal size of a Dining Table for 4 persons?" [90 × 90 cm]
- "What is the ideal height of a Dining table?" [0.75m]
- "For work kitchens, what is the optimum counter height?" [850–900mm]
- "Which of the following is NOT part of the Interior?" [Soffit]
- "Which of the following is NOT considered a fixture?" [Wall Hanging]
- "Paint on wall is considered:" [Architectural Interiors]
- "What constitutes the work triangle in a kitchen?" [Refrigerator, cooktop, and sink]
- "Which is NOT part of Architectural Interiors (AI)?" [distinguishing AI from non-AI elements]

### Key Values to Know (frequently tested)
- Twin bed: 99cm × 190cm (or 38" × 76")
- Full/Double bed: 54" × 75"
- Queen bed: 60" × 80"
- King bed: 76" × 80"
- Dining table height: 750mm (0.75m)
- Dining seat height: 450mm
- Work kitchen counter: 850–900mm
- Circular table for 8: 60 inches diameter
- Rectangular table for 10: 750mm × 2400mm
- Comfortable dining chair: 0.50 × 0.50
- Clerical station with side return + 2 visitors: 4.60 sqm
- Clerical station with side return + desktop computer: 3.20 sqm

### Distractor Engineering for AI Questions
- Metric/imperial confusion (0.90m vs 90cm vs 36")
- Adjacent furniture standard (dining height vs counter height)
- Confusing AI with non-AI elements (exterior soffit is NOT interior)
- Work triangle misconceptions (oven vs refrigerator)

---

## 7. ES — Estimating

Tests material quantity computation — tiles, paint, CHB, concrete, lumber, and cost calculation.

### Stem Patterns
- "How many 16" × 16" tiles will be used in the Foyer?"
- "How many Vinyl Tiles will you use for the Service/Maid's Room?"
- "If Cement Boards were used for a 106 sqm office wall partition, how many pieces will you use?"
- "How much paint is needed (using 2 sq.m./gal coverage) to paint the area?"
- "If the partition wall between two units is 8.0m, and the wall height is 3.0m at the end and 6.0m at the middle, how many 6" CHB is needed?"
- "Estimate the quantity of floor tiles required for one kitchen if the owner wants to use 30cm × 30cm ceramic tiles. Provide a 5% allowance for breakage."
- "How much will the tilework cost?" [area × tiles per sqm × cost per tile + labor]
- "At Php 550/bf, how much is 120pcs — 2"×4"×8'?"
- "Estimate the volume of concrete required for the floor slab if the slab will be 125mm thick."

### Computation Patterns
- **Tile count:** Floor area ÷ tile area = number of tiles. Add wastage (usually 5–10%).
- **CHB count:** Wall area ÷ area per CHB (standard 6" CHB: 12.5 pcs/sqm).
- **Paint:** Wall area ÷ coverage rate (sqm/gal) × number of coats.
- **Lumber board feet:** pieces × (thickness" × width" × length') ÷ 12.
- **Concrete volume:** length × width × thickness (all in meters) = cu.m.
- **Cost:** quantity × unit price.

### Distractor Engineering for ES Questions
- Forgot wastage allowance
- Wrong CHB count per sqm (used 4" CHB rate for 6" CHB)
- Area computed wrong (forgot to account for trapezoidal wall shape)
- Used wrong coverage rate for paint
- Board feet formula error
- Used the wrong tile size in computation

---

## 8. PK — Parking & Vehicular

Tests parking slot computation per occupancy type, driveway dimensions, and vehicular access requirements.

### Stem Patterns
- "In order to satisfy the parking provisions required by the NBC, the project may make use of a permanent parking building if the said building is how far from the project?"
- "For deliveries, the owner asked you to provide parking slots for three delivery trucks. What are the minimum dimensions required by the NBC for standard trucks?"
- "What is the minimum required width for a dropped curb that leads to a 1.10m-wide crossing?"
- "How many parking slots are required for the project?" [based on occupancy and GFA]
- "The Architect specified 0.60 × 0.60 Tiles for the Waiting Area. How many boxes must the contractor procure?"

### Key Parking Ratios (PD 1096 IRR)
- Residential condo: 1 slot per unit (or per NBC table)
- Office: 1 slot per 100 sqm GFA
- Commercial/retail: 1 slot per 50–100 sqm GFA (varies)
- Restaurant: 1 slot per specific seating/area
- Market: 1 customer slot per 150 sqm; 1 vendor slot per 300 sqm
- Standard car slot: 2.50m × 5.00m
- Standard truck slot: 3.60m × 12.00m
- Off-street parking building distance: not more than 200.0m (or 100.0m per some provisions)

### Distractor Engineering for PK Questions
- Used wrong parking ratio for occupancy type
- Confused car slot dimensions with truck slot dimensions
- Forgot to add jeepney/shuttle terminal requirement for markets
- Applied residential parking ratios to commercial
