import streamlit as st
import pandas as pd
import datetime
import os
import time

st.set_page_config(page_title="AIR 1 Velocity Tracker", page_icon="🚀", layout="wide")

st.title("🚀 AIR 1 Velocity Engine: Ultimate Command Station")
st.markdown("---")

# ----------------- DATA ARCHITECTURE SCRIPT -----------------
DATA_FILE = "study_log.csv"
if os.path.exists(DATA_FILE):
    df_log = pd.read_csv(DATA_FILE)
    df_log['Date'] = pd.to_datetime(df_log['Date']).dt.date
else:
    df_log = pd.DataFrame(columns=['Date', 'Hours_Studied', 'Daily_Goal'])

# MASTER SYLLABUS DATA STRUCT
JEE_SYLLABUS = {
    "Physics": ["Units & Dimensions", "Vectors & Kinematics", "Laws of Motion", "Work, Energy & Power", "Rotational Motion", "Gravitation", "Properties of Matter", "Thermodynamics", "SHM & Waves"],
    "Chemistry": ["Mole Concept", "Atomic Structure", "Periodic Table", "Chemical Bonding", "States of Matter", "Thermodynamics", "Chemical Equilibrium", "Ionic Equilibrium", "Redox Reactions"],
    "Math": ["Sets", "Relations & Functions", "Trigonometry", "Quadratic Equations", "Complex Numbers", "Sequences & Series", "Straight Lines", "Circles", "Permutations & Combinations"]
}

# Create Tabs
tab1, tab2 = st.tabs(["📊 Daily Desk Station & Logs", "🎯 Smart Syllabus Matrix & Rank Engine"])

# ==========================================
# TAB 1: LOGS & LIVE STOPWATCH SYSTEM
# ==========================================
with tab1:
    st.subheader("⏱️ Live Desk Session Stopwatch")
    
    # Initialize session state variables for stopwatch
    if "running" not in st.session_state:
        st.session_state.running = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0.0
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0.0

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🏁 Start Session", use_container_width=True):
            if not st.session_state.running:
                st.session_state.start_time = time.time() - st.session_state.elapsed_time
                st.session_state.running = True
    with c2:
        if st.button("🛑 Pause/Stop Session", use_container_width=True):
            if st.session_state.running:
                st.session_state.elapsed_time = time.time() - st.session_state.start_time
                st.session_state.running = False
    with c3:
        if st.button("♻️ Reset Timer", use_container_width=True):
            st.session_state.running = False
            st.session_state.start_time = 0.0
            st.session_state.elapsed_time = 0.0

    # Live time computation display
    if st.session_state.running:
        current_elapsed = time.time() - st.session_state.start_time
    else:
        current_elapsed = st.session_state.elapsed_time
        
    hours_calculated = current_elapsed / 3600.0
    
    st.info(f"### Current Desk Time Tracked: `{hours_calculated:.2f} Hours` ({int(current_elapsed//60)} minutes)")

    st.markdown("---")
    st.subheader("📝 Save Session to Master Database")
    
    col_d, col_h, col_g = st.columns(3)
    with col_d:
        log_date = st.date_input("Select Date", datetime.date.today())
    with col_h:
        # Defaults automatically to whatever your stopwatch timed!
        study_hours = st.number_input("Study Hours:", min_value=0.0, max_value=24.0, value=round(hours_calculated, 2), step=0.1)
    with col_g:
        custom_daily_goal = st.slider("Set Target Goal for this Date (Hrs):", min_value=1.0, max_value=14.0, value=6.0, step=0.5)

    if st.button("📥 Commit Entry to Cloud Log"):
        if not df_log.empty:
            df_log = df_log[df_log['Date'] != log_date]
        
        new_row = pd.DataFrame({'Date': [log_date], 'Hours_Studied': [study_hours], 'Daily_Goal': [custom_daily_goal]})
        df_log = pd.concat([df_log, new_row], ignore_index=True).sort_values(by='Date')
        df_log.to_csv(DATA_FILE, index=False)
        st.success(f"Log Updated: Saved {study_hours} hrs against a {custom_daily_goal} hr goal!")
        st.rerun()

    st.markdown("---")
    
    if not df_log.empty:
        st.subheader("📊 Analytics Trend")
        total_hours = df_log['Hours_Studied'].sum()
        avg_hours = df_log['Hours_Studied'].mean()
        net_deficit = total_hours - df_log['Daily_Goal'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Hours Banked", f"{total_hours:.1f} hrs")
        m2.metric("True Daily Velocity Average", f"{avg_hours:.1f} hrs/day")
        m3.metric("Adaptive Goal Buffer", f"{'+' if net_deficit >= 0 else ''}{net_deficit:.1f} hrs", delta_color="normal" if net_deficit >= 0 else "inverse")
        
        chart_data = df_log.copy().set_index('Date')
        st.line_chart(chart_data[['Hours_Studied', 'Daily_Goal']])

# ==========================================
# TAB 2: SMART MATRIX & adaptive RANK ENGINE
# ==========================================
with tab2:
    st.subheader("🛡️ Dynamic Chapter Checklist & Trackers")
    st.markdown("Check off your chapters and select their health status. The system calculates completion percentages automatically.")
    
    p_percentages = []
    c_percentages = []
    m_percentages = []
    
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    # Trackers counters for Backlogs
    total_backlogs = 0
    
    with sub_col1:
        st.markdown("### ⚛️ Physics Core Matrix")
        for ch in JEE_SYLLABUS["Physics"]:
            cb = st.checkbox(ch, key=f"check_p_{ch}")
            status = st.selectbox("Status", ["🟢 Completed (PYQs Done)", "🟡 Only Theory", "🔴 Backlog"], key=f"status_p_{ch}")
            if cb:
                p_percentages.append(1.0 if status == "🟢 Completed (PYQs Done)" else 0.6)
            if status == "🔴 Backlog":
                total_backlogs += 1
                
    with sub_col2:
        st.markdown("### 🧪 Chemistry Core Matrix")
        for ch in JEE_SYLLABUS["Chemistry"]:
            cb = st.checkbox(ch, key=f"check_c_{ch}")
            status = st.selectbox("Status", ["🟢 Completed (PYQs Done)", "🟡 Only Theory", "🔴 Backlog"], key=f"status_c_{ch}")
            if cb:
                c_percentages.append(1.0 if status == "🟢 Completed (PYQs Done)" else 0.6)
            if status == "🔴 Backlog":
                total_backlogs += 1
                
    with sub_col3:
        st.markdown("### 📐 Math Core Matrix")
        for ch in JEE_SYLLABUS["Math"]:
            cb = st.checkbox(ch, key=f"check_m_{ch}")
            status = st.selectbox("Status", ["🟢 Completed (PYQs Done)", "🟡 Only Theory", "🔴 Backlog"], key=f"status_m_{ch}")
            if cb:
                m_percentages.append(1.0 if status == "🟢 Completed (PYQs Done)" else 0.6)
            if status == "🔴 Backlog":
                total_backlogs += 1

    # Automating calculations instead of manuals sliders
    p_cov_pct = (sum(p_percentages) / len(JEE_SYLLABUS["Physics"])) * 100
    c_cov_pct = (sum(c_percentages) / len(JEE_SYLLABUS["Chemistry"])) * 100
    m_cov_pct = (sum(m_percentages) / len(JEE_SYLLABUS["Math"])) * 100

    st.markdown("---")
    st.subheader("🚨 Real-Time Command Metrics")
    
    if total_backlogs > 0:
        st.error(f"⚠️ **Backlog Threat Multiplier Alert:** You have `{total_backlogs}` active backlogs marked. Clear these dependencies before jumping to massive next modules!")
    else:
        st.success("✅ **Clear Horizon:** Zero active backlogs flagged. Velocity stability nominal.")

    # Calculations Engine Integration for Rank Projection
    mains_readiness = (p_cov_pct + c_cov_pct + m_cov_pct) / 3.0
    adv_readiness = mains_readiness * (1.1 if total_backlogs == 0 else 0.85)
    adv_readiness = max(1.0, min(100.0, adv_readiness))

    prog_col1, prog_col2 = st.columns(2)
    with prog_col1:
        st.markdown(f"**Calculated JEE Mains Progress:** `{mains_readiness:.1f}%` Complete")
        st.progress(mains_readiness / 100.0)
    with prog_col2:
        st.markdown(f"**Calculated JEE Advanced Progress:** `{adv_readiness:.1f}%` Complete")
        st.progress(adv_readiness / 100.0)

    st.markdown("### 🎯 Algorithmic National Rank Prediction Coordinates")
    if adv_readiness >= 40.0:
        st.success("🔥 **Elite Velocity Pace:** AIR < 2,500. Consistent chapter clearing and depth levels verified.")
    elif mains_readiness >= 15.0:
        st.info("⚡ **NIT Selection Stability Zone:** AIR 5,000 - 15,000. Foundations are scaling up beautifully. Keep moving chapters to 'Completed'.")
    elif mains_readiness > 0:
        st.warning("⚠️ **Starting Acceleration Phase:** Initial modules locked down. Keep accumulating completed targets to move up ranks.")
    else:
        st.info("The Syllabus Matrix is clean. Check your current running batch chapters above to deploy your baseline positioning index!")
