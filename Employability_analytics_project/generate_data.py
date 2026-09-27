"""
Synthetic dataset generator: Indian Employability/EdTech Platform
2024-2025 Business Operations & Growth Analytics data
Fully fictional. Seeded for reproducibility.
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta

rng = np.random.default_rng(42)

# ----------------------------------------------------------------------
# 0. REFERENCE DATA
# ----------------------------------------------------------------------

# Cities with state, tier of city (metro/tier2/tier3) and a growth multiplier
CITIES = [
    # city, state, city_tier, base_weight, growth_trend (2025 vs 2024), placement_strength
    ("Bengaluru", "Karnataka", "Metro", 14, 1.28, 0.90),
    ("Hyderabad", "Telangana", "Metro", 11, 1.22, 0.86),
    ("Pune", "Maharashtra", "Metro", 10, 1.20, 0.84),
    ("Delhi NCR", "Delhi", "Metro", 13, 1.15, 0.80),
    ("Mumbai", "Maharashtra", "Metro", 9, 1.10, 0.82),
    ("Chennai", "Tamil Nadu", "Metro", 8, 1.18, 0.83),
    ("Kolkata", "West Bengal", "Metro", 5, 1.02, 0.62),
    ("Ahmedabad", "Gujarat", "Tier2", 5, 1.14, 0.70),
    ("Jaipur", "Rajasthan", "Tier2", 4.5, 1.08, 0.58),
    ("Lucknow", "Uttar Pradesh", "Tier2", 4, 0.98, 0.50),
    ("Indore", "Madhya Pradesh", "Tier2", 3.5, 1.16, 0.66),
    ("Nagpur", "Maharashtra", "Tier2", 3, 1.05, 0.55),
    ("Coimbatore", "Tamil Nadu", "Tier2", 3, 1.12, 0.68),
    ("Bhopal", "Madhya Pradesh", "Tier2", 2.5, 0.95, 0.48),
    ("Patna", "Bihar", "Tier3", 3.5, 1.30, 0.38),
    ("Ranchi", "Jharkhand", "Tier3", 2, 1.10, 0.40),
    ("Kanpur", "Uttar Pradesh", "Tier3", 2.5, 0.92, 0.42),
    ("Guwahati", "Assam", "Tier3", 2, 1.20, 0.44),
    ("Nashik", "Maharashtra", "Tier3", 2, 1.05, 0.52),
    ("Varanasi", "Uttar Pradesh", "Tier3", 1.5, 0.90, 0.36),
]
city_df = pd.DataFrame(CITIES, columns=["City", "State", "City_Tier", "Weight", "Growth", "Placement_Strength"])
city_df["Weight"] = city_df["Weight"] / city_df["Weight"].sum()

DEGREES = {
    "B.Tech": ["Computer Science", "Electronics", "Mechanical", "Civil", "Information Technology", "Electrical"],
    "B.Sc": ["Computer Science", "Physics", "Mathematics", "Statistics"],
    "B.Com": ["General", "Honours"],
    "BBA": ["General", "Marketing", "Finance"],
    "MBA": ["Marketing", "Finance", "HR", "Operations"],
    "Diploma": ["Mechanical", "Electrical", "Computer Science"],
    "BCA": ["General"],
}
degree_list = list(DEGREES.keys())
degree_weights = np.array([26, 12, 14, 12, 10, 8, 18], dtype=float)
degree_weights = degree_weights / degree_weights.sum()

ACQ_CHANNELS = [
    # channel, share_of_volume, lead_to_reg_conv, reg_to_assess_conv, cost_per_lead_range, quality_factor
    ("College Partnership Drive", 0.16, 0.62, 0.93, (25, 60), 1.15),
    ("Referral", 0.11, 0.58, 0.90, (10, 30), 1.20),
    ("Organic Search", 0.14, 0.34, 0.82, (0, 5), 1.05),
    ("Google Paid Search", 0.13, 0.24, 0.74, (60, 140), 0.95),
    ("Facebook/Instagram Ads", 0.22, 0.16, 0.58, (35, 90), 0.65),
    ("YouTube Ads", 0.09, 0.19, 0.63, (30, 75), 0.75),
    ("LinkedIn", 0.06, 0.41, 0.88, (90, 220), 1.10),
    ("Webinar/Events", 0.09, 0.46, 0.85, (40, 100), 1.05),
]
channel_names = [c[0] for c in ACQ_CHANNELS]
channel_share = np.array([c[1] for c in ACQ_CHANNELS])
channel_share = channel_share / channel_share.sum()

COLLEGE_TIERS = ["Tier 1", "Tier 2", "Tier 3"]
college_tier_weights = [0.22, 0.45, 0.33]
# Tier -> (assessment completion multiplier, enrollment mult, placement mult)
TIER_EFFECT = {
    "Tier 1": dict(assess=1.12, enroll=1.20, place=1.30, salary_mult=1.35),
    "Tier 2": dict(assess=1.00, enroll=1.00, place=1.00, salary_mult=1.00),
    "Tier 3": dict(assess=0.85, enroll=0.78, place=0.62, salary_mult=0.78),
}
COLLEGE_TYPES = ["Engineering", "Arts & Science", "Management", "Polytechnic", "Autonomous University"]

PROGRAMS = [
    # name, category, fee, capacity_per_cohort, base_completion, base_placement_boost
    ("Full Stack Web Development", "Technical", 24999, 400, 0.72, 1.25),
    ("Data Analytics with Power BI & SQL", "Technical", 19999, 350, 0.78, 1.20),
    ("Data Science & Machine Learning", "Technical", 32999, 300, 0.68, 1.30),
    ("Cloud Computing (AWS/Azure)", "Technical", 27999, 250, 0.70, 1.22),
    ("Digital Marketing Mastery", "Domain", 14999, 350, 0.80, 1.05),
    ("Banking & Finance Job Prep", "Domain", 12999, 300, 0.75, 1.10),
    ("UI/UX Design Foundations", "Technical", 17999, 200, 0.73, 1.08),
    ("Core Engineering Interview Prep", "Domain", 9999, 400, 0.71, 1.12),
    ("Aptitude & Reasoning Mastery", "Aptitude", 4999, 600, 0.84, 0.95),
    ("Communication & Soft Skills Bootcamp", "Soft Skills", 5999, 550, 0.55, 0.85),
    ("Resume & Interview Bootcamp", "Soft Skills", 3999, 500, 0.88, 1.00),
    ("Business Analytics Certification", "Domain", 21999, 220, 0.74, 1.15),
]

OUTCOME_COMPANY_CATS = ["Startup", "MNC/IT Services", "Product Company", "BFSI", "SME/Local Business", "Core Engineering"]
JOB_ROLES = ["Software Engineer", "Data Analyst", "Business Analyst", "Associate Consultant",
             "Digital Marketing Executive", "Operations Executive", "Support Engineer",
             "Trainee Engineer", "Customer Success Associate", "Sales Executive", "UI/UX Designer"]

N_STUDENTS = 22000
N_COLLEGES = 160

START = date(2024, 1, 1)
END = date(2025, 12, 31)
ALL_DAYS = (END - START).days + 1

def random_dates(n, start=START, span=ALL_DAYS, monthly_weights=None):
    """Return n dates between start and start+span, optionally seasonally weighted by month."""
    if monthly_weights is None:
        offsets = rng.integers(0, span, size=n)
        return [start + timedelta(days=int(o)) for o in offsets]
    # build day-level weight array from monthly weights
    days = [start + timedelta(days=i) for i in range(span)]
    w = np.array([monthly_weights[d.month - 1] for d in days], dtype=float)
    w = w / w.sum()
    idx = rng.choice(span, size=n, p=w)
    return [days[i] for i in idx]

# Seasonality: registrations dip in exam months (Mar, Apr, Nov-Dec exams) and peak after
# results (Jun-Aug) and in Jan (new year resolution) — also model 2025 growth over 2024.
MONTHLY_SEASONALITY = [1.05, 0.95, 0.72, 0.80, 1.10, 1.35, 1.40, 1.25, 1.10, 0.95, 0.75, 0.85]

print("Reference data ready.")

# ----------------------------------------------------------------------
# 1. COLLEGES
# ----------------------------------------------------------------------
college_rows = []
for i in range(1, N_COLLEGES + 1):
    city_idx = rng.choice(len(city_df), p=city_df["Weight"].values)
    city_row = city_df.iloc[city_idx]
    tier = rng.choice(COLLEGE_TIERS, p=college_tier_weights)
    ctype = rng.choice(COLLEGE_TYPES, p=[0.38, 0.20, 0.14, 0.16, 0.12])
    name_pool = {
        "Engineering": ["Institute of Technology", "College of Engineering", "Engineering College"],
        "Arts & Science": ["Arts & Science College", "Degree College"],
        "Management": ["School of Management", "Institute of Management Studies"],
        "Polytechnic": ["Polytechnic College", "Institute of Polytechnic"],
        "Autonomous University": ["University", "Autonomous University"],
    }
    suffix = rng.choice(name_pool[ctype])
    college_name = f"{city_row['City']} {suffix} {i:03d}"
    partnership_start = random_dates(1, start=date(2022, 1, 1), span=(date(2024,12,31)-date(2022,1,1)).days)[0]
    college_rows.append(dict(
        College_ID=f"CLG{i:04d}",
        College_Name=college_name,
        College_Type=ctype,
        City=city_row["City"],
        State=city_row["State"],
        Tier=tier,
        Partnership_Date=partnership_start,
    ))
colleges_df = pd.DataFrame(college_rows)
# college weight for student assignment: tier1 colleges get somewhat more volume on average, but tier2 most numerous
tier_pull = colleges_df["Tier"].map({"Tier 1": 1.3, "Tier 2": 1.0, "Tier 3": 0.75}).values
college_probs = tier_pull / tier_pull.sum()

print(f"Colleges: {len(colleges_df)}")

# ----------------------------------------------------------------------
# 2. STUDENTS
# ----------------------------------------------------------------------
FIRST_NAMES_M = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Reyansh","Krishna","Ishaan","Rohan","Kabir",
                  "Aryan","Dev","Karthik","Siddharth","Yash","Nikhil","Rahul","Amit","Sahil","Varun",
                  "Manish","Abhishek","Gaurav","Harsh","Naveen","Rajat","Sandeep","Vikram","Tarun","Puneet"]
FIRST_NAMES_F = ["Ananya","Diya","Ishita","Saanvi","Aadhya","Myra","Pari","Anika","Navya","Riya",
                  "Priya","Sneha","Neha","Pooja","Kavya","Shreya","Divya","Nisha","Ritika","Simran",
                  "Meera","Aishwarya","Swati","Tanvi","Preeti","Kriti","Bhavya","Namrata","Radhika","Sanya"]
LAST_NAMES = ["Sharma","Verma","Gupta","Patel","Reddy","Iyer","Nair","Singh","Kumar","Rao",
              "Mehta","Joshi","Chatterjee","Bose","Das","Pillai","Naidu","Menon","Agarwal","Kapoor",
              "Malhotra","Chauhan","Bhatt","Desai","Trivedi","Yadav","Mishra","Pandey","Saxena","Thakur"]

def make_name():
    gender = rng.choice(["Male", "Female"], p=[0.58, 0.42])
    fname = rng.choice(FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F)
    lname = rng.choice(LAST_NAMES)
    return f"{fname} {lname}", gender

channel_idx = rng.choice(len(ACQ_CHANNELS), size=N_STUDENTS, p=channel_share)
city_idx_arr = rng.choice(len(city_df), size=N_STUDENTS, p=city_df["Weight"].values)

# registration dates: seasonality + YoY growth per city (2025 volume = 2024 volume * city growth)
# build weights across full 2-year span combining month seasonality and yearly growth trend
days_all = [START + timedelta(days=i) for i in range(ALL_DAYS)]

student_rows = []
for n in range(N_STUDENTS):
    city_row = city_df.iloc[city_idx_arr[n]]
    channel = ACQ_CHANNELS[channel_idx[n]]
    # date weighting: seasonality x (growth factor if in 2025)
    # sample month-based via seasonality then pick year weighted by growth
    year = rng.choice([2024, 2025], p=[1/(1+city_row["Growth"]), city_row["Growth"]/(1+city_row["Growth"])])
    month = rng.choice(range(1, 13), p=np.array(MONTHLY_SEASONALITY)/sum(MONTHLY_SEASONALITY))
    day = int(rng.integers(1, 28))
    reg_date = date(year, month, day)
    if reg_date > END:
        reg_date = END - timedelta(days=int(rng.integers(0, 30)))

    degree = rng.choice(degree_list, p=degree_weights)
    stream = rng.choice(DEGREES[degree])
    grad_year = reg_date.year if reg_date.month <= 5 else reg_date.year + 1
    grad_year = int(np.clip(grad_year + rng.integers(-1, 2), 2023, 2026))
    age = int(np.clip(rng.normal(21.5, 1.6), 19, 28))
    name, gender = make_name()

    # college assignment weighted by tier & same-state preference (70% same state as college)
    college_choice_idx = rng.choice(len(colleges_df), p=college_probs)
    college_row = colleges_df.iloc[college_choice_idx]

    student_rows.append(dict(
        Student_ID=f"STU{n+1:06d}",
        Student_Name=name,
        Gender=gender,
        Age=age,
        Graduation_Year=grad_year,
        Degree=degree,
        Stream=stream,
        College_ID=college_row["College_ID"],
        City=city_row["City"],
        State=city_row["State"],
        Registration_Date=reg_date,
        Acquisition_Channel=channel[0],
    ))

students_df = pd.DataFrame(student_rows)
print(f"Students: {len(students_df)}")

# merge helper columns for probability computation
students_df = students_df.merge(colleges_df[["College_ID", "Tier"]], on="College_ID", how="left")
students_df = students_df.merge(city_df[["City", "Placement_Strength", "City_Tier"]], on="City", how="left")
chan_lookup = {c[0]: c for c in ACQ_CHANNELS}
students_df["chan_assess_conv"] = students_df["Acquisition_Channel"].map(lambda c: chan_lookup[c][3])
students_df["chan_quality"] = students_df["Acquisition_Channel"].map(lambda c: chan_lookup[c][5])
students_df["tier_assess_mult"] = students_df["Tier"].map(lambda t: TIER_EFFECT[t]["assess"])
students_df["tier_enroll_mult"] = students_df["Tier"].map(lambda t: TIER_EFFECT[t]["enroll"])
students_df["tier_place_mult"] = students_df["Tier"].map(lambda t: TIER_EFFECT[t]["place"])
students_df["tier_salary_mult"] = students_df["Tier"].map(lambda t: TIER_EFFECT[t]["salary_mult"])

# ----------------------------------------------------------------------
# 3. ASSESSMENTS
# ----------------------------------------------------------------------
# Probability a registered student starts an assessment
p_start = (students_df["chan_assess_conv"] * students_df["tier_assess_mult"] * students_df["chan_quality"]).clip(0.05, 0.97)
starts_assessment = rng.random(len(students_df)) < p_start

assess_rows = []
assess_id = 1
ASSESS_TYPES = ["Aptitude Test", "Technical Assessment", "Communication Assessment", "Full Employability Test"]

for idx, row in students_df[starts_assessment].iterrows():
    n_attempts = 1 + (rng.random() < 0.18) + (rng.random() < 0.05)  # some retake
    base_complete_p = np.clip(0.80 * row["tier_assess_mult"] * row["chan_quality"], 0.15, 0.97)
    reg_date = row["Registration_Date"]
    for attempt in range(1, int(n_attempts) + 1):
        assess_date = reg_date + timedelta(days=int(rng.integers(1, 25)) * attempt)
        if assess_date > END:
            assess_date = END
        completed = rng.random() < (base_complete_p if attempt == 1 else min(base_complete_p + 0.15, 0.98))
        status = "Completed" if completed else rng.choice(["Incomplete", "Dropped Off"], p=[0.5, 0.5])
        # scores only meaningful if completed
        if completed:
            skill_center = 55 + 20 * (row["tier_assess_mult"] - 1) + rng.normal(0, 12)
            aptitude = np.clip(skill_center + rng.normal(0, 10), 10, 99)
            technical = np.clip(skill_center + rng.normal(-3, 14), 5, 99)
            comm = np.clip(skill_center + rng.normal(5, 11), 15, 99)
            overall = round((aptitude * 0.35 + technical * 0.35 + comm * 0.30), 1)
        else:
            aptitude = technical = comm = overall = np.nan
        assess_rows.append(dict(
            Assessment_ID=f"AST{assess_id:07d}",
            Student_ID=row["Student_ID"],
            Assessment_Date=assess_date,
            Assessment_Type=rng.choice(ASSESS_TYPES, p=[0.35, 0.30, 0.15, 0.20]),
            Score=overall,
            Aptitude_Score=round(aptitude, 1) if completed else np.nan,
            Technical_Score=round(technical, 1) if completed else np.nan,
            Communication_Score=round(comm, 1) if completed else np.nan,
            Completion_Status=status,
            Attempt_Number=attempt,
        ))
        assess_id += 1

assessments_df = pd.DataFrame(assess_rows)
print(f"Assessments: {len(assessments_df)}")

# a student "completed" assessment if any row says Completed
completed_students = set(assessments_df.loc[assessments_df.Completion_Status == "Completed", "Student_ID"])
students_df["Assessment_Completed_Flag"] = students_df["Student_ID"].isin(completed_students)
print(f"Students with completed assessment: {students_df['Assessment_Completed_Flag'].sum()}")

# ----------------------------------------------------------------------
# 4. PROGRAMS
# ----------------------------------------------------------------------
program_rows = []
for i, (pname, cat, fee, cap, comp_rate, place_boost) in enumerate(PROGRAMS, start=1):
    # multiple cohorts across 2024-2025 (quarterly-ish)
    program_rows.append(dict(
        Program_ID=f"PRG{i:03d}",
        Program_Name=pname,
        Program_Category=cat,
        Fee=fee,
        Capacity=cap,
        Base_Completion_Rate=comp_rate,
        Placement_Boost=place_boost,
    ))
programs_df = pd.DataFrame(program_rows)
# add Start_Date / End_Date per program as representative cohort window (for reference dimension table use we keep one row per program with earliest cohort start & typical duration)
programs_df["Start_Date"] = date(2024, 1, 15)
programs_df["End_Date"] = programs_df["Start_Date"].apply(lambda d: d + timedelta(days=70))
print(f"Programs: {len(programs_df)}")


# ----------------------------------------------------------------------
# 5. ENROLLMENTS  (only students who completed assessment are eligible)
# ----------------------------------------------------------------------
eligible = students_df[students_df["Assessment_Completed_Flag"]].copy()

# Deliberate problem: Communication & Soft Skills Bootcamp gets high enrollment but low completion later (handled in outcomes via completion flag on enrollment)
program_weights = np.array([  # relative popularity
    18, 16, 10, 9, 14, 8, 7, 10, 20, 22, 12, 6
], dtype=float)
program_weights = program_weights / program_weights.sum()

enroll_rows = []
enroll_id = 1
for idx, row in eligible.iterrows():
    p_enroll = np.clip(0.42 * row["tier_enroll_mult"] * row["chan_quality"], 0.05, 0.95)
    if rng.random() >= p_enroll:
        continue
    prog_idx = rng.choice(len(programs_df), p=program_weights)
    prog = programs_df.iloc[prog_idx]
    # find student's latest completed assessment date as anchor
    stu_assess = assessments_df[(assessments_df.Student_ID == row["Student_ID"]) & (assessments_df.Completion_Status == "Completed")]
    anchor = stu_assess["Assessment_Date"].max()
    enroll_date = anchor + timedelta(days=int(rng.integers(2, 20)))
    if enroll_date > END:
        enroll_date = END
    payment_status = rng.choice(["Fully Paid", "Partially Paid", "Refunded", "Pending"], p=[0.72, 0.16, 0.04, 0.08])
    if payment_status == "Fully Paid":
        amount_paid = prog["Fee"]
    elif payment_status == "Partially Paid":
        amount_paid = round(prog["Fee"] * rng.uniform(0.3, 0.7))
    elif payment_status == "Refunded":
        amount_paid = 0
    else:
        amount_paid = 0
    # completion of the program (drives placement eligibility) — soft skills bootcamp deliberately weak
    comp_rate = prog["Base_Completion_Rate"] * row["tier_enroll_mult"] * (0.9 + 0.2 * row["chan_quality"])
    comp_rate = float(np.clip(comp_rate, 0.1, 0.97))
    p_progress = max(0.02, (1 - comp_rate) * 0.35)
    p_dropped = max(0.02, (1 - comp_rate) * 0.65)
    probs = np.array([comp_rate, p_progress, p_dropped])
    probs = probs / probs.sum()
    enrollment_status = rng.choice(["Completed", "In Progress", "Dropped"], p=probs)
    enroll_rows.append(dict(
        Enrollment_ID=f"ENR{enroll_id:07d}",
        Student_ID=row["Student_ID"],
        Program_ID=prog["Program_ID"],
        Enrollment_Date=enroll_date,
        Enrollment_Status=enrollment_status,
        Payment_Status=payment_status,
        Amount_Paid=int(amount_paid),
    ))
    enroll_id += 1

enrollments_df = pd.DataFrame(enroll_rows)
print(f"Enrollments: {len(enrollments_df)}")

# ----------------------------------------------------------------------
# 6. OUTCOMES / PLACEMENTS (only for students whose enrollment status == Completed
#     AND enough time has elapsed since enrollment, i.e. enrolled before ~ Oct 2025)
# ----------------------------------------------------------------------
completed_enroll = enrollments_df[enrollments_df.Enrollment_Status == "Completed"].copy()
completed_enroll = completed_enroll.merge(students_df[["Student_ID", "tier_place_mult", "tier_salary_mult",
                                                        "Placement_Strength", "Degree"]], on="Student_ID", how="left")
completed_enroll = completed_enroll.merge(programs_df[["Program_ID", "Placement_Boost", "Program_Category"]], on="Program_ID", how="left")

cutoff_for_placement = date(2025, 10, 15)  # need lead time to place
completed_enroll = completed_enroll[completed_enroll.Enrollment_Date <= cutoff_for_placement]

outcome_rows = []
outcome_id = 1
BASE_SALARY_BY_CATEGORY = {
    "Startup": (280000, 550000), "MNC/IT Services": (350000, 650000), "Product Company": (500000, 1100000),
    "BFSI": (320000, 600000), "SME/Local Business": (200000, 380000), "Core Engineering": (300000, 520000),
}
for idx, row in completed_enroll.iterrows():
    p_place = np.clip(0.5 * row["tier_place_mult"] * row["Placement_Boost"] * (0.6 + 0.5 * row["Placement_Strength"]), 0.05, 0.95)
    placed = rng.random() < p_place
    outcome_date = row["Enrollment_Date"] + timedelta(days=int(rng.integers(30, 150)))
    if outcome_date > date(2025, 12, 31):
        outcome_date = date(2025, 12, 31)
    if placed:
        status = "Placed"
        company_cat = rng.choice(list(BASE_SALARY_BY_CATEGORY.keys()),
                                  p=[0.20, 0.28, 0.14, 0.13, 0.16, 0.09])
        lo, hi = BASE_SALARY_BY_CATEGORY[company_cat]
        salary = int(np.clip(rng.uniform(lo, hi) * row["tier_salary_mult"], 150000, 2200000))
        job_role = rng.choice(JOB_ROLES)
        source = rng.choice(["Campus Drive", "Platform Job Board", "Referral", "Direct Company Tie-up"],
                             p=[0.30, 0.35, 0.15, 0.20])
    else:
        status = rng.choice(["Not Placed", "Actively Searching"], p=[0.4, 0.6])
        company_cat = None
        salary = None
        job_role = None
        source = None
    outcome_rows.append(dict(
        Outcome_ID=f"OUT{outcome_id:07d}",
        Student_ID=row["Student_ID"],
        Outcome_Date=outcome_date,
        Placement_Status=status,
        Company_Category=company_cat,
        Salary=salary,
        Job_Role=job_role,
        Placement_Source=source,
    ))
    outcome_id += 1

outcomes_df = pd.DataFrame(outcome_rows)
print(f"Outcomes: {len(outcomes_df)}  | Placed: {(outcomes_df.Placement_Status=='Placed').sum()}")


# ----------------------------------------------------------------------
# 7. MARKETING / ACQUISITION (daily grain by channel)
# ----------------------------------------------------------------------
# Build from actual registrations per channel per day, then back out Leads/Spend/funnel
# using channel-specific conversion & cost parameters (adds realistic ROI variation).
reg_daily = (students_df.groupby(["Registration_Date", "Acquisition_Channel"])
             .size().reset_index(name="Registrations"))

# ensure every (date, channel) combo exists for a clean daily table (fill zeros)
all_dates = pd.DataFrame({"Registration_Date": days_all})
all_dates["key"] = 1
chan_df = pd.DataFrame({"Acquisition_Channel": channel_names})
chan_df["key"] = 1
grid = all_dates.merge(chan_df, on="key").drop(columns="key")
mkt = grid.merge(reg_daily, on=["Registration_Date", "Acquisition_Channel"], how="left")
mkt["Registrations"] = mkt["Registrations"].fillna(0).astype(int)

def chan_params(c):
    return chan_lookup[c]

leads = []
started = []
completed_a = []
conversions = []
spend = []
for _, r in mkt.iterrows():
    cp = chan_params(r["Acquisition_Channel"])
    # tuple layout: (name, share, lead_to_reg_conv, reg_to_assess_conv, cost_range, quality)
    cpl_lo, cpl_hi = cp[4]
    quality = cp[5]
    regs = int(r["Registrations"])
    # leads implied from registrations & lead->reg conversion, with noise
    lead_conv = cp[2]
    n_leads = int(regs / max(lead_conv, 0.05) * rng.uniform(0.85, 1.15)) if regs > 0 else int(rng.poisson(2))
    # use binomial draws (not truncating multiplication) so small daily counts don't
    # systematically collapse to zero — preserves true long-run conversion rates
    p_started = float(np.clip(cp[3] * rng.uniform(0.9, 1.1), 0.05, 0.99))
    n_started = int(rng.binomial(regs, p_started)) if regs > 0 else 0
    p_completed = float(np.clip(0.82 * quality * rng.uniform(0.85, 1.15), 0.05, 0.99))
    n_completed = int(rng.binomial(n_started, p_completed)) if n_started > 0 else 0
    p_conv = float(np.clip(0.45 * quality * rng.uniform(0.8, 1.2), 0.03, 0.95))
    n_conversions = int(rng.binomial(n_completed, p_conv)) if n_completed > 0 else 0
    unit_cost = rng.uniform(cpl_lo, cpl_hi)
    daily_spend = round(n_leads * unit_cost, 2)
    leads.append(n_leads); started.append(n_started); completed_a.append(n_completed)
    conversions.append(n_conversions); spend.append(daily_spend)

mkt["Leads"] = leads
mkt["Assessment_Started"] = started
mkt["Assessment_Completed"] = completed_a
mkt["Conversions"] = conversions
mkt["Marketing_Spend"] = spend
mkt = mkt.rename(columns={"Registration_Date": "Date", "Acquisition_Channel": "Channel"})
mkt = mkt[["Date", "Channel", "Leads", "Registrations", "Assessment_Started",
           "Assessment_Completed", "Conversions", "Marketing_Spend"]]
print(f"Marketing rows: {len(mkt)}")


# ----------------------------------------------------------------------
# 8. FINALIZE CLEAN DIMENSION/FACT TABLES (drop helper cols)
# ----------------------------------------------------------------------
students_clean = students_df[["Student_ID","Student_Name","Gender","Age","Graduation_Year","Degree",
                               "Stream","College_ID","City","State","Registration_Date","Acquisition_Channel"]].copy()
colleges_clean = colleges_df.copy()
colleges_clean["Student_Count"] = colleges_clean["College_ID"].map(students_clean["College_ID"].value_counts()).fillna(0).astype(int)
colleges_clean = colleges_clean[["College_ID","College_Name","College_Type","City","State","Tier","Student_Count","Partnership_Date"]]
assessments_clean = assessments_df.copy()
programs_clean = programs_df[["Program_ID","Program_Name","Program_Category","Start_Date","End_Date","Fee","Capacity"]].copy()
enrollments_clean = enrollments_df.copy()
outcomes_clean = outcomes_df.copy()
marketing_clean = mkt.copy()

# ----------------------------------------------------------------------
# 9. INTRODUCE REALISTIC DATA-QUALITY ISSUES INTO A "RAW" EXPORT
#    (mirrors what you'd receive from source systems before cleaning)
# ----------------------------------------------------------------------
dq_report = {}

# --- Students raw: missing values, duplicates, invalid dates, bad ages
students_raw = students_clean.copy()
n = len(students_raw)

# 1) Missing Gender / Age / City (MCAR ~1-2%)
miss_idx = rng.choice(n, size=int(n*0.012), replace=False)
students_raw.loc[miss_idx, "Gender"] = np.nan
miss_idx2 = rng.choice(n, size=int(n*0.008), replace=False)
students_raw.loc[miss_idx2, "Age"] = np.nan

# 2) Duplicate records (same student appears twice - common export duplication)
dup_sample = students_raw.sample(n=int(n*0.006), random_state=1)
students_raw = pd.concat([students_raw, dup_sample], ignore_index=True)

# 3) Invalid / impossible dates (typo years, future dates)
bad_date_idx = rng.choice(len(students_raw), size=int(n*0.004), replace=False)
for i in bad_date_idx:
    choice = rng.choice(["future", "typo_year", "blank"])
    if choice == "future":
        students_raw.loc[i, "Registration_Date"] = date(2026, rng.integers(1,13), rng.integers(1,28))
    elif choice == "typo_year":
        students_raw.loc[i, "Registration_Date"] = date(2004, rng.integers(1,13), rng.integers(1,28))
    else:
        students_raw.loc[i, "Registration_Date"] = pd.NaT

# 4) Outlier / impossible ages
out_idx = rng.choice(len(students_raw), size=int(n*0.003), replace=False)
students_raw.loc[out_idx, "Age"] = rng.choice([14, 15, 63, 71], size=len(out_idx))

# 5) Referential integrity break: a few students point to a College_ID that doesn't exist
bad_ref_idx = rng.choice(len(students_raw), size=int(n*0.002), replace=False)
students_raw.loc[bad_ref_idx, "College_ID"] = "CLG9999"

dq_report["students"] = dict(
    total_raw_rows=len(students_raw),
    missing_gender=int(students_raw["Gender"].isna().sum()),
    missing_age=int(students_raw["Age"].isna().sum()),
    duplicate_rows=int(students_raw.duplicated(subset=["Student_ID"]).sum()),
    invalid_or_missing_dates=int(students_raw["Registration_Date"].isna().sum()) + len(bad_date_idx) - int(students_raw["Registration_Date"].isna().sum()),
    age_outliers=len(out_idx),
    broken_college_refs=len(bad_ref_idx),
)

# --- Assessments raw: missing scores already natural (incomplete attempts); add a few negative/impossible scores + duplicates
assessments_raw = assessments_clean.copy()
m = len(assessments_raw)
neg_idx = rng.choice(m, size=int(m*0.0015), replace=False)
assessments_raw.loc[neg_idx, "Score"] = -assessments_raw.loc[neg_idx, "Score"].abs()
over_idx = rng.choice(m, size=int(m*0.001), replace=False)
assessments_raw.loc[over_idx, "Technical_Score"] = 140  # impossible >100 score
dup_a = assessments_raw.sample(n=int(m*0.004), random_state=2)
assessments_raw = pd.concat([assessments_raw, dup_a], ignore_index=True)

dq_report["assessments"] = dict(
    total_raw_rows=len(assessments_raw),
    negative_scores=len(neg_idx),
    out_of_range_scores_gt_100=len(over_idx),
    duplicate_rows=int(assessments_raw.duplicated(subset=["Assessment_ID"]).sum()),
    naturally_missing_scores_incomplete_attempts=int(assessments_clean["Score"].isna().sum()),
)

# --- Outcomes raw: salary outliers + missing company category for placed (bad data entry)
outcomes_raw = outcomes_clean.copy()
k = len(outcomes_raw)
placed_idx = outcomes_raw[outcomes_raw.Placement_Status == "Placed"].index
sal_out_idx = rng.choice(placed_idx, size=max(1,int(len(placed_idx)*0.004)), replace=False)
outcomes_raw.loc[sal_out_idx, "Salary"] = outcomes_raw.loc[sal_out_idx, "Salary"] * 12  # entered as monthly instead of annual, by mistake
entry_err_idx = rng.choice(placed_idx, size=max(1,int(len(placed_idx)*0.003)), replace=False)
outcomes_raw.loc[entry_err_idx, "Company_Category"] = np.nan

dq_report["outcomes"] = dict(
    total_raw_rows=len(outcomes_raw),
    salary_unit_outliers=len(sal_out_idx),
    missing_company_category_for_placed=len(entry_err_idx),
)

print("DQ issues injected. Report:")
for k_, v_ in dq_report.items():
    print(k_, v_)


# ----------------------------------------------------------------------
# 10. EXPORT
# ----------------------------------------------------------------------
import os, json
os.makedirs("data/clean", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)

# CLEAN (model-ready) tables -> used to build the Power BI data model
students_clean.to_csv("data/clean/Students.csv", index=False)
colleges_clean.to_csv("data/clean/Colleges.csv", index=False)
assessments_clean.to_csv("data/clean/Assessments.csv", index=False)
programs_clean.to_csv("data/clean/Programs.csv", index=False)
enrollments_clean.to_csv("data/clean/Enrollments.csv", index=False)
outcomes_clean.to_csv("data/clean/Outcomes.csv", index=False)
marketing_clean.to_csv("data/clean/Marketing.csv", index=False)

# RAW (pre-cleaning, with intentional DQ issues) — for the data-quality write-up / demo
students_raw.to_csv("data/raw/Students_RAW.csv", index=False)
assessments_raw.to_csv("data/raw/Assessments_RAW.csv", index=False)
outcomes_raw.to_csv("data/raw/Outcomes_RAW.csv", index=False)

with open("data/dq_report.json", "w") as f:
    json.dump(dq_report, f, indent=2, default=str)

# Also a single multi-sheet Excel workbook for easy Power BI import
with pd.ExcelWriter("data/Employability_Platform_Dataset.xlsx", engine="openpyxl") as writer:
    students_clean.to_excel(writer, sheet_name="Students", index=False)
    colleges_clean.to_excel(writer, sheet_name="Colleges", index=False)
    assessments_clean.to_excel(writer, sheet_name="Assessments", index=False)
    programs_clean.to_excel(writer, sheet_name="Programs", index=False)
    enrollments_clean.to_excel(writer, sheet_name="Enrollments", index=False)
    outcomes_clean.to_excel(writer, sheet_name="Outcomes", index=False)
    marketing_clean.to_excel(writer, sheet_name="Marketing", index=False)

print("\n--- ROW COUNTS (clean model-ready tables) ---")
for name, df_ in [("Students", students_clean), ("Colleges", colleges_clean),
                   ("Assessments", assessments_clean), ("Programs", programs_clean),
                   ("Enrollments", enrollments_clean), ("Outcomes", outcomes_clean),
                   ("Marketing", marketing_clean)]:
    print(f"{name}: {len(df_):,}")
print("TOTAL ROWS:", sum(len(x) for x in [students_clean,colleges_clean,assessments_clean,programs_clean,enrollments_clean,outcomes_clean,marketing_clean]))
