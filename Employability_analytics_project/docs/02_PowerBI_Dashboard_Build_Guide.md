# Power BI Build Guide — Employability Business Performance Dashboard

> **Important note on scope:** This environment can generate the dataset, SQL, DAX, and
> full design spec, but cannot run Power BI Desktop or output a binary `.pbix` file (Power
> BI Desktop is a Windows/Mac application, not something buildable via code). Everything
> below is written so you can build the actual `.pbix` in ~3–5 hours by following it
> step by step, importing `data/Employability_Platform_Dataset.xlsx` (or the individual
> CSVs). Every visual, field, and measure referenced already exists in `/dax/dax_measures.md`
> or the data model below.

## 0. Setup

1. Open Power BI Desktop → **Get Data → Excel** → select `Employability_Platform_Dataset.xlsx`
   → load all 7 sheets (Students, Colleges, Assessments, Programs, Enrollments, Outcomes,
   Marketing) as separate tables.
2. **Model view** → create relationships:
   - `Students[College_ID]` → `Colleges[College_ID]` (Many-to-1)
   - `Students[Student_ID]` → `Assessments[Student_ID]` (1-to-Many)
   - `Students[Student_ID]` → `Enrollments[Student_ID]` (1-to-Many)
   - `Enrollments[Program_ID]` → `Programs[Program_ID]` (Many-to-1)
   - `Students[Student_ID]` → `Outcomes[Student_ID]` (1-to-Many)
3. Create a **Channel** dimension table: `New Table` →
   `Channel = DISTINCT(UNION(DISTINCT(Students[Acquisition_Channel]), DISTINCT(Marketing[Channel])))`
   (rename the resulting column to `Channel`). Relate `Students[Acquisition_Channel]` → `Channel[Channel]`
   and `Marketing[Channel]` → `Channel[Channel]` (both Many-to-1).
4. Create a **Calendar** date table:
   ```DAX
   Calendar =
   ADDCOLUMNS (
       CALENDAR ( DATE(2024,1,1), DATE(2025,12,31) ),
       "Year", YEAR([Date]),
       "Month", FORMAT([Date], "MMM YYYY"),
       "MonthNum", MONTH([Date]),
       "Quarter", "Q" & QUARTER([Date]) & " " & YEAR([Date])
   )
   ```
   Mark it as a **Date Table** (Table tools → Mark as Date Table → `Date` column).
   Relate to `Students[Registration_Date]`, `Marketing[Date]` as active; relate to
   `Enrollments[Enrollment_Date]` and `Outcomes[Outcome_Date]` as inactive relationships
   (use `USERELATIONSHIP` in any measure that needs those roles).
5. Import all measures from `/dax/dax_measures.md` into a new blank table called
   `_Measures` (Modeling → New Table → `_Measures = ROW("x", 0)`, then hide the `x` column
   and add each measure via New Measure).
6. **Theme:** Power BI → View → Themes → Browse for themes → import a custom JSON theme
   (template below) for the navy/blue corporate palette.

```json
{
  "name": "Employability Corporate",
  "dataColors": ["#0A2E5C", "#1B5FAE", "#4A90D9", "#8FC1E8", "#0A2E5C", "#F2A65A", "#D64550", "#6C7A89"],
  "background": "#FFFFFF",
  "foreground": "#0A2E5C",
  "tableAccent": "#1B5FAE",
  "good": "#2E8B57",
  "neutral": "#F2A65A",
  "bad": "#D64550"
}
```
Navy `#0A2E5C` for headers/text, blue `#1B5FAE`/`#4A90D9` for primary chart series,
light blue `#8FC1E8` for secondary series, orange `#F2A65A` for neutral flags, red
`#D64550` reserved strictly for "needs attention" alerts.

---

## PAGE 1 — Executive Overview

**Canvas:** 1280×720 (16:9). Header band (navy `#0A2E5C`, full width, 60px) with page
title in white, 24pt: *"Employability Business Performance Dashboard"*. Page navigation
buttons (rounded rectangles, top-right) linking to Pages 2–5.

**KPI card row (top, 8 cards in a row, 150×90 each):**
`[Total Students]` · `[Total Registrations]` · `[Assessments Completed]` ·
`[Program Enrollments]` · `[Placement Rate]` (format `0.0%`) · `[Total Revenue]`
(format `₹#,##0,,"L"` for lakhs or `₹#,##0` full) · `[Average Salary]` (₹ format) ·
`[Overall Conversion Rate]` (format `0.0%`). Each card: bold navy number, grey label
underneath, thin blue top border, small line-icon (use the Icons in the "Hierarchy
Slicer" or embed SVG icons via the Shapes/Icons pane).

**Row 2 (left, ~55% width):**
- **Monthly student acquisition trend** — Line chart. X = `Calendar[Month]`, Y =
  `[Total Registrations]`. Add a secondary line for `[Total Revenue]` on a second axis
  if useful, or keep single-metric for clarity.
- **Registration → Placement funnel** — Funnel visual. Categories in order: Registrations,
  Assessment Started, Assessment Completed, Program Enrollment, Placement. Use 5 explicit
  measures (`[Total Registrations]`, `[Assessments Completed]`... build a small disconnected
  table `Funnel_Stage` with an index column and a switch measure, or simply drag the 5
  count measures into the funnel's "Values" as a multi-measure funnel).

**Row 2 (right, ~45% width):**
- **State/City performance** — Filled map (Location = `Students[State]`, Size/Color =
  `[Total Students]` or `[Placement Rate]`) or, if map visuals are restricted in your
  tenant, a horizontal bar chart of Top 10 states by `[Total Students]`.

**Row 3:**
- **Top 5 performing colleges** — Bar chart, `Colleges[College_Name]` filtered/sorted
  Top 5 by `[Placement Rate]` (use a Top N filter on the visual).
- **Bottom 5 colleges requiring attention** — Same visual, Bottom 5 by `[Placement Rate]`,
  bars colored red/amber via conditional formatting rule (`< 45%` = red, `45–60%` = amber).

**Slicers (slicer panel, left rail or top strip):** `Calendar[Date]` (between), `Students[State]`,
`Students[City]`, `Colleges[Tier]`, `Programs[Program_Name]`, `Channel[Channel]`.

**Management Snapshot (bottom band, light grey `#F5F7FA` background, 5 text/card
callouts):**
1. "Highest-performing channel: " & `[Top Performing Channel]`
2. Biggest MoM growth — a card showing `[Month-over-Month Growth %]` with a title
   "Biggest Growth Month" filtered to the max month (build via a small measure using
   `TOPN` over the Calendar's month-level `[Month-over-Month Growth %]`)
3. "Lowest-converting region: " & `[Lowest Converting Region]`
4. Best-performing program — Top 1 program by `[Placement Rate]` via `TOPN`, similar
   pattern to `[Top Performing Channel]`
5. "Area requiring attention: " & (a text measure naming whichever KPI/segment is
   currently furthest below its target threshold — e.g. flag Facebook/Instagram Ads
   or Tier 3 college placement, both of which surface clearly in this dataset)

---

## PAGE 2 — Growth & Acquisition

**Title:** *"Growth & Student Acquisition"*

**KPI cards:** `[Total Leads]` · `[Total Registrations]` · Registration Conversion %
(`DIVIDE([Total Registrations],[Total Leads])`) · `[Marketing Spend]` ·
`[Cost per Registration]` · `[Month-over-Month Growth %]`.

**Visuals:**
- **Monthly Leads vs Registrations** — Clustered column/line combo, X = `Calendar[Month]`,
  columns = `[Total Leads]`, line = `[Total Registrations]`.
- **Acquisition Channel Performance** — Bar chart, `Channel[Channel]` × `[Total Registrations]`,
  sorted descending. Facebook/Instagram Ads and Google Paid Search will show the highest
  raw volume in this dataset.
- **Cost per Registration by Channel** — Bar chart, `Channel[Channel]` × `[Cost per Registration]`.
  YouTube Ads and Facebook/Instagram Ads surface as the most expensive per registration.
- **Channel Conversion Rate** — Bar chart, `Channel[Channel]` × `[Overall Conversion Rate]`.
  Referral and College Partnership Drive surface as most efficient — direct visual contrast
  with the volume chart above.
- **State-wise Student Acquisition** — Bar or map, `Students[State]` × `[Total Students]`.
- **Month-over-Month Growth** — Line/column, `Calendar[Month]` × `[Month-over-Month Growth %]`.
- **Top and Bottom Acquisition Sources** — two small Top-N / Bottom-N bar charts by
  `[Overall Conversion Rate]`.

**Matrix (core deliverable for this page):**
Rows = `Channel[Channel]`; Values = `[Total Leads]`, `[Total Registrations]`,
`[Overall Conversion Rate]`, `[Marketing Spend]`, `[Cost per Registration]`,
`[Cost per Conversion]`, `[Total Revenue]` (needs a channel-attributed revenue measure —
add `Channel Revenue = CALCULATE([Total Revenue], USERELATIONSHIP(Students[Acquisition_Channel], Channel[Channel]))`
or simpler: `CALCULATE(SUM(Enrollments[Amount_Paid]))` in a channel-filtered context via
the `Channel` table relationship to `Students`), `[ROI]`.
**Conditional formatting:** background color scale on `Cost per Conversion` (red = high,
green = low) and on `ROI` (red = negative/low multiple, green = high multiple) — Format
visual → Cell elements → Background color → Color scale.

**Management question callout box:** *"Where should the company focus its acquisition
efforts?"* — answer visually reinforced by the matrix (Referral & College Partnership
Drive: lower cost, higher conversion, positive ROI; Facebook/Instagram Ads & YouTube Ads:
high volume, poor conversion, weak ROI).

---

## PAGE 3 — Student Funnel & Operational Efficiency

**Title:** *"Student Funnel & Operational Efficiency"*

**Funnel visual** (large, left side): Registrations → Assessment Started → Assessment
Completed → Program Enrollment → Placement, with % of first stage and % of previous
stage both labeled (Funnel visual's built-in data labels support this).

**KPI cards:** Registration→Assessment % · `[Assessment Completion Rate]` ·
`[Enrollment Rate]` · `[Placement Rate]` · `[Avg Assessment Score]` ·
`[Avg Processing Time (Days)]`.

**Visuals:**
- **Conversion by college tier** — Clustered bar, `Colleges[Tier]` × `[Assessment Completion Rate]`
  and `[Placement Rate]` (two measures). Tier 1 > Tier 2 > Tier 3 pattern will be visible.
- **Conversion by state** — Bar chart, `Students[State]` × `[Enrollment Rate]`.
- **Conversion by program** — Bar chart, `Programs[Program_Name]` × `[Enrollment Rate]`
  or completion rate (calculate from Enrollments, `Enrollment_Status = "Completed"`).
- **Monthly completion trend** — Line chart, `Calendar[Month]` × `[Assessment Completion Rate]`.
- **Assessment score distribution** — Histogram (use a calculated grouping column on
  `Assessments[Score]` binned into 10-point buckets) or a simple column chart.
- **Drop-off analysis** — Column chart with one bar per funnel-stage transition and
  `[Funnel Drop-off %]`-style measures (build one measure per stage-pair as noted in
  the DAX file).

**"Problem Areas" callout section** (bottom, red-accented left border cards):
Auto-surface the stage with the highest drop-off (Registration → Assessment Started, and
separately Assessment Completed → Enrollment, both show meaningful drop-off in this
dataset — the exact ranking will depend on the live filter context) and the
lowest-performing program (Communication & Soft Skills Bootcamp shows the weakest
enrollment→completion rate in this dataset by design — good story to highlight here).

---

## PAGE 4 — College & Regional Performance

**Title:** *"College & Regional Performance"*

**KPI cards:** Students Registered · `[Assessment Completion Rate]` · `[Enrollment Rate]` ·
`[Placement Rate]` · `[Total Revenue]` · `[Average Salary]`.

**Visuals:**
- **State performance bar chart** — `Students[State]` × `[Placement Rate]`, sorted.
- **College tier comparison** — Clustered column, `Colleges[Tier]` × `[Placement Rate]`,
  `[Assessment Completion Rate]`, `[Enrollment Rate]` (3 measures side by side).
- **Top 10 colleges** — Table/bar, Top N filter by `[Placement Rate]` (min. volume filter
  via a measure like `Outcome Count > 15` in the visual-level filter to avoid small-sample
  noise, matching SQL Q2's approach).
- **Bottom 10 colleges** — same, Bottom N, red conditional formatting.
- **City performance matrix** — Rows = `Students[City]`, Values = Students, Assessment
  Completion %, Enrollment %, Placement %, Revenue.
- **Placement rate by region** — Bar or map, `Students[State]` × `[Placement Rate]`.

**Scatter plot** (signature visual for this page):
X-axis = **Student Volume** (`[Total Students]`), Y-axis = **Placement Rate**
(`[Placement Rate]`), **Bubble size = Revenue** (`[Total Revenue]`), one bubble per
college (`Colleges[College_Name]` in the "Details"/legend field). Add average reference
lines (Format → Analytics pane → Average line on both X and Y) to split the plot into
four quadrants.

**How this supports business decisions (include as a text box next to the scatter plot):**
- **High volume / high placement** (top-right) → *scale these partnerships further* —
  proven colleges worth deeper investment (more cohorts, dedicated account management).
- **High volume / low placement** (bottom-right) → *investigate immediately* — significant
  student intake isn't converting to outcomes; likely a training-quality or
  employer-pipeline gap at these specific colleges, not a demand problem.
- **Low volume / high placement** (top-left) → *untapped growth opportunity* — strong
  outcomes but small intake; a case for increased acquisition spend or partnership
  expansion at these colleges.
- **Low volume / low placement** (bottom-left) → *deprioritize or restructure* — weak on
  both dimensions; lowest ROI segment for continued investment without a structural fix.

---

## PAGE 5 — Strategic Insights & Action Areas

**Title:** *"Strategic Insights & Action Areas"*

Designed as a **read-only executive brief**, not an exploratory page — minimal slicers,
mostly cards/tables/text.

**Section 1 — Growth Opportunities** (green-accented cards):
- High-growth regions: table of States, sorted by `[Year-over-Year Growth %]` descending
  (Patna, Guwahati and other Tier-3 cities show the strongest YoY growth in this dataset,
  even though their absolute placement rate is lower — a useful nuance to call out).
- High-performing channels: Referral & College Partnership Drive (highest conversion,
  positive ROI).
- High-potential colleges: colleges in the "low volume / high placement" scatter quadrant
  from Page 4.
- Programs with strong demand: Aptitude & Reasoning Mastery and Resume & Interview
  Bootcamp show the highest completion rates; Full Stack Web Development and Data
  Analytics show strong enrollment + revenue combined.

**Section 2 — Operational Issues** (red-accented cards):
- Highest funnel drop-off stage (from Page 3).
- Lowest assessment completion: Facebook/Instagram Ads and YouTube Ads-sourced students.
- Lowest enrollment conversion: Communication & Soft Skills Bootcamp.
- Poorest-performing regions: Tier-3 cities on placement rate specifically (Patna, Ranchi,
  Kanpur in this dataset), despite strong lead volume growth — a genuine "growth vs.
  quality" tension worth flagging to management.

**Section 3 — Financial Insights:**
Cards/table: `[Total Revenue]`, `[Marketing Spend]`, `[ROI]`, Revenue by Program (bar),
Revenue by Acquisition Channel (bar).

**Section 4 — Recommended Action Areas** (4–6 cards, each with 4 fields: Issue / Evidence
/ Business Implication / Suggested Action). Populate using the *actual computed numbers*
from this dataset — do not use placeholder text. Example (fill in the live numbers once
built, they will match what's in `/docs/03_Key_Insights.md`):

> **Issue:** Facebook/Instagram Ads generates the highest lead volume of any channel but
> converts poorly.
> **Evidence:** Lead-to-conversion rate is ~1.4%, versus a ~29% rate for College
> Partnership Drive and ~27% for Referral — roughly 20x lower.
> **Business implication:** A large share of total marketing spend is going toward the
> least efficient channel, inflating blended cost-per-conversion.
> **Suggested action:** Reduce/reallocate Facebook/Instagram budget toward Referral and
> College Partnership channels; if Facebook spend continues, tighten audience targeting
> and add a lead-quality filter before the assessment stage.

(Four more of these are pre-written with the real computed numbers in
`/docs/03_Key_Insights.md` — copy them onto Page 5 cards directly.)

---

## Cross-page UI requirements checklist

- [ ] 16:9 canvas size on every page (Page settings → Custom, 1280×720)
- [ ] Consistent font: **Segoe UI** (or "Lato"/"Calibri" if unavailable) throughout,
      navy `#0A2E5C` headers, dark grey `#333333` body text
- [ ] ₹ currency format on all revenue/salary fields: `₹#,##0`
- [ ] Percentage format `0.0%` on all rate measures
- [ ] Conditional formatting (red/amber/green) only on tables/matrices showing
      performance — not decorative elsewhere
- [ ] No pie/donut charts anywhere (per spec) — use bar/column instead
- [ ] No 3D visuals
- [ ] Thin (1px) or no borders on cards; rely on whitespace for separation
- [ ] Tooltips: enable report-page tooltips or default tooltips with 2–3 extra context
      measures on hover for each major chart
- [ ] Drill-through: set up a drill-through page ("College Detail") from any
      College-related visual on Pages 1/4, showing that college's full funnel + a table
      of its enrolled students
- [ ] Navigation buttons: consistent top-right pill buttons on every page, linking to
      the other 4 pages (Format → Action → Page navigation)
