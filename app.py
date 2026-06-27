import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="AIR 1 Velocity Tracker", page_icon="🚀", layout="wide")

st.title("🚀 AIR 1 Velocity Engine: Master Command Station")
st.markdown("---")

# ----------------- STORAGE ARCHITECTURE -----------------
LOG_FILE = "study_log.csv"
SYLLABUS_FILE = "syllabus_state.csv"

# Load Daily Study Log
if os.path.exists(LOG_FILE):
    df_log = pd.read_csv(LOG_FILE)
    df_log['Date'] = pd.to_datetime(df_log['Date']).dt.date
else:
    df_log = pd.DataFrame(columns=['Date', 'Hours_Studied', 'Daily_Goal'])

# MASTER SYLLABUS DATA MATRIX
JEE_SYLLABUS = {
    "Physics": ["Units & Dimensions", "Vectors & Kinematics", "Laws of Motion", "Work, Energy & Power", "Rotational Motion", "Gravitation", "Properties of Matter", "Thermodynamics", "SHM & Waves"],
    "Chemistry": ["Mole Concept", "Atomic Structure", "Periodic Table", "Chemical Bonding", "States of Matter", "Thermodynamics", "Chemical Equilibrium", "Ionic Equilibrium", "Redox Reactions"],
    "Math": ["Sets", "Relations & Functions", "Trigonometry", "Quadratic Equations", "Complex Numbers", "Sequences & Series", "Straight Lines", "Circles", "Permutations & Combinations"]
}

# Load or Initialize Permanent Syllabus State
if os.path.exists(SYLLABUS_FILE):
    df_syll = pd.read_csv(SYLLABUS_FILE)
else:
    rows = []
    for sub, chapters in JEE_SYLLABUS.items():
        for ch in chapters:
            rows.append({"Subject": sub, "Chapter": ch, "Completed": False, "Status": "🔴 Backlog"})
    df_syll = pd.DataFrame(rows)

# Create Navigation Tabs
tab1, tab2 = st.tabs(["📊 Daily Desk Station & Logs", "🎯 Smart Syllabus Matrix & Rank Engine"])

# ===================================================
# TAB 1: CLEAN DATA LOGS & PERFORMANCE GRAPH
# ===================================================
with tab1:
    st.subheader("📝 Log Your Study Hours")
    st.markdown("Enter your deep work duration tracked via your PC focus clock.")
    
    col_d, col_h, col_g = st.columns(3)
    with col_d:
        log_date = st.date_input("Select Date", datetime.date.today())
    with col_h:
        study_hours = st.number_input("Study Hours Logged:", min_value=0.0, max_value=24.0, value=6.0, step=0.5)
    with col_g:
        custom_daily_goal = st.slider("Set Target Goal for this Date (Hrs):", min_value=1.0, max_value=14.0, value=6.0, step=0.5)

    if st.button("📥 Commit Entry to Master Cloud Log"):
        if not df_log.empty:
            df_log = df_log[df_log['Date'] != log_date]
        
        new_row = pd.DataFrame({'Date': [log_date], 'Hours_Studied': [study_hours], 'Daily_Goal': [custom_daily_goal]})
        df_log = pd.concat([df_log, new_row], ignore_index=True).sort_values(by='Date')
        df_log.to_csv(LOG_FILE, index=False)
        st.success(f"Log Updated Successfully!")
        st.rerun()

    st.markdown("---")
    
    if not df_log.empty:
        st.subheader("📊 Performance Metrics & Analytics")
        total_hours = df_log['Hours_Studied'].sum()
        avg_hours = df_log['Hours_Studied'].mean()
        net_deficit = total_hours - df_log['Daily_Goal'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Hours Banked", f"{total_hours:.1f} hrs")
        m2.metric("True Daily Velocity Average", f"{avg_hours:.1f} hrs/day")
        m3.metric("Adaptive Goal Buffer", f"{'+' if net_deficit >= 0 else ''}{net_deficit:.1f} hrs", delta_color="normal" if net_deficit >= 0 else "inverse")
        
        st.markdown("### 📈 Historical Execution Trend")
        chart_data = df_log.copy().set_index('Date')
        st.line_chart(chart_data[['Hours_Studied', 'Daily_Goal']])
        
        with st.expander("📂 View Raw History Sheet"):
            st.dataframe(df_log, use_container_width=True)
else:
    st.info("The Master Log is currently blank. Enter your study hours above to initialize tracking!")

# ===================================================
# TAB 2: PERSISTENT SMART MATRIX & RANK ENGINE
# ===================================================
with tab2:
    st.subheader("🛡️ Permanent Chapter Checklist Matrix")
    st.markdown("Check off chapters and update statuses. The system auto-saves parameters securely.")

    sub_col1, sub_col2, sub_col3 = st.columns(3)
    subjects = ["Physics", "Chemistry", "Math"]
    cols_mapped = [sub_col1, sub_col2, sub_col3]
    
    updated_rows = []
    total_backlogs = 0

    for i, sub in enumerate(subjects):
        with cols_mapped[i]:
            st.markdown(f"### {sub} Core Matrix")
            sub_df = df_syll[df_syll["Subject"] == sub]
            
            for idx, row in sub_df.iterrows():
                ch_name = row["Chapter"]
                
                default_checked = bool(row["Completed"])
                default_status_str = str(row["Status"])
                status_options = ["🟢 Completed (PYQs Done)", "🟡 Only Theory", "🔴 Backlog"]
                default_status_idx = status_options.index(default_status_str) if default_status_str in status_options else 2
                
                new_check = st.checkbox(ch_name, value=default_checked, key=f"ch_{sub}_{ch_name}")
                new_status = st.selectbox("Status:", status_options, index=default_status_idx, key=f"st_{sub}_{ch_name}")
                
                if new_status == "🔴 Backlog":
                    total_backlogs += 1
                
                updated_rows.append({"Subject": sub, "Chapter": ch_name, "Completed": new_check, "Status": new_status})

    # Save changes instantly to file storage
    df_new_syll = pd.DataFrame(updated_rows)
    df_new_syll.to_csv(SYLLABUS_FILE, index=False)

    # Calculate completions
    p_sub = df_new_syll[df_new_syll["Subject"] == "Physics"]
    c_sub = df_new_syll[df_new_syll["Subject"] == "Chemistry"]
    m_sub = df_new_syll[df_new_syll["Subject"] == "Math"]

    def calc_pts(df):
        pts = 0
        for _, r in df.iterrows():
            if r["Completed"]:
                pts += 1.0 if r["Status"] == "🟢 Completed (PYQs Done)" else 0.6
        return (pts / len(df)) * 100 if len(df) > 0 else 0.0

    p_cov_pct = calc_pts(p_sub)
    c_cov_pct = calc_pts(c_sub)
    m_cov_pct = calc_pts(m_sub)

    # --------------------------------======================
    # NEW EXTENSION: TIME & EFFORT SUCCESS RANK CALCULATOR
    # --------------------------------======================
    st.markdown("---")
    st.subheader("⚡ Study Consistency & Effort Rank Predictor")
    st.markdown("Evaluate how your current weekly consistency rules map to the national competition tier.")
    
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    with calc_col1:
        days_per_week = st.slider("Effective Study Days Per Week:", min_value=1, max_value=7, value=6)
    with calc_col2:
        hours_per_day = st.slider("Average Self-Study Hours Per Day:", min_value=1.0, max_value=16.0, value=6.0, step=0.5)
    with calc_col3:
        mock_score = st.slider("Target/Current Mock Test Score (Out of 300):", min_value=0, max_value=300, value=180, step=5)

    # Calculation logic for time-based rank velocity
    weekly_hours = days_per_week * hours_per_day
    
    st.markdown(f"#### 📉 Total Weekly Focus Volume: `{weekly_hours:.1f} Hours`")
    
    # Combined predictor using both time and test performance
    if weekly_hours >= 56.0 or mock_score >= 240:
        st.success("🔥 **CRITICAL EXECUTOR: Projected Rank Bracket: AIR Under 500 (IIT Top Branches)**\nAbsolute powerhouse consistency. Maintaining 8+ hours every single day or hitting 240+ marks places you in the national elite tier.")
    elif weekly_hours >= 42.0 or mock_score >= 180:
        st.success("🚀 **HIGH CONSISTENCY: Projected Rank Bracket: AIR 500 - 3,000 (Top IITs / Top NITs)**\nFantastic pace. 6 days a week at 7+ hours or a solid 180+ on mocks gives you severe leverage over 99% of aspirants.")
    elif weekly_hours >= 30.0 or mock_score >= 140:
        st.info("⚡ **COMPETITIVE STABILITY: Projected Rank Bracket: AIR 3,000 - 12,000 (NIT Confirmed Zone)**\nYou have structural stability. You are securely clearing cutoffs and entering solid seat choices. Increasing your study days to 6-7 will scale this rank up fast.")
    elif weekly_hours >= 18.0 or mock_score >= 90:
        st.warning("⚠️ **BORDERLINE PACING: Projected Rank Bracket: AIR 12,000 - 35,000 (State Level / Lower NITs)**\nYour weekly study volume is on the lower side. To secure a high rank, aim to push your weekly desk time past 30 hours.")
    else:
        st.error("🚨 **DANGER RANGE TRACKING: High Risk Zone**\nWeekly hours or test scores are sub-optimal for national engineering tiers. Push your daily study count up immediately to shift your competitive trajectory.")

    # ------------------ SYLLABUS DISPLAYS ------------------
    st.markdown("---")
    st.subheader("🚨 Real-Time Syllabus Command Metrics")
    
    mains_readiness = (p_cov_pct + c_cov_pct + m_cov_pct) / 3.0
    adv_readiness = mains_readiness 

    prog_col1, prog_col2 = st.columns(2)
    with prog_col1:
        st.markdown(f"**Calculated JEE Mains Progress:** `{mains_readiness:.1f}%` Complete")
        st.progress(mains_readiness / 100.0)
    with prog_col2:
        st.markdown(f"**Calculated JEE Advanced Progress:** `{adv_readiness:.1f}%` Complete")
        st.progress(adv_readiness / 100.0)
        
