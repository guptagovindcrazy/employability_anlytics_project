<<<<<<< HEAD
# Business Growth & Operations Analytics Dashboard
### Employability Platform — Power BI | SQL | DAX | Python

> **Note:** All data in this project is **fictional/synthetic**, generated to reflect
> realistic business patterns for an Indian education/employability platform. It is not
> based on, or intended to represent, any real company.

---

## Business Problem

Employability platforms operate a multi-stage funnel — leads become registrations,
registrations attempt assessments, assessments convert into paid program enrollments,
and enrollments (eventually) convert into job placements. Without a unified view across
that funnel, management cannot see *where* growth is happening, *where* money is being
wasted, or *which* colleges, cities and programs deserve more investment versus a fix.
This project builds that unified view: a single source of truth connecting acquisition,
assessments, enrollments, revenue and placement outcomes, so leadership can move from
"we grew this quarter" to "we grew because of X, and we're losing money because of Y."

## Objective

Build an executive-ready Power BI dashboard that lets a Founder/CEO/Business Head:
- Track growth and acquisition efficiency across 8 marketing channels
- Diagnose exactly where students are lost in the funnel
- Compare 160 colleges and 20 cities on volume *and* outcome quality (not volume alone)
- See revenue, spend and ROI by channel and program
- Get pre-computed, evidence-backed action recommendations, not just charts

## Tools Used

- **Power BI** — data model, DAX measures, 5-page executive dashboard
- **DAX** — 20+ measures covering conversion, growth, ROI and time intelligence
- **SQL** — 15 business-question queries + data-quality detection queries
- **Python (pandas/numpy)** — synthetic dataset generation with realistic funnel logic,
  seasonality, and intentionally injected data-quality issues

## Dataset

A relational dataset (not a single flat table) covering **2024–2025**, generated with
realistic business relationships rather than random values:

| Table | Rows | Grain |
|---|---|---|
| Students | 22,000 | 1 row per student |
| Colleges | 160 | 1 row per college |
| Assessments | 19,588 | 1 row per assessment attempt |
| Programs | 12 | 1 row per program |
| Enrollments | 5,968 | 1 row per program enrollment |
| Outcomes | 4,268 | 1 row per tracked placement outcome |
| Marketing | 5,848 | 1 row per channel per day |

**~57,800 total rows** across 7 related tables. See `/data/clean/` for the model-ready
CSVs, `/data/Employability_Platform_Dataset.xlsx` for a single multi-sheet workbook, and
`/data/raw/` + `/docs/01_Data_Quality_Report.md` for the pre-cleaning versions and how
issues in them were found and fixed.

The data encodes deliberate, realistic business problems: some channels have high volume
but poor conversion; some colleges have high registrations but low assessment completion;
Tier 3 colleges/cities show strong growth but weaker placement outcomes; one program has
high enrollment but low completion; registrations follow real seasonality (dips around
exam months, peaks after results). Full generation logic: `/generate_data.py`.

## Key KPIs

Total Students · Total Leads · Registrations · Assessment Completion Rate · Enrollment
Rate · Placement Rate · Overall Conversion Rate · Total Revenue · Average Revenue per
Student · Average Salary · Marketing Spend · Cost per Registration · Cost per Conversion
· ROI · Month-over-Month / Year-over-Year Growth

## Key Insights

See `/docs/03_Key_Insights.md` for the full write-up with evidence. Highlights:
- Facebook/Instagram Ads drives 39% of all leads but converts at just 1.43% — roughly
  20x worse than Referral (26.8%) or College Partnership Drive (28.9%)
- Placement rate falls sharply by college tier: Tier 1 69.2% → Tier 2 52.0% → Tier 3 34.1%
- The single biggest funnel leak is assessment-completion → enrollment (55.6% loss),
  larger than the registration → assessment-completion loss (38.9%)
- "Communication & Soft Skills Bootcamp" has the lowest program completion rate (65.0%)
  of all 12 programs
- Patna (Tier-3 city) is growing at +23.7% YoY while posting one of the weakest placement
  rates — a growth/quality mismatch worth flagging

## Business Recommendations

Full detail with supporting numbers in `/docs/03_Key_Insights.md`. Summary:
1. Reallocate spend from Facebook/Instagram Ads toward Referral & College Partnership Drive
2. Fix the assessment → enrollment conversion gap (the largest funnel leak) before
   spending more on acquisition
3. Redesign or retire the Communication & Soft Skills Bootcamp in its current form
4. Invest in placement support for Tier 3 colleges before scaling intake further there
5. Prioritize new high-fee program launches in the top revenue states (Maharashtra,
   Karnataka, Delhi)
6. Investigate the two cities with negative YoY growth (Bhopal, Varanasi)

## Dashboard Pages

| Page | Focus |
|---|---|
| 1. Executive Overview | Top-line KPIs, funnel, revenue trend, top/bottom colleges, auto-generated management snapshot |
| 2. Growth & Acquisition | Channel performance matrix with conditional formatting, cost per registration/conversion, ROI |
| 3. Student Funnel & Operations | Full funnel with stage-by-stage conversion %, drop-off diagnosis, assessment score distribution |
| 4. College & Regional Performance | Top/bottom 10 colleges, tier comparison, volume-vs-placement-vs-revenue scatter (quadrant analysis) |
| 5. Strategic Insights & Action Areas | Growth opportunities, operational issues, financial summary, 6 evidence-backed recommendations |

Full page-by-page build specification (fields, measures, visuals, formatting rules):
`/docs/02_PowerBI_Dashboard_Build_Guide.md`.

## Skills Demonstrated

SQL · Data Modeling (star schema) · DAX · Power BI · Business Analysis · KPI Development
· Data Visualization · Data Quality Auditing · Problem Solving · Strategic Thinking

## Repository Structure

```
├── README.md
├── generate_data.py                        # synthetic dataset generator (Python)
├── data/
│   ├── Employability_Platform_Dataset.xlsx  # single workbook, all 7 tables
│   ├── clean/                               # model-ready CSVs (import these into Power BI)
│   │   ├── Students.csv
│   │   ├── Colleges.csv
│   │   ├── Assessments.csv
│   │   ├── Programs.csv
│   │   ├── Enrollments.csv
│   │   ├── Outcomes.csv
│   │   └── Marketing.csv
│   ├── raw/                                 # pre-cleaning versions with intentional DQ issues
│   │   ├── Students_RAW.csv
│   │   ├── Assessments_RAW.csv
│   │   └── Outcomes_RAW.csv
│   └── dq_report.json
├── sql/
│   ├── business_analysis_queries.sql        # 15 business-question queries
│   └── data_quality_checks.sql              # detection queries used in the DQ report
├── dax/
│   └── dax_measures.md                      # 20+ measures with explanations
├── docs/
│   ├── 01_Data_Quality_Report.md
│   ├── 02_PowerBI_Dashboard_Build_Guide.md  # page-by-page build spec
│   ├── 03_Key_Insights.md
│   └── 04_Interview_Prep.md
└── Employability_Business_Dashboard.pbix    # (build locally — see build guide)
```

## How to Rebuild This Project

1. `python generate_data.py` — regenerates the dataset (seeded, reproducible)
2. Load `sql/data_quality_checks.sql` against `data/raw/` to reproduce the DQ findings
3. Run `sql/business_analysis_queries.sql` against the cleaned tables (works in
   PostgreSQL directly; minor syntax edits for SQL Server/MySQL)
4. Open Power BI Desktop → follow `docs/02_PowerBI_Dashboard_Build_Guide.md` step by step,
   importing `data/Employability_Platform_Dataset.xlsx` and pasting in the measures from
   `dax/dax_measures.md`
=======
# employability_anlytics_project
emplability analystics dashboard using power bi and employability platform dataset
>>>>>>> 5e3e144c064aaed39ecb3f28087ff01382556ddd
