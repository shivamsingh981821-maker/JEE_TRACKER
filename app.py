import streamlit as st
import pandas as pd
import datetime
import os
import time

st.set_page_config(page_title="AIR 1 Velocity Tracker", page_icon="🚀", layout="wide")

st.title("🚀 AIR 1 Velocity Engine: Ultimate Command Station")
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

# MASTER SYLLABUS STRUCTURE
JEE_SYLLABUS = {
    "Physics": ["Units & Dimensions", "Vectors & Kinematics", "Laws of Motion", "Work, Energy & Power", "Rotational Motion", "Gravitation", "Properties of Matter", "Thermodynamics", "SHM & Waves"],
    "Chemistry": ["Mole Concept", "Atomic Structure", "Periodic Table", "Chemical Bonding", "States of Matter", "Thermodynamics", "Chemical Equilibrium", "Ionic Equilibrium", "Redox Reactions"],
    "Math": ["Sets", "Relations & Functions", "Trigonometry", "Quadratic Equations", "Complex Numbers", "Sequences & Series", "Straight Lines", "Circles", "Permutations & Combinations"]
}

# Load or Initialize Permanent Syllabus State
if os.path.exists(SYLLABUS_FILE):
    df_syll = pd.read_csv(SYLLABUS_FILE)
else:
    # Build default structure
    rows = []
    for sub, chapters in JEE_SYLLABUS.items():
        for ch in chapters:
            rows.append({"Subject": sub, "Chapter": ch, "Completed": False, "Status": "🔴 Backlog"})
    df_syll = pd.DataFrame(rows)

# Create Master Navigation Tabs
tab1, tab2 = st.tabs(["📊 Daily Desk Station & Logs", "🎯 Smart Syllabus Matrix & Rank Engine"])

# ===================================================
# TAB 1: TIMESTAMP ENGINE LOGS SYSTEM
# ===================================================
with tab1:
    st.subheader("⏱️ Professional Desk Session Clock")
    
    if "session_start" not in st.session_state:
        st.session_state.session_start = None
    if "manual_hours" not in st.session_state:
        st.session_state.manual_hours = 0.0

    col_btn1, col_btn2, _ = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("🏁 Start Session Clock", use_container_width=True):
            st.session_state.session_start = time.time()
            st.success("Session timestamp initiated! You can close this app or lock your screen now.")

    with col_btn2:
        if st.button("🛑 Stop & Calculate Time", use_container_width=True):
            if st.session_state.session_start is not None:
                duration_seconds = time.time() - st.session_state.session_start
                st.session_state.manual_hours = round(duration_seconds / 3600.0, 2)
                st.session_state.session_start = None
                st.success("Time computed from background timestamps successfully!")
            else:
                st.warning("No active session running. Click Start first.")

    # Status indicator line
    if st.session_state.session_start is not None:
        st.info("⚡ **Running in background:** The server is tracking your delta window context. Go study!")
    
    st.markdown("---")
    st.subheader("📝 Save Session to Master Database")
    
    col_d, col_h, col_g = st.columns(3)
    with col_d:
        log_date = st.date_input("Select Date", datetime.date.today())
    with col_h:
        study_hours = st.number_input("Study Hours Logged:", min_value=0.0, max_value=24.0, value=float(st.session_state.manual_hours), step=0.1)
    with col_g:
        custom_daily_goal = st.slider("Set Target Goal for this Date (Hrs):", min_value=1.0, max_value=14.0, value=6.0, step=0.5)

    if st.button("📥 Commit Entry to Cloud Log"):
        if not df_log.empty:
            df_log = df_log[df_log['Date'] != log_date]
        
        new_row = pd.DataFrame({'Date': [log_date], 'Hours_Studied': [study_hours], 'Daily_Goal': [custom_daily_goal]})
        df_log = pd.concat([df_log, new_row], ignore_index=True).sort_values(by='Date')
        df_log.to_csv(LOG_FILE, index=False)
        st.session_state.manual_hours = 0.0  # Clear buffer
        st.success("Log Saved!")
        st.rerun()

    st.markdown("---")
    if not df_log.empty:
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
# TAB 2: PERSISTENT SMART MATRIX & RANK ENGINE
# ===================================================
with tab2:
    st.subheader("🛡️ Permanent Chapter Checklist Matrix")
    st.markdown("Changes made here are permanently recorded into the server storage system.")

    # Render checklist columns dynamically mapped to the dataframe storage
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
                
                # Load values out of memory rows
                default_checked = bool(row["Completed"])
                default_status_idx = ["🟢 Completed (PYQs Done)", "🟡 Only Theory", "🔴 Backlog"].index(row["Status"])
                
                # Display interactive options
                new_check = st.checkbox(ch_name, value=default_checked, key=f"ch_{sub}_{ch_name}")
                new_status = st.selectbox("Status:", ["🟢 Completed (PYQs Done)", "🟡 Only Theory", "🔴 Backlog"], index=default_status_idx, key=f"st_{sub}_{ch_name}")
                
                if new_status == "🔴 Backlog":
                    total_backlogs += 1
                
                updated_rows.append({"Subject": sub, "Chapter": ch_name, "Completed": new_check, "Status": new_status})

    # Save changes instantly to file storage if any states differ
    df_new_syll = pd.DataFrame(updated_rows)
    if not df_new_syll.equals(df_syll):
        df_new_syll.to_csv(SYLLABUS_FILE, index=False)
        st.rerun()

    # Automating calculations using saved data
    p_sub = df_new_syll[df_new_syll["Subject"] == "Physics"]
    c_sub = df_new_syll[df_new_syll["Subject"] == "Chemistry"]
    m_sub = df_new_syll[df_new_syll["Subject"] == "Math"]

    def calc_pts(df):
        pts = 0
        for _, r in df.iterrows():
            if r["Completed"]:
                pts += 1.0 if r["Status"] == "🟢 Completed (PYQs Done)" else 0.6
        return (pts / len(df)) * 100

    p_cov_pct = calc_pts(p_sub)
    c_cov_pct = calc_pts(c_sub)
    m_cov_pct = calc_pts(m_sub)

    st.markdown("---")
    st.subheader("🚨 Real-Time Command Metrics")
    
    if total_backlogs > 0:
        st.error(f"⚠️ **Backlog Threat Multiplier:** You have `{total_backlogs}` active backlogs marked.")
    else:
        st.success("✅ **Clear Horizon:** Zero active backlogs flagged.")

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
        st.success("🔥 **Elite Velocity Pace:** AIR < 2,500.")
    elif mains_readiness >= 15.0:
        st.info("⚡ **NIT Selection Stability Zone:** AIR 5,000 - 15,000.")
    elif mains_readiness > 0:
        st.warning("⚠️ **Starting Acceleration Phase:** Initial modules locked down.")
    else:
        st.info("The Syllabus Matrix is clean. Check your current running batch chapters above to deploy your index!")
