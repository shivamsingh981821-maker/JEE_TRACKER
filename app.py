import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="AIR 1 Velocity Tracker", page_icon="🚀", layout="wide")

st.title("🚀 AIR 1 Velocity Engine: Master Station")
st.markdown("---")

# File path to store our study history locally
DATA_FILE = "study_log.csv"

# Load existing data or create an empty DataFrame if it doesn't exist
if os.path.exists(DATA_FILE):
    df_log = pd.read_csv(DATA_FILE)
    df_log['Date'] = pd.to_datetime(df_log['Date']).dt.date
else:
    df_log = pd.DataFrame(columns=['Date', 'Hours_Studied', 'Daily_Goal'])

# Create two clean tabs at the top of your webpage
tab1, tab2 = st.tabs(["📊 Daily Execution Log", "🎯 Rank Velocity Predictor"])

# ==========================================
# TAB 1: ADVANCED LOGGING & GRAPH SYSTEM
# ==========================================
with tab1:
    st.subheader("📝 Setup & Log Today's Execution")
    col1, col2, col3 = st.columns(3)

    with col1:
        log_date = st.date_input("Select Date", datetime.date.today())
    with col2:
        study_hours = st.number_input("Study Hours Logged:", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
    with col3:
        custom_daily_goal = st.slider("Set Target Goal for this Date (Hrs):", min_value=1.0, max_value=14.0, value=6.0, step=0.5)

    if st.button("Save Entry to Cloud Log"):
        if not df_log.empty:
            df_log = df_log[df_log['Date'] != log_date]
        
        new_row = pd.DataFrame({'Date': [log_date], 'Hours_Studied': [study_hours], 'Daily_Goal': [custom_daily_goal]})
        df_log = pd.concat([df_log, new_row], ignore_index=True)
        df_log = df_log.sort_values(by='Date')
        df_log.to_csv(DATA_FILE, index=False)
        st.success(f"Successfully logged {study_hours} hrs against a {custom_daily_goal} hr goal for {log_date}!")
        st.rerun()

    st.markdown("---")

    if not df_log.empty:
        st.subheader("📊 Performance Metrics & Analytics")
        
        total_entries = len(df_log)
        total_hours = df_log['Hours_Studied'].sum()
        avg_hours = df_log['Hours_Studied'].mean()
        expected_total_hours = df_log['Daily_Goal'].sum()
        net_deficit = total_hours - expected_total_hours
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Hours Banked", f"{total_hours:.1f} hrs")
        m2.metric("True Daily Velocity Average", f"{avg_hours:.1f} hrs/day")
        
        if net_deficit >= 0:
            m3.metric("Adaptive Goal Buffer", f"+{net_deficit:.1f} hrs ahead")
        else:
            m3.metric("Adaptive Goal Buffer", f"{net_deficit:.1f} hrs behind", delta_color="inverse")
            
        latest_entry = df_log.iloc[-1]
        latest_hours = latest_entry['Hours_Studied']
        latest_goal = latest_entry['Daily_Goal']
        latest_date = latest_entry['Date']
        
        st.markdown("### 🎯 Target Breakdown")
        if latest_hours >= latest_goal:
            st.success(f"**Status for {latest_date}:** Escape Velocity Achieved! You crossed your custom {latest_goal} hr target by +{latest_hours - latest_goal:.1f} hours.")
        else:
            st.warning(f"**Status for {latest_date}:** Target Deficit. You achieved {latest_hours} hours, which is {latest_goal - latest_hours:.1f} hours short of your self-defined target.")

        st.markdown("### 📈 Historical Execution Trend")
        chart_data = df_log.copy().set_index('Date')
        st.line_chart(chart_data[['Hours_Studied', 'Daily_Goal']])
        
        with st.expander("📂 View Raw History Sheet"):
            st.dataframe(df_log, use_container_width=True)
    else:
        st.info("The Master Log is currently blank. Enter your study hours above to initialize tracking!")

# ==========================================
# TAB 2: ORIGINAL RANK VELOCITY ENGINE
# ==========================================
with tab2:
    st.subheader("🎯 Instant Rank Estimation Calculator")
    st.markdown("Slide the bars to evaluate your current routine's competitive projection.")
    
    # Restoring your original interactive logic sliders
    daily_study = st.slider("Pure Self-Study Hours (Excluding Classes):", min_value=0.0, max_value=16.0, value=6.0, step=0.5)
    focus_efficiency = st.slider("Focus & Concentration Level (%):", min_value=10, max_value=100, value=80, step=5)
    
    # Calculate effective execution metrics
    effective_hours = daily_study * (focus_efficiency / 100.0)
    
    st.markdown("---")
    st.subheader(f"⚡ Effective Study Velocity: `{effective_hours:.1f} Hours`")
    
    # Predict rank brackets based on effective hours
    if effective_hours >= 10.0:
        st.success("🔥 **Elite AIR Bracket Prediction:** Top 100 / IIT Bombay CSE Pace. Absolute dominant velocity.")
    elif effective_hours >= 8.0:
        st.success("🚀 **Top Tier IIT Bracket Prediction:** AIR Under 1,000. Exceptional consistency.")
    elif effective_hours >= 6.0:
        st.info("⚡ **Solid NIT / Core IIT Selection Pace:** AIR 1,000 - 10,000. You are securely in the game.")
    elif effective_hours >= 4.0:
        st.warning("⚠️ **Borderline Competitive Bracket:** Safe Qualifier. Increase daily duration to break into the elite ranks.")
    else:
        st.error("🚨 **Danger Zone Velocity:** High risk of missing cutoff thresholds. Immediate acceleration required.")
