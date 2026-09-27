# DAX Measures — Employability Business Performance Dashboard

All measures live in a dedicated **`_Measures`** table (best practice: keep measures
out of physical fact tables, use a homeless/measures table for organization).

Data model relationships (star schema):
- `Students[College_ID]` → `Colleges[College_ID]` (many-to-one)
- `Students[Student_ID]` → `Assessments[Student_ID]` (one-to-many)
- `Students[Student_ID]` → `Enrollments[Student_ID]` (one-to-many)
- `Enrollments[Program_ID]` → `Programs[Program_ID]` (many-to-one)
- `Students[Student_ID]` → `Outcomes[Student_ID]` (one-to-many)
- `Marketing[Channel]` ↔ `Students[Acquisition_Channel]` (via a shared `Channel` dimension table — see note below)
- A `Calendar` (date) table marked as a Date table, related to `Students[Registration_Date]`,
  `Marketing[Date]`, `Outcomes[Outcome_Date]`, `Enrollments[Enrollment_Date]` (use separate
  active/inactive relationships + `USERELATIONSHIP` where more than one date role is needed)

> **Note on Channel relationship:** Because `Acquisition_Channel` lives on `Students` and
> `Channel` lives on `Marketing` at a different grain (daily, aggregated), build a small
> `Channel` dimension table (`DISTINCT` list of channel names) and relate both `Students`
> and `Marketing` to it. This avoids a direct many-to-many relationship between two fact
> tables, which is a common Power BI modeling pitfall.

---

## 1. Volume & Core Counts

```DAX
Total Students = DISTINCTCOUNT(Students[Student_ID])
```
Counts unique registered students in the current filter context. `DISTINCTCOUNT` (not
`COUNTROWS`) guards against any accidental duplication in the fact table.

```DAX
Total Leads = SUM(Marketing[Leads])
```
Top-of-funnel volume from the daily channel-level marketing table.

```DAX
Total Registrations = SUM(Marketing[Registrations])
```
Registrations as recorded in the marketing funnel (should reconcile with `Total Students`
when no date filter narrows the Students table differently — used as a cross-check).

```DAX
Assessments Completed =
CALCULATE (
    DISTINCTCOUNT ( Assessments[Student_ID] ),
    Assessments[Completion_Status] = "Completed"
)
```
Distinct students (not attempts) who completed at least one assessment — avoids
double-counting students who retook a test.

```DAX
Program Enrollments = DISTINCTCOUNT(Enrollments[Enrollment_ID])
```

---

## 2. Conversion & Funnel Rate Measures

```DAX
Assessment Completion Rate =
DIVIDE ( [Assessments Completed], [Total Students] )
```

```DAX
Enrollment Rate =
DIVIDE ( [Program Enrollments], [Assessments Completed] )
```
Measures how many students who completed an assessment go on to enroll in a paid program.

```DAX
Placement Rate =
VAR PlacedStudents =
    CALCULATE ( DISTINCTCOUNT ( Outcomes[Student_ID] ), Outcomes[Placement_Status] = "Placed" )
VAR OutcomeTrackedStudents = DISTINCTCOUNT ( Outcomes[Student_ID] )
RETURN
DIVIDE ( PlacedStudents, OutcomeTrackedStudents )
```
Placement rate is calculated against students who have a *tracked outcome* (i.e. enough
time has passed since program completion to know their status), not against all
registrations — this avoids diluting the rate with students who haven't had time to be
placed yet.

```DAX
Overall Conversion Rate =
DIVIDE ( [Program Enrollments], [Total Leads] )
```
End-to-end funnel efficiency: lead → paying/enrolled student.

```DAX
Funnel Drop-off % =
VAR StageStart = [Total Registrations]
VAR StageEnd = [Assessments Completed]
RETURN
DIVIDE ( StageStart - StageEnd, StageStart )
```
Generic drop-off measure between two adjacent funnel stages — duplicate this pattern
(swap `StageStart`/`StageEnd`) for each stage transition, or parameterize with field
parameters for an interactive stage-selector on Page 3.

---

## 3. Revenue & Financial Measures

```DAX
Total Revenue = SUM(Enrollments[Amount_Paid])
```

```DAX
Average Revenue per Student =
DIVIDE ( [Total Revenue], DISTINCTCOUNT ( Enrollments[Student_ID] ) )
```

```DAX
Average Salary =
CALCULATE ( AVERAGE ( Outcomes[Salary] ), Outcomes[Placement_Status] = "Placed" )
```

```DAX
Marketing Spend = SUM(Marketing[Marketing_Spend])
```

```DAX
Cost per Registration =
DIVIDE ( [Marketing Spend], [Total Registrations] )
```

```DAX
Cost per Conversion =
DIVIDE ( [Marketing Spend], SUM ( Marketing[Conversions] ) )
```

```DAX
ROI =
VAR Revenue = [Total Revenue]
VAR Spend = [Marketing Spend]
RETURN
DIVIDE ( Revenue - Spend, Spend )
```
Expressed as a multiple (e.g. 2.5 = ₹2.50 returned for every ₹1 spent). Format as `0.0"x"`
or as a percentage per the KPI card style chosen.

---

## 4. Time Intelligence

> Requires a proper marked **Date table** (`Calendar`) related to the fact tables' date
> columns for these to work correctly.

```DAX
Previous Month Revenue =
CALCULATE ( [Total Revenue], DATEADD ( 'Calendar'[Date], -1, MONTH ) )
```

```DAX
Previous Month Registrations =
CALCULATE ( [Total Registrations], DATEADD ( 'Calendar'[Date], -1, MONTH ) )
```

```DAX
Month-over-Month Growth % =
DIVIDE ( [Total Registrations] - [Previous Month Registrations], [Previous Month Registrations] )
```

```DAX
Year-over-Year Growth % =
VAR PriorYear = CALCULATE ( [Total Registrations], SAMEPERIODLASTYEAR ( 'Calendar'[Date] ) )
RETURN
DIVIDE ( [Total Registrations] - PriorYear, PriorYear )
```

```DAX
Revenue MoM Growth % =
VAR PrevRevenue = [Previous Month Revenue]
RETURN
DIVIDE ( [Total Revenue] - PrevRevenue, PrevRevenue )
```

---

## 5. Ranking / "Top Performer" Measures (for Management Snapshot cards)

```DAX
Top Performing Channel =
VAR ChannelTable =
    ADDCOLUMNS (
        VALUES ( 'Channel'[Channel] ),
        "ConvRate", [Overall Conversion Rate]
    )
RETURN
CALCULATE (
    SELECTEDVALUE ( 'Channel'[Channel] ),
    TOPN ( 1, ChannelTable, [ConvRate], DESC )
)
```
Returns the single channel name with the highest conversion rate in the current filter
context — feeds directly into a Management Snapshot text card ("Best channel this month: " & [Top Performing Channel]).

```DAX
Top Performing Region =
VAR RegionTable =
    ADDCOLUMNS (
        VALUES ( Students[State] ),
        "PlaceRate", [Placement Rate]
    )
RETURN
CALCULATE (
    SELECTEDVALUE ( Students[State] ),
    TOPN ( 1, RegionTable, [PlaceRate], DESC )
)
```

```DAX
Lowest Converting Region =
VAR RegionTable =
    ADDCOLUMNS (
        VALUES ( Students[State] ),
        "ConvRate", [Overall Conversion Rate]
    )
RETURN
CALCULATE (
    SELECTEDVALUE ( Students[State] ),
    TOPN ( 1, RegionTable, [ConvRate], ASC )
)
```

---

## 6. Supporting Measures (used inside conditional formatting / tooltips)

```DAX
Avg Assessment Score =
CALCULATE ( AVERAGE ( Assessments[Score] ), Assessments[Completion_Status] = "Completed" )
```

```DAX
Avg Processing Time (Days) =
AVERAGEX (
    Enrollments,
    DATEDIFF ( RELATED ( Students[Registration_Date] ), Enrollments[Enrollment_Date], DAY )
)
```
Average number of days from registration to program enrollment — an operational
efficiency indicator for Page 3.

```DAX
Revenue vs Spend Variance =
[Total Revenue] - [Marketing Spend]
```

```DAX
KPI Status Color =
VAR Rate = [Placement Rate]
RETURN
SWITCH (
    TRUE (),
    Rate >= 0.65, "Green",
    Rate >= 0.45, "Amber",
    "Red"
)
```
Used to drive conditional-formatting rules on matrices/cards (red/amber/green thresholds
should be agreed with the business, not hard-coded arbitrarily — these are illustrative).

---

## DAX Practices Followed

- **Measures over calculated columns** wherever a value can be computed at query time —
  keeps the model smaller and calculations context-aware (respond correctly to slicers).
- **`DIVIDE()` instead of `/`** everywhere, to safely handle divide-by-zero without needing
  nested `IF` guards.
- **Variables (`VAR`/`RETURN`)** used for readability and to avoid re-evaluating the same
  expression multiple times inside one measure.
- **`DISTINCTCOUNT` over `COUNT`/`COUNTROWS`** on ID columns to guard against fact-table
  duplication (e.g., multiple assessment attempts per student).
- Explicit **filter-context measures** (`CALCULATE` with clear filter arguments) rather than
  relying on ambiguous row context, so measures behave predictably when placed on any
  visual, in any combination of slicers.
