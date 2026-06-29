import streamlit as st
import pandas as pd
import datetime
import os
import google.generativeai as genai

st.set_page_config(page_title="AIR 1 Velocity Tracker", page_icon="🚀", layout="wide")

st.title("🚀 AIR 1 Velocity Engine: Ultimate Command Station")
st.markdown("---")

# ----------------- STORAGE ARCHITECTURE -----------------
LOG_FILE = "study_log.csv"
SYLLABUS_FILE = "syllabus_state.csv"

if os.path.exists(LOG_FILE):
    df_log = pd.read_csv(LOG_FILE)
    df_log['Date'] = pd.to_datetime(df_log['Date']).dt.date
else:
    df_log = pd.DataFrame(columns=['Date', 'Hours_Studied', 'Daily_Goal'])

JEE_SYLLABUS = {
    "Physics": ["Units & Dimensions", "Vectors & Kinematics", "Laws of Motion", "Work, Energy & Power", "Rotational Motion", "Gravitation", "Properties of Matter", "Thermodynamics", "SHM & Waves"],
    "Chemistry": ["Mole Concept", "Atomic Structure", "Periodic Table", "Chemical Bonding", "States of Matter", "Thermodynamics", "Chemical Equilibrium", "Ionic Equilibrium", "Redox Reactions"],
    "Math": ["Sets", "Relations & Functions", "Trigonometry", "Quadratic Equations", "Complex Numbers", "Sequences & Series", "Straight Lines", "Circles", "Permutations & Combinations"]
}

if os.path.exists(SYLLABUS_FILE):
    df_syll = pd.read_csv(SYLLABUS_FILE)
else:
    rows = []
    for sub, chapters in JEE_SYLLABUS.items():
        for ch in chapters:
            rows.append({"Subject": sub, "Chapter": ch, "Completed": False, "Status": "🔴 Backlog"})
    df_syll = pd.DataFrame(rows)

# Create Navigation Tabs (Added Tab 3!)
tab1, tab2, tab3 = st.tabs(["📊 Daily Desk Station & Logs", "🎯 Smart Syllabus Matrix & Rank Engine", "📝 AI Infinite Practice Arena"])

# ===================================================
# TAB 1: DATA LOGS & PERFORMANCE GRAPH
# ===================================================
with tab1:
    st.subheader("📝 Log Your Study Hours")
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
        
        chart_data = df_log.copy().set_index('Date')
        st.line_chart(chart_data[['Hours_Studied', 'Daily_Goal']])

# ===================================================
# TAB 2: SMART MATRIX & RANK ENGINE
# ===================================================
with tab2:
    st.subheader("🛡️ Permanent Chapter Checklist Matrix")
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

    df_new_syll = pd.DataFrame(updated_rows)
    df_new_syll.to_csv(SYLLABUS_FILE, index=False)

    def calc_pts(df):
        pts = 0
        for _, r in df.iterrows():
            if r["Completed"]:
                pts += 1.0 if r["Status"] == "🟢 Completed (PYQs Done)" else 0.6
        return (pts / len(df)) * 100 if len(df) > 0 else 0.0

    p_cov_pct = calc_pts(df_new_syll[df_new_syll["Subject"] == "Physics"])
    c_cov_pct = calc_pts(df_new_syll[df_new_syll["Subject"] == "Chemistry"])
    m_cov_pct = calc_pts(df_new_syll[df_new_syll["Subject"] == "Math"])

    st.markdown("---")
    st.subheader("⚡ Study Consistency & Effort Rank Predictor")
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    with calc_col1:
        days_per_week = st.slider("Effective Study Days Per Week:", min_value=1, max_value=7, value=1)
    with calc_col2:
        hours_per_day = st.slider("Average Self-Study Hours Per Day:", min_value=1.0, max_value=14.0, value=1.0, step=0.5)
    with calc_col3:
        mock_score = st.slider("Target/Current Mock Test Score (Out of 300):", min_value=0, max_value=300, value=0, step=1)

    weekly_hours = days_per_week * hours_per_day
    
    if weekly_hours >= 56.0 and mock_score >= 240:
        st.success("🔥 **CRITICAL EXECUTOR: Projected Rank Bracket: AIR Under 500**")
    elif weekly_hours >= 45.0 and mock_score >= 180:
        st.success("🚀 **HIGH CONSISTENCY: Projected Rank Bracket: AIR 500 - 3,000**")
    elif weekly_hours >= 36.0 and mock_score >= 140:
        st.info("⚡ **COMPETITIVE STABILITY: Projected Rank Bracket: AIR 3,000 - 12,000**")
    elif weekly_hours >= 25.0 and mock_score >= 100:
        st.warning("⚠️ **BORDERLINE PACING: Projected Rank Bracket: AIR 12,000 - 35,000**")
    else:
        st.error("🚨 **DANGER RANGE TRACKING: High Risk Zone (Syllabus Crash Warning)**")

# ===================================================
# NEW TAB 3: DYNAMIC AI QUESTION GENERATOR Arena
# ===================================================
with tab3:
    st.subheader("🎯 IIT-JEE Infinite Question Generator")
    st.markdown("Generate real-time custom mock problems powered by Google Gemini.")

    # Secure configuration input box for your secret key
    user_api_key = st.text_input("🔑 Enter your Google Gemini API Key:", type="password", help="Get your key for free from Google AI Studio.")
    
    st.markdown("---")
    
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        sel_sub = st.selectbox("Select Subject:", ["Physics", "Chemistry", "Math"])
    with qc2:
        # Changes target chapter list automatically based on selected subject!
        sel_ch = st.selectbox("Select Target Module:", JEE_SYLLABUS[sel_sub])
    with qc3:
        sel_diff = st.selectbox("Difficulty Profile:", ["JEE Main (Conceptual/Easy)", "JEE Main (Standard/Medium)", "JEE Advanced (Intense Matrix/Hard)"])
    with qc4:
        sel_qty = st.slider("Question Quantity:", min_value=1, max_value=5, value=3)

    if st.button("🚀 Fire Up Practice Arena Tests", use_container_width=True):
        if not user_api_key:
            st.error("Please enter your Gemini API Key first to authenticate the pipeline!")
        else:
            try:
                with st.spinner("Professor Engine processing configuration parameters... Generating your workspace..."):
                    genai.configure(api_key=user_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Framing the ultimate strict engineering instructions prompt
                    prompt = f"""
                    Act as an elite IIT-JEE professor. Generate exactly {sel_qty} clear Multiple Choice Questions (MCQs) for the subject {sel_sub}, chapter "{sel_ch}", matching a difficulty profile of {sel_diff}.
                    
                    Format rules strictly:
                    For each question:
                    1. Output the Question clearly with proper standard layout notations.
                    2. Provide four clear options labeled clearly as A), B), C), D).
                    3. Right below the options, add an expandable-ready hint or solution block clearly demarcated as "Correct Answer & Step-by-Step Explanation:"
                    Make sure the explanations explain the formulas used cleanly.
                    """
                    
                    response = model.generate_content(prompt)
                    st.session_state.current_test_output = response.text
                    st.success("Test Sheet Compiled Successfully!")
            except Exception as e:
                st.error(f"API Connection Exception triggered: {e}")

    # Render generated data on screen
    if "current_test_output" in st.session_state:
        st.markdown("---")
        st.subheader("📝 Live Test Sheet Coordinates")
        st.info("Grab a rough notebook and solve these before scrolling down to view answers!")
        st.markdown(st.session_state.current_test_output)
