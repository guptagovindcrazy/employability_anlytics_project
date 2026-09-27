/* ============================================================================
   DATA QUALITY DETECTION QUERIES
   Run against the RAW tables before cleaning (see /data/raw/*.csv)
   ============================================================================ */

-- Missing values
SELECT COUNT(*) AS missing_gender FROM Students_RAW WHERE Gender IS NULL OR TRIM(Gender) = '';
SELECT COUNT(*) AS missing_age FROM Students_RAW WHERE Age IS NULL;

-- Duplicate records
SELECT Student_ID, COUNT(*) AS occurrences
FROM Students_RAW
GROUP BY Student_ID
HAVING COUNT(*) > 1;

-- Invalid / implausible dates
SELECT *
FROM Students_RAW
WHERE Registration_Date IS NULL
   OR Registration_Date > CURRENT_DATE
   OR Registration_Date < DATE '2023-06-01';   -- platform launched 2024, allow a small buffer

-- Age outliers (plausible working range for this cohort: 17-35)
SELECT *
FROM Students_RAW
WHERE Age IS NOT NULL AND (Age < 17 OR Age > 35);

-- Referential integrity: students pointing to a College_ID that doesn't exist
SELECT s.Student_ID, s.College_ID
FROM Students_RAW s
LEFT JOIN Colleges c ON c.College_ID = s.College_ID
WHERE c.College_ID IS NULL;

-- Assessment score range violations
SELECT * FROM Assessments_RAW WHERE Score < 0;
SELECT * FROM Assessments_RAW WHERE Technical_Score > 100 OR Aptitude_Score > 100 OR Communication_Score > 100;

-- Duplicate assessment records
SELECT Assessment_ID, COUNT(*)
FROM Assessments_RAW
GROUP BY Assessment_ID
HAVING COUNT(*) > 1;

-- Salary outliers within each company category (IQR method)
WITH stats AS (
    SELECT
        Company_Category,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Salary) AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Salary) AS Q3
    FROM Outcomes_RAW
    WHERE Placement_Status = 'Placed'
    GROUP BY Company_Category
)
SELECT o.*
FROM Outcomes_RAW o
JOIN stats st ON st.Company_Category = o.Company_Category
WHERE o.Salary > st.Q3 + 1.5 * (st.Q3 - st.Q1)
   OR o.Salary < st.Q1 - 1.5 * (st.Q3 - st.Q1);

-- Missing Company_Category for placed students
SELECT * FROM Outcomes_RAW WHERE Placement_Status = 'Placed' AND Company_Category IS NULL;

-- Cross-table logic check: a placement should only exist for a COMPLETED enrollment
SELECT o.Student_ID
FROM Outcomes_RAW o
LEFT JOIN Enrollments e ON e.Student_ID = o.Student_ID AND e.Enrollment_Status = 'Completed'
WHERE o.Placement_Status = 'Placed' AND e.Student_ID IS NULL;
