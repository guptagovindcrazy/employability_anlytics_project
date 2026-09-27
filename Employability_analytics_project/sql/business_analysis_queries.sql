/* ============================================================================
   BUSINESS GROWTH & OPERATIONS ANALYTICS — SQL QUERY PORTFOLIO
   Employability Platform (fictional/synthetic dataset)
   Dialect: ANSI SQL / PostgreSQL syntax (works with minor tweaks in
   SQL Server / MySQL — date-trunc equivalents are noted where used).

   Tables:
     Students(Student_ID, Student_Name, Gender, Age, Graduation_Year, Degree,
              Stream, College_ID, City, State, Registration_Date, Acquisition_Channel)
     Colleges(College_ID, College_Name, College_Type, City, State, Tier,
              Student_Count, Partnership_Date)
     Assessments(Assessment_ID, Student_ID, Assessment_Date, Assessment_Type,
              Score, Aptitude_Score, Technical_Score, Communication_Score,
              Completion_Status, Attempt_Number)
     Programs(Program_ID, Program_Name, Program_Category, Start_Date, End_Date,
              Fee, Capacity)
     Enrollments(Enrollment_ID, Student_ID, Program_ID, Enrollment_Date,
              Enrollment_Status, Payment_Status, Amount_Paid)
     Outcomes(Outcome_ID, Student_ID, Outcome_Date, Placement_Status,
              Company_Category, Salary, Job_Role, Placement_Source)
     Marketing(Date, Channel, Leads, Registrations, Assessment_Started,
              Assessment_Completed, Conversions, Marketing_Spend)
   ============================================================================ */


/* ----------------------------------------------------------------------
   Q1. Which acquisition channels generate the highest conversion rate?
   (Conversion = enrollment-stage "Conversions" / Leads, from Marketing)
   ---------------------------------------------------------------------- */
SELECT
    Channel,
    SUM(Leads)                                   AS Total_Leads,
    SUM(Registrations)                           AS Total_Registrations,
    SUM(Conversions)                             AS Total_Conversions,
    ROUND(100.0 * SUM(Conversions) / NULLIF(SUM(Leads), 0), 2)         AS Lead_to_Conversion_Pct,
    ROUND(100.0 * SUM(Registrations) / NULLIF(SUM(Leads), 0), 2)       AS Lead_to_Registration_Pct
FROM Marketing
GROUP BY Channel
ORDER BY Lead_to_Conversion_Pct DESC;


/* ----------------------------------------------------------------------
   Q2. Which colleges have the highest placement rates? (min. 15 outcomes)
   ---------------------------------------------------------------------- */
SELECT
    c.College_Name,
    c.Tier,
    c.City,
    COUNT(o.Outcome_ID)                                              AS Total_Outcomes,
    SUM(CASE WHEN o.Placement_Status = 'Placed' THEN 1 ELSE 0 END)   AS Placed_Count,
    ROUND(100.0 * SUM(CASE WHEN o.Placement_Status = 'Placed' THEN 1 ELSE 0 END)
          / NULLIF(COUNT(o.Outcome_ID), 0), 2)                       AS Placement_Rate_Pct
FROM Outcomes o
JOIN Students s ON s.Student_ID = o.Student_ID
JOIN Colleges c ON c.College_ID = s.College_ID
GROUP BY c.College_Name, c.Tier, c.City
HAVING COUNT(o.Outcome_ID) >= 15
ORDER BY Placement_Rate_Pct DESC
LIMIT 10;


/* ----------------------------------------------------------------------
   Q3. Which states generate the highest revenue?
   ---------------------------------------------------------------------- */
SELECT
    s.State,
    COUNT(DISTINCT e.Student_ID)          AS Paying_Students,
    SUM(e.Amount_Paid)                    AS Total_Revenue,
    ROUND(AVG(e.Amount_Paid), 0)          AS Avg_Revenue_Per_Enrollment
FROM Enrollments e
JOIN Students s ON s.Student_ID = e.Student_ID
GROUP BY s.State
ORDER BY Total_Revenue DESC;


/* ----------------------------------------------------------------------
   Q4. Which programs have the highest enrollment?
   ---------------------------------------------------------------------- */
SELECT
    p.Program_Name,
    p.Program_Category,
    COUNT(e.Enrollment_ID)                                            AS Total_Enrollments,
    SUM(CASE WHEN e.Enrollment_Status = 'Completed' THEN 1 ELSE 0 END) AS Completed_Count,
    ROUND(100.0 * SUM(CASE WHEN e.Enrollment_Status = 'Completed' THEN 1 ELSE 0 END)
          / NULLIF(COUNT(e.Enrollment_ID), 0), 2)                      AS Completion_Rate_Pct
FROM Enrollments e
JOIN Programs p ON p.Program_ID = e.Program_ID
GROUP BY p.Program_Name, p.Program_Category
ORDER BY Total_Enrollments DESC;


/* ----------------------------------------------------------------------
   Q5. What is the month-over-month registration growth rate?
   ---------------------------------------------------------------------- */
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', Registration_Date) AS Reg_Month,
        COUNT(*)                                AS Registrations
    FROM Students
    GROUP BY DATE_TRUNC('month', Registration_Date)
)
SELECT
    Reg_Month,
    Registrations,
    LAG(Registrations) OVER (ORDER BY Reg_Month)                       AS Prev_Month_Registrations,
    ROUND(100.0 * (Registrations - LAG(Registrations) OVER (ORDER BY Reg_Month))
          / NULLIF(LAG(Registrations) OVER (ORDER BY Reg_Month), 0), 2) AS MoM_Growth_Pct
FROM monthly
ORDER BY Reg_Month;


/* ----------------------------------------------------------------------
   Q6. Where is the largest drop-off in the student funnel?
   (Registration -> Assessment Started -> Completed -> Enrolled -> Placed)
   ---------------------------------------------------------------------- */
WITH funnel AS (
    SELECT
        (SELECT COUNT(*) FROM Students)                                                         AS Registrations,
        (SELECT COUNT(DISTINCT Student_ID) FROM Assessments)                                     AS Assessment_Started,
        (SELECT COUNT(DISTINCT Student_ID) FROM Assessments WHERE Completion_Status='Completed') AS Assessment_Completed,
        (SELECT COUNT(DISTINCT Student_ID) FROM Enrollments)                                     AS Enrolled,
        (SELECT COUNT(DISTINCT Student_ID) FROM Outcomes WHERE Placement_Status='Placed')        AS Placed
)
SELECT
    'Registration -> Assessment Started' AS Funnel_Stage,
    Registrations AS Stage_Start, Assessment_Started AS Stage_End,
    ROUND(100.0 * (Registrations - Assessment_Started) / NULLIF(Registrations,0), 2) AS Drop_Off_Pct
FROM funnel
UNION ALL
SELECT 'Assessment Started -> Completed', Assessment_Started, Assessment_Completed,
    ROUND(100.0 * (Assessment_Started - Assessment_Completed) / NULLIF(Assessment_Started,0), 2)
FROM funnel
UNION ALL
SELECT 'Assessment Completed -> Enrolled', Assessment_Completed, Enrolled,
    ROUND(100.0 * (Assessment_Completed - Enrolled) / NULLIF(Assessment_Completed,0), 2)
FROM funnel
UNION ALL
SELECT 'Enrolled -> Placed', Enrolled, Placed,
    ROUND(100.0 * (Enrolled - Placed) / NULLIF(Enrolled,0), 2)
FROM funnel
ORDER BY Drop_Off_Pct DESC;


/* ----------------------------------------------------------------------
   Q7. Which acquisition channels have poor ROI?
   (ROI proxied as Revenue from converted students per channel vs. Spend;
    revenue attribution: enrollment Amount_Paid for students acquired via
    that channel)
   ---------------------------------------------------------------------- */
WITH channel_revenue AS (
    SELECT s.Acquisition_Channel, SUM(e.Amount_Paid) AS Revenue
    FROM Enrollments e
    JOIN Students s ON s.Student_ID = e.Student_ID
    GROUP BY s.Acquisition_Channel
),
channel_spend AS (
    SELECT Channel, SUM(Marketing_Spend) AS Spend
    FROM Marketing
    GROUP BY Channel
)
SELECT
    cs.Channel,
    cs.Spend,
    COALESCE(cr.Revenue, 0)                                     AS Attributed_Revenue,
    ROUND((COALESCE(cr.Revenue, 0) - cs.Spend) / NULLIF(cs.Spend, 0), 2) AS ROI_Multiple
FROM channel_spend cs
LEFT JOIN channel_revenue cr ON cr.Acquisition_Channel = cs.Channel
ORDER BY ROI_Multiple ASC;


/* ----------------------------------------------------------------------
   Q8. Which colleges have high student volume but low placement rate?
   (Quadrant analysis input — flags colleges above median volume but
    below median placement rate)
   ---------------------------------------------------------------------- */
WITH college_stats AS (
    SELECT
        c.College_ID, c.College_Name, c.Tier, c.City,
        COUNT(DISTINCT s.Student_ID)                                             AS Student_Volume,
        COUNT(DISTINCT CASE WHEN o.Placement_Status='Placed' THEN o.Student_ID END) AS Placed_Count,
        COUNT(DISTINCT o.Student_ID)                                             AS Outcome_Count
    FROM Colleges c
    JOIN Students s ON s.College_ID = c.College_ID
    LEFT JOIN Outcomes o ON o.Student_ID = s.Student_ID
    GROUP BY c.College_ID, c.College_Name, c.Tier, c.City
),
medians AS (
    SELECT
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY Student_Volume) AS Median_Volume,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY
            CASE WHEN Outcome_Count > 0 THEN 1.0*Placed_Count/Outcome_Count END) AS Median_Placement_Rate
    FROM college_stats
)
SELECT
    cs.College_Name, cs.Tier, cs.City, cs.Student_Volume,
    ROUND(100.0 * cs.Placed_Count / NULLIF(cs.Outcome_Count,0), 2) AS Placement_Rate_Pct
FROM college_stats cs, medians m
WHERE cs.Student_Volume > m.Median_Volume
  AND (1.0 * cs.Placed_Count / NULLIF(cs.Outcome_Count,0)) < m.Median_Placement_Rate
ORDER BY cs.Student_Volume DESC;


/* ----------------------------------------------------------------------
   Q9. What is the average salary by program?
   ---------------------------------------------------------------------- */
SELECT
    p.Program_Name,
    COUNT(o.Outcome_ID)             AS Placed_Students,
    ROUND(AVG(o.Salary), 0)         AS Avg_Salary,
    MIN(o.Salary)                   AS Min_Salary,
    MAX(o.Salary)                   AS Max_Salary
FROM Outcomes o
JOIN Enrollments e ON e.Student_ID = o.Student_ID
JOIN Programs p ON p.Program_ID = e.Program_ID
WHERE o.Placement_Status = 'Placed'
GROUP BY p.Program_Name
ORDER BY Avg_Salary DESC;


/* ----------------------------------------------------------------------
   Q10. Which cities show the strongest registration growth (2024 -> 2025)?
   ---------------------------------------------------------------------- */
WITH yearly AS (
    SELECT City, EXTRACT(YEAR FROM Registration_Date) AS Yr, COUNT(*) AS Registrations
    FROM Students
    GROUP BY City, EXTRACT(YEAR FROM Registration_Date)
)
SELECT
    y24.City,
    y24.Registrations AS Registrations_2024,
    y25.Registrations AS Registrations_2025,
    ROUND(100.0 * (y25.Registrations - y24.Registrations) / NULLIF(y24.Registrations, 0), 2) AS Growth_Pct
FROM yearly y24
JOIN yearly y25 ON y25.City = y24.City AND y25.Yr = 2025
WHERE y24.Yr = 2024
ORDER BY Growth_Pct DESC;


/* ----------------------------------------------------------------------
   Q11. Which colleges show declining performance (registrations dropping
   quarter over quarter in the most recent two quarters on record)?
   ---------------------------------------------------------------------- */
WITH quarterly AS (
    SELECT
        c.College_Name,
        DATE_TRUNC('quarter', s.Registration_Date) AS Qtr,
        COUNT(*) AS Registrations
    FROM Students s
    JOIN Colleges c ON c.College_ID = s.College_ID
    GROUP BY c.College_Name, DATE_TRUNC('quarter', s.Registration_Date)
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY College_Name ORDER BY Qtr DESC) AS rn
    FROM quarterly
)
SELECT
    cur.College_Name,
    prev.Registrations AS Prior_Quarter,
    cur.Registrations  AS Latest_Quarter,
    ROUND(100.0 * (cur.Registrations - prev.Registrations) / NULLIF(prev.Registrations, 0), 2) AS QoQ_Change_Pct
FROM ranked cur
JOIN ranked prev ON prev.College_Name = cur.College_Name AND prev.rn = cur.rn + 1
WHERE cur.rn = 1
  AND cur.Registrations < prev.Registrations
ORDER BY QoQ_Change_Pct ASC;


/* ----------------------------------------------------------------------
   Q12. What percentage of registered students complete an assessment?
   ---------------------------------------------------------------------- */
SELECT
    (SELECT COUNT(*) FROM Students)                                                            AS Total_Registrations,
    (SELECT COUNT(DISTINCT Student_ID) FROM Assessments WHERE Completion_Status = 'Completed')  AS Completed_Assessment,
    ROUND(100.0 * (SELECT COUNT(DISTINCT Student_ID) FROM Assessments WHERE Completion_Status = 'Completed')
          / NULLIF((SELECT COUNT(*) FROM Students), 0), 2)                                      AS Assessment_Completion_Pct;


/* ----------------------------------------------------------------------
   Q13. Which programs generate the highest revenue per enrolled student?
   ---------------------------------------------------------------------- */
SELECT
    p.Program_Name,
    COUNT(e.Enrollment_ID)                              AS Total_Enrollments,
    SUM(e.Amount_Paid)                                  AS Total_Revenue,
    ROUND(SUM(e.Amount_Paid) * 1.0 / NULLIF(COUNT(e.Enrollment_ID), 0), 0) AS Revenue_Per_Student
FROM Enrollments e
JOIN Programs p ON p.Program_ID = e.Program_ID
GROUP BY p.Program_Name
ORDER BY Revenue_Per_Student DESC;


/* ----------------------------------------------------------------------
   Q14. Which acquisition channels have the lowest cost per conversion?
   ---------------------------------------------------------------------- */
SELECT
    Channel,
    SUM(Marketing_Spend)                                              AS Total_Spend,
    SUM(Conversions)                                                  AS Total_Conversions,
    ROUND(SUM(Marketing_Spend) / NULLIF(SUM(Conversions), 0), 2)      AS Cost_Per_Conversion
FROM Marketing
GROUP BY Channel
HAVING SUM(Conversions) > 0
ORDER BY Cost_Per_Conversion ASC;


/* ----------------------------------------------------------------------
   Q15. Which segments (city x college tier x channel) should management
   investigate first? (Composite risk score: high volume, low completion,
   low placement, high spend inefficiency)
   ---------------------------------------------------------------------- */
WITH seg AS (
    SELECT
        s.City,
        c.Tier,
        s.Acquisition_Channel,
        COUNT(DISTINCT s.Student_ID)                                                              AS Volume,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.Completion_Status='Completed' THEN a.Student_ID END)
              / NULLIF(COUNT(DISTINCT s.Student_ID), 0), 2)                                        AS Assessment_Completion_Pct,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN o.Placement_Status='Placed' THEN o.Student_ID END)
              / NULLIF(COUNT(DISTINCT o.Student_ID), 0), 2)                                        AS Placement_Pct
    FROM Students s
    JOIN Colleges c ON c.College_ID = s.College_ID
    LEFT JOIN Assessments a ON a.Student_ID = s.Student_ID
    LEFT JOIN Outcomes o ON o.Student_ID = s.Student_ID
    GROUP BY s.City, c.Tier, s.Acquisition_Channel
)
SELECT *
FROM seg
WHERE Volume >= 20
  AND (Assessment_Completion_Pct < 50 OR Placement_Pct < 40)
ORDER BY Volume DESC, Placement_Pct ASC
LIMIT 20;
