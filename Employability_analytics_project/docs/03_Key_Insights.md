# Key Insights & Business Recommendations

All figures below are computed directly from the cleaned dataset (`/data/clean/`) and
reproducible via `/sql/business_analysis_queries.sql`.

## Headline Numbers (2024–2025)

| Metric | Value |
|---|---|
| Total Students Registered | 22,000 |
| Total Leads | 78,473 |
| Assessments Completed (unique students) | 13,439 (61.1% of registrations) |
| Program Enrollments | 5,968 |
| Placement Rate (of outcome-tracked students) | 55.6% |
| Total Revenue | ₹7.24 crore |
| Total Marketing Spend | ₹48.1 lakh |
| Average Placed Salary | ₹5.40 lakh |
| Overall Lead → Enrollment Conversion | 7.6% |

---

## Key Insights

1. **Channel volume and channel quality are inversely related.** Facebook/Instagram Ads
   brings in the single largest volume of leads (30,438 — 39% of all leads) but converts
   at just **1.43%**, the lowest of any channel. Referral (26.8%) and College Partnership
   Drive (28.9%) convert roughly **19–20x better**, despite generating far fewer leads.

2. **College Partnership Drive and Referral are the most capital-efficient channels.**
   Combined they cost ₹3.13 lakh in spend for 2,682 conversions (~₹117/conversion), while
   Facebook/Instagram Ads and YouTube Ads together cost ₹25.0 lakh for only 696 conversions
   (~₹3,600/conversion) — roughly **30x more expensive per converted student**.

3. **College tier is the strongest single predictor of placement outcomes.** Placement
   rate steps down sharply by tier: **Tier 1 colleges 69.2%**, **Tier 2 52.0%**,
   **Tier 3 34.1%** — a 35-point spread between the best and weakest tier.

4. **The steepest funnel drop-off is between assessment completion and program
   enrollment, not at the top of the funnel.** Of students who complete an assessment,
   **55.6% do not go on to enroll** in a paid program — a larger relative loss than the
   38.9% drop-off between registration and assessment completion. This points to a
   post-assessment conversion/counseling gap, not an acquisition problem.

5. **"Communication & Soft Skills Bootcamp" is the weakest program on completion.**
   It has strong enrollment volume but only a **65.0%** completion rate — 15–29 points
   below every other program (next-lowest is Data Science & ML at 79.9%; the strongest,
   Resume & Interview Bootcamp, completes at 94.0%).

6. **Growth is fastest in metros, but a few Tier-3 cities are growing meaningfully
   despite weak placement.** Bengaluru (+38.9% YoY), Chennai (+31.2%) and Hyderabad
   (+30.4%) lead overall growth, but Patna — a Tier-3 city — also grew **+23.7% YoY**
   while recording one of the **lowest placement rates** in the dataset. Growth in
   student intake is outpacing the platform's ability to convert that intake into
   outcomes in that specific city.

7. **Two cities are shrinking:** Bhopal (-7.0% YoY) and Varanasi (-4.7% YoY) are the
   only two cities with negative registration growth between 2024 and 2025.

8. **Maharashtra is the single largest revenue state** (₹1.67 crore, driven by Pune and
   Mumbai combined), followed by Karnataka (₹0.98 crore) and Delhi (₹0.82 crore) —
   together the top 3 states contribute roughly 46% of total revenue.

---

## Business Recommendations

**1. Reallocate acquisition spend away from Facebook/Instagram Ads toward Referral and
College Partnership Drive.**
*Evidence:* Facebook/Instagram Ads' conversion rate (1.43%) is ~20x lower than Referral
(26.8%) despite receiving the largest share of total marketing spend (₹19.6 lakh of
₹48.1 lakh, ~41%).
*Action:* Shift 25–30% of the Facebook/Instagram budget to a structured referral
incentive program and expand College Partnership Drive to additional Tier 1/2 colleges,
where both channels already show proven efficiency.

**2. Fix the assessment-to-enrollment conversion gap before spending more on acquisition.**
*Evidence:* 55.6% of students who complete an assessment never enroll — the single
largest leak in the funnel, larger than any acquisition-stage loss.
*Action:* Introduce a structured counseling/nudge sequence (call or WhatsApp follow-up
within 48 hours of assessment completion) and test program-fee financing or EMI options
for price-sensitive segments, since this is a conversion problem, not a volume problem.

**3. Redesign or retire the Communication & Soft Skills Bootcamp in its current form.**
*Evidence:* 65.0% completion rate, the lowest of all 12 programs, dragging down overall
enrollment-to-completion performance.
*Action:* Audit the program's format and pacing against Resume & Interview Bootcamp
(94.0% completion) — likely a duration, engagement, or scheduling issue rather than
demand, since enrollment volume into the program is healthy.

**4. Direct targeted operational support to Tier 3 colleges, rather than only chasing new
volume there.**
*Evidence:* Tier 3 placement rate (34.1%) is less than half of Tier 1 (69.2%), and
Tier-3 city Patna is simultaneously one of the fastest-growing cities (+23.7% YoY) and
one of the weakest on placement — a growth/quality mismatch that will compound if
unaddressed.
*Action:* Before scaling acquisition further in Tier 3 cities, invest in employer
partnerships and placement-readiness support specifically for Tier 3 colleges; growing
intake without growing outcomes will hurt the platform's placement-rate KPI and its
credibility with those colleges.

**5. Protect and expand what's working in the top revenue states.**
*Evidence:* Maharashtra, Karnataka and Delhi together generate ~46% of total revenue,
led by strong metro performance (Bengaluru, Pune, Mumbai).
*Action:* Prioritize any new premium/high-fee program launches (Data Science & ML, Cloud
Computing) in these states first, where willingness-to-pay and placement outcomes are
both already validated.

**6. Investigate the two declining cities before they compound further.**
*Evidence:* Bhopal and Varanasi are the only cities with negative YoY registration
growth (-7.0% and -4.7% respectively).
*Action:* A focused root-cause review (college partnership health, local competition,
channel mix in that city) is warranted before the next acquisition budget cycle, rather
than assuming national trends apply uniformly.
