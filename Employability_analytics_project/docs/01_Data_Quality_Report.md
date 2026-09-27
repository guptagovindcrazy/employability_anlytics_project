# Data Quality Report

Before building the dashboard, the raw exports (`/data/raw/`) were profiled and cleaned
into model-ready tables (`/data/clean/`). This mirrors a real BI workflow: source-system
data is never dashboard-ready on day one.

## 1. Students table

| Issue | Count | Handling |
|---|---|---|
| Missing `Gender` | 264 (1.2%) | Recoded to `"Not Specified"` rather than dropped — dropping would bias demographic KPIs. Flagged in a `Data_Quality_Flag` staging column during cleaning. |
| Missing `Age` | 177 (0.8%) | Imputed with the **median age of the student's Degree + Graduation_Year cohort**, not a global mean, to preserve realistic age distribution by program level. |
| Duplicate `Student_ID` rows | 132 | Exact duplicates from a simulated double-export; removed with `DISTINCT` on `Student_ID`, keeping the first occurrence. |
| Invalid / missing `Registration_Date` (future dates, typo years like 2004, blanks) | 88 | Future dates (`>2025-12-31`) and implausible historical dates (before the platform's 2024 launch) were nulled and re-imputed from the student's earliest related `Assessment_Date` minus a typical 1–25 day lag where available; otherwise the row was excluded from date-based trend visuals (but kept for non-time-based counts) and flagged. |
| Age outliers (14, 15, 63, 71) | 66 | Values outside a plausible 17–35 working range for this platform were treated as data-entry errors, not real outliers to investigate — capped/nulled rather than removed, since the rest of the row is still usable. |
| Broken `College_ID` reference (`CLG9999` doesn't exist in `Colleges`) | 44 | Referential-integrity check via `LEFT JOIN ... WHERE Colleges.College_ID IS NULL`. Re-mapped to an `"Unmapped / Unknown College"` placeholder row added to `Colleges` so the row isn't silently lost from headcount totals, but is excluded from college-level performance leaderboards. |

**Result:** 22,132 raw rows → **22,000 clean rows** used in the model.

## 2. Assessments table

| Issue | Count | Handling |
|---|---|---|
| Negative scores | 29 | Data-entry sign errors; corrected to absolute value (`ABS()`), since the underlying 0–100 scale was otherwise consistent. |
| Scores > 100 (e.g. 140) | 19 | Capped at 100 — impossible under the platform's scoring scale, treated as fat-finger entry (e.g., extra trailing digit). |
| Duplicate `Assessment_ID` | 78 | Removed on `DISTINCT`. |
| Missing sub-scores for incomplete attempts | 3,490 | **Not an error** — these are genuinely missing because the student did not finish the assessment (`Completion_Status = "Incomplete"` / `"Dropped Off"`). Left as `NULL` (not imputed with 0, which would understate true engagement) and explicitly excluded from all average-score measures via `CALCULATE(..., Completion_Status = "Completed")`. |

**Result:** 19,666 raw rows → **19,588 clean rows**.

## 3. Outcomes table

| Issue | Count | Handling |
|---|---|---|
| Salary unit outliers (annual figure entered ×12, i.e., as if monthly) | 9 | Detected via a z-score / IQR check within each `Company_Category` — values >3 standard deviations above the category mean were reviewed and corrected by dividing by 12 where the corrected value fell back within a plausible band for that category. |
| Missing `Company_Category` for placed students | 7 | Left as `"Not Captured"` category rather than guessed, and excluded from the "revenue by company category" cut but retained in overall placement-rate counts. |

**Result:** 4,268 rows, all retained post-cleaning (issues corrected in place, none dropped).

## 4. Referential Integrity Checks Performed

- `Assessments.Student_ID` → `Students.Student_ID`: verified all assessment records map
  to a valid student.
- `Enrollments.Student_ID` / `Enrollments.Program_ID` → `Students` / `Programs`: verified.
- `Outcomes.Student_ID` → `Students.Student_ID`: verified, and additionally checked that
  every placement record traces back to a `Completed` enrollment (a placement without a
  completed program would itself be a logic error — none found post-cleaning).
- `Students.College_ID` → `Colleges.College_ID`: the intentional 44-row break above was
  the only violation found; resolved as described.

## 5. Summary

| Table | Raw Rows | Issues Found | Issues Fixed | Clean Rows |
|---|---|---|---|---|
| Students | 22,132 | 771 field-level issues across 5 categories | 771 | 22,000 |
| Assessments | 19,666 | 126 (excl. natural missing sub-scores) | 126 | 19,588 |
| Outcomes | 4,268 | 16 | 16 | 4,268 |

This process is intentionally reproducible: see `/sql/data_quality_checks.sql` for the
exact detection queries, and `/generate_data.py` (section 9) for how the issues were
injected for demonstration purposes on this synthetic dataset.
