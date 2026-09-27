# Interview Preparation — Business Growth & Operations Analytics Dashboard

## 60-Second Project Explanation (say this out loud, time it)

"I built an end-to-end analytics project simulating an Indian employability platform —
the kind of company that helps students become job-ready through assessments and
training. I generated a realistic synthetic dataset of about 22,000 students across
seven related tables — students, colleges, assessments, programs, enrollments, and
placement outcomes — with real funnel logic: leads become registrations, registrations
attempt assessments, assessments convert into paid enrollments, and enrollments convert
into placements, each with realistic drop-off at every stage. I intentionally built in
business problems — for example, one acquisition channel drives 40% of all leads but
converts at under 2%, while referrals convert 20 times better. I did a full data-quality
pass — missing values, duplicates, invalid dates, referential integrity — before building
anything. Then I built a five-page Power BI dashboard with 20-plus DAX measures covering
conversion rates, ROI, and growth, and wrote fifteen SQL queries answering real business
questions like where the biggest funnel drop-off is and which channels have the worst
ROI. The end deliverable isn't just charts — it's six data-backed recommendations, like
reallocating marketing spend away from the underperforming channel, that I could actually
defend to a CEO."

---

## 3 Resume Bullet Points

- **Built an end-to-end Power BI analytics dashboard** across a 7-table, ~58,000-row
  relational dataset (22,000 students, 160 colleges) simulating an employability
  platform's full student lifecycle, using 20+ DAX measures to track acquisition,
  conversion, revenue and placement KPIs.
- **Diagnosed a 20x acquisition-efficiency gap** between marketing channels (1.4%
  conversion vs. 28.9%) and a 55.6% funnel drop-off at the assessment-to-enrollment
  stage, translating findings into 6 evidence-backed recommendations for budget
  reallocation and operational fixes.
- **Authored 15+ SQL queries and a full data-quality audit** (missing values, duplicates,
  referential integrity, outlier detection) covering ~800 injected data issues across
  three tables, demonstrating a raw-data-to-decision analytics workflow.

---

## 10 Likely Interview Questions & Strong Sample Answers

### 1. Walk me through this project — why did you build it this way?
"I wanted a project that mirrors what a Founder's Office or Business Strategy analyst
actually does: not just visualizing data someone hands you, but going from a business
problem to a data model to KPIs to recommendations. I picked an employability platform
because it has a genuinely interesting multi-stage funnel — leads, registrations,
assessments, enrollments, placements — which forces you to think about conversion at
every stage rather than one flat 'sales' number. I built the dataset myself with
Python so I could control the business logic and bake in realistic problems, rather than
using a generic Kaggle dataset that wouldn't have a story to tell."

### 2. Why is your data synthetic, and how did you make sure it's realistic rather than random?
"I generated it with Python using seeded randomness, but every number is driven by
business logic, not pure randomness. For example, conversion rates vary by acquisition
channel, college tier, and city — Referral and College Partnership channels have
meaningfully higher quality multipliers than paid social, and Tier 1 colleges have higher
completion and placement multipliers than Tier 3. Registration volume follows real
seasonality — it dips during exam months like March and dips again around November-
December, and peaks after results come out in June-July. I also modeled year-over-year
growth per city instead of a flat trend. The result is a dataset where the patterns you'd
expect a real EdTech company to have — quality varies by channel, tier drives outcomes,
some programs underperform — actually show up when you query it."

### 3. What was the biggest insight you found, and how did you find it?
"The biggest one surprised me a little: the largest drop-off in the entire funnel isn't
at acquisition, it's between assessment completion and program enrollment — 55.6% of
students who finish an assessment never enroll in a paid program, which is actually a
bigger relative loss than the registration-to-assessment stage (38.9%). I found it by
building the funnel measures in DAX and then querying the exact same numbers in SQL as a
cross-check. It reframes the whole growth conversation — the instinct is often 'get more
leads,' but the data says the real leak is downstream, in counseling or pricing at the
enrollment decision point, not top-of-funnel volume."

### 4. How did you handle data quality issues?
"I deliberately injected realistic issues into a 'raw' version of three tables — missing
gender and age values, duplicate student records, invalid or future-dated registrations,
age outliers, and a broken foreign key where a student pointed to a college ID that
didn't exist. Then I documented, table by table, what I found and exactly how I handled
it — for example, I imputed missing age using the median for that student's degree and
graduation-year cohort rather than a single global average, because a blanket average
would have distorted the age distribution across different program levels. I was careful
to distinguish real data-entry errors from naturally missing data — incomplete assessment
attempts naturally have no score, and I didn't impute those with zero, because that would
understate genuine engagement; I excluded them from average-score calculations instead."

### 5. Why did you choose these specific DAX measures / why DIVIDE() instead of a slash?
"I used `DIVIDE()` everywhere instead of a plain division operator because it handles
divide-by-zero gracefully without needing a nested IF for every measure — cleaner and
safer, especially once you start slicing by filters that could return zero rows, like a
city with no completed placements yet. I also used `DISTINCTCOUNT` rather than `COUNT` on
ID columns specifically because some students retake assessments — multiple attempts per
student — so a plain row count would have overstated unique student engagement. And I
used variables (`VAR`/`RETURN`) in the more complex measures, like the ranking measures
for 'Top Performing Channel,' both for readability and so the same sub-calculation isn't
evaluated twice."

### 6. How would this scale or change with real production data?
"Three things would change. First, volume and refresh cadence — real production data
would need incremental refresh in Power BI rather than a one-time import, since a live
platform would be adding thousands of rows a day across these tables. Second, I'd expect
messier, less structured data quality issues than the ones I intentionally injected —
real systems have inconsistent formatting, multiple source systems that don't agree on
IDs, and timezone issues in timestamps. Third, I'd want to validate the funnel
definitions with the actual business — for example, confirming exactly what counts as a
'lead' versus a 'registration' with the marketing team, since that boundary is often
fuzzier in practice than in a clean dataset like this one."

### 7. Which channel would you cut, and would you cut it entirely?
"I wouldn't cut Facebook/Instagram Ads entirely — it's still the single largest lead
source, and completely removing it would leave a large volume gap that Referral and
College Partnership Drive can't fill overnight, since both are inherently capacity-
limited (you can only get as many referrals as you have satisfied students, and only as
many partnership leads as you have partnered colleges). What I'd actually do is shift
maybe 25-30% of that budget toward the higher-converting channels as a first test, tighten
audience targeting on what remains, and add a lead-quality gate before the assessment
stage — then re-measure in a quarter before making a bigger cut."

### 8. How do you know your recommendations are actually data-backed and not just plausible-sounding?
"Each recommendation in my insights doc is tied to a specific computed metric, not a
general impression — for example, the recommendation to fix the assessment-to-enrollment
stage cites the exact 55.6% drop-off figure and explicitly compares it to the 38.9%
registration-stage drop-off, so the evidence for prioritizing it over an acquisition fix
is in the numbers themselves, not my opinion. I also cross-validated key numbers in both
DAX and SQL independently to make sure I wasn't looking at a modeling artifact — like the
data model double-counting something because of a wrong relationship cardinality."

### 9. What would you do differently, or what's a limitation of this project?
"The placement-rate calculation only looks at students whose outcome is already tracked
— meaning enough time has passed since they finished a program — rather than all
enrolled students. That's the right way to avoid diluting the rate with students who
haven't had a chance to be placed yet, but it does mean the 'placement rate' isn't
directly comparable to a naive 'placed / total enrolled' number without that caveat, and
I'd want to make that distinction very explicit on a real executive dashboard, probably
with a tooltip, so no one misreads it. I'd also want a longer time window than two years
in a real deployment to properly separate seasonality from genuine trend."

### 10. Why should we trust this project as a signal of your business/strategy thinking, not just Power BI skill?
"Because the dashboard is the last step, not the point. I started from a business problem
— a Founder or Business Head needs to know where growth is coming from and where money
is being wasted — then built the data model, funnel logic and KPIs specifically to answer
that, and I finished with six recommendations phrased the way I'd actually present them
in a room: issue, evidence, implication, suggested action, each one traceable to a real
number in the dataset. The Power BI and DAX skills are how I delivered it, but the harder
part was deciding which questions actually matter to a management team and making sure
the data could answer them credibly."
