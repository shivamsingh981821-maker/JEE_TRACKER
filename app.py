import streamlit as st
import pandas as pd
import datetime
import os
import time
import google.generativeai as genai

st.set_page_config(page_title="AIR Infinite Velocity Engine", page_icon="🎯", layout="wide")

st.title("🦅 AIR Infinite Velocity Engine: Master Command Station")
st.markdown("---")

LOG_FILE = "study_log.csv"
SYLLABUS_FILE = "syllabus_state.csv"

if os.path.exists(LOG_FILE):
    df_log = pd.read_csv(LOG_FILE)
    df_log['Date'] = pd.to_datetime(df_log['Date']).dt.date
else:
    df_log = pd.DataFrame(columns=['Date', 'Hours_Studied', 'Daily_Goal'])

JEE_SYLLABUS = {
    "Physics": [
        "Units & Dimensions", "Vectors & Kinematics", "Laws of Motion", "Work, Energy & Power", 
        "Rotational Motion", "Gravitation", "Mechanical Properties of Solids", "Mechanical Properties of Fluids", 
        "Thermal Properties of Matter", "Thermodynamics", "Kinetic Theory of Gases", "SHM & Waves",
        "Electrostatics & Gauss Law", "Capacitance", "Current Electricity", "Moving Charges & Magnetism", 
        "Magnetism & Matter", "Electromagnetic Induction (EMI)", "Alternating Current (AC)", "Electromagnetic Waves",
        "Ray Optics & Optical Instruments", "Wave Optics", "Dual Nature of Radiation & Matter", "Atoms", "Nuclei", 
        "Electronic Devices (Semiconductors)"
    ],
    "Chemistry": [
        "Some Basic Concepts of Chemistry (Mole Concept)", "Structure of Atom", "Classification of Elements & Periodicity", 
        "Chemical Bonding & Molecular Structure", "Chemical Thermodynamics", "Chemical Equilibrium", "Ionic Equilibrium", 
        "Redox Reactions", "Organic Chemistry: Basic Principles & Techniques (GOC)", "Hydrocarbons",
        "Solutions", "Electrochemistry", "Chemical Kinetics", "The d & f-Block Elements", "Coordination Compounds", 
        "Haloalkanes & Haloarenes", "Alcohols, Phenols & Ethers", "Aldehydes, Ketones & Carboxylic Acids", 
        "Amines", "Biomolecules"
    ],
    "Math": [
        "Sets", "Relations & Functions", "Trigonometric Functions", "Principle of Mathematical Induction", 
        "Complex Numbers & Quadratic Equations", "Linear Inequalities", "Permutations & Combinations", 
        "Binomial Theorem", "Sequences & Series", "Straight Lines", "Conic Sections (Circles, Parabola, Ellipse, Hyperbola)", 
        "Introduction to 3D Geometry", "Limits & Derivatives", "Statistics", "Probability",
        "Matrices", "Determinants", "Continuity & Differentiability", "Applications of Derivatives", 
        "Integrals (Calculus)", "Applications of Integrals", "Differential Equations", "Vector Algebra", 
        "Three Dimensional Geometry"
    ]
}

if os.path.exists(SYLLABUS_FILE):
    df_syll = pd.read_csv(SYLLABUS_FILE)
else:
    rows = []
    for sub, chapters in JEE_SYLLABUS.items():
        for ch in chapters:
            rows.append({"Subject": sub, "Chapter": ch, "Completed": False, "Status": "🔴 Backlog"})
    df_syll = pd.DataFrame(rows)

tab1, tab2, tab3 = st.tabs(["📊 Daily Desk Station & Logs", "🎯 Smart Syllabus Matrix & Rank Engine", "📝 AI Infinite Practice Arena"])

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

with tab2:
    st.subheader("🛡️ Permanent Chapter Checklist Matrix")
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    subjects = ["Physics", "Chemistry", "Math"]
    cols_mapped = [sub_col1, sub_col2, sub_col3]
    updated_rows = []

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
                updated_rows.append({"Subject": sub, "Chapter": ch_name, "Completed": new_check, "Status": new_status})

    df_new_syll = pd.DataFrame(updated_rows)
    df_new_syll.to_csv(SYLLABUS_FILE, index=False)

    st.markdown("---")
    st.subheader("⚡ Study Consistency & Effort Rank Predictor")
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    with calc_col1:
        days_per_week = st.slider("Effective Study Days Per Week:", min_value=1, max_value=7, value=6)
    with calc_col2:
        hours_per_day = st.slider("Average Self-Study Hours Per Day:", min_value=1.0, max_value=16.0, value=6.0, step=0.5)
    with calc_col3:
        mock_score = st.slider("Target/Current Mock Test Score (Out of 300):", min_value=0, max_value=300, value=104, step=5)

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

with tab3:
    st.subheader("🎯 Elite Examination Testing Arena")
    st.markdown("Generate comprehensive custom problem sets mapping strictly to national examination parameters.")

    user_api_key = st.text_input("🔑 Enter your Google Gemini API Key:", type="password")
    st.markdown("---")
    
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        sel_sub = st.selectbox("Choose Target Subject:", ["Physics", "Chemistry", "Math"])
    with qc2:
        sel_ch = st.selectbox("Choose Target Chapter Module:", JEE_SYLLABUS[sel_sub])
    with qc3:
        sel_exam_mode = st.selectbox("Select Target Examination Pattern:", [
            "CBSE Class 11 Board Mode (Subjective & Derivations)", 
            "JEE Mains Mode (Single-Correct MCQs + Numerical)", 
            "JEE Advanced Mode (Intense Multiple-Correct / Matrix Match)"
        ])
    with qc4:
        sel_qty = st.number_input("Custom Question Quantity:", min_value=1, max_value=50, value=5, step=1)

    time_per_question = 2 if "Mains" in sel_exam_mode else (4 if "Advanced" in sel_exam_mode else 3)
    total_allocated_minutes = sel_qty * time_per_question

    st.info(f"⏳ **Exam Strategy Target:** Total exam duration allocated for this set: **{total_allocated_minutes} Minutes**.")

    if st.button("🚀 Execute Problem Set Compilation Engine", use_container_width=True):
        if not user_api_key:
            st.error("Authentication Missing: Please paste your secret developer key into the secure input box.")
        else:
            try:
                with st.spinner("AI Professor compiling custom exam workspace sheets..."):
                    genai.configure(api_key=user_api_key) 
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    Act as an expert Indian National Examination coordinator for IIT-JEE and NCERT CBSE Boards.
                    Generate exactly {sel_qty} pristine questions for {sel_sub}, focusing entirely on the module "{sel_ch}".
                    
                    Strict Pattern Architecture Rules:
                    Target Format Blueprint: {sel_exam_mode}.
                    - If Class 11 Board Mode: Focus on formal theoretical definitions, standard NCERT derivations, and clean step-by-step subjective numerical problems. 
                    - If JEE Mains Mode: Focus on high-yield single-correct MCQs and standard numerical fill-ins matching recent trends.
                    - If JEE Advanced Mode: Generate high-conceptual depth problems including multiple-correct options, matrix matching, or challenging multi-tier numerical answers.
                    
                    Ensure all questions use standard symbols and notations. Hide the solution block directly underneath each problem in a clean expandable structure designated as:
                    "Correct Answer & Step-by-Step Explanation:"
                    """
                    
                    response = model.generate_content(prompt)
                    st.session_state.unlocked_arena_output = response.text
                    st.session_state.exam_start_time = time.time()
                    st.session_state.exam_duration_seconds = total_allocated_minutes * 60
                    st.success("Custom Exam Paper Generated successfully!")
            except Exception as e:
                st.error(f"Execution Error: Code failed to reach servers. Reason: {e}")

    if "exam_start_time" in st.session_state and "unlocked_arena_output" in st.session_state:
        elapsed_time = time.time() - st.session_state.exam_start_time
        remaining_time = st.session_state.exam_duration_seconds - elapsed_time
        
        if remaining_time > 0:
            mins, secs = divmod(int(remaining_time), 60)
            st.warning(f"⏰ **LIVE EXAM COUNTDOWN TIMER:** `{mins:02d}:{secs:02d}` Remaining!")
        else:
            st.error("🚨 **TIME OVER:** Allocated practice time has expired!")

    if "unlocked_arena_output" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.unlocked_arena_output)
