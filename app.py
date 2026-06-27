import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="AIR 1 Velocity Tracker", page_icon="🚀", layout="wide")

st.title("🚀 AIR 1 Velocity Engine: Advanced Log")
st.markdown("---")

# File path to store our study history locally
DATA_FILE = "study_log.csv"

# Load existing data or create an empty DataFrame if it doesn't exist
if os.path.exists(DATA_FILE):
    df_log = pd.read_csv(DATA_FILE)
    df_log['Date'] = pd.to_datetime(df_log['Date']).dt.date
else:
    df_log = pd.DataFrame(columns=['Date', 'Hours_Studied', 'Daily_Goal'])

# ----------------- SECTION 1: LOGGING INPUTS -----------------
st.subheader("📝 Setup & Log Today's Execution")
col1, col2, col3 = st.columns(3)

with col1:
    log_date = st.date_input("Select Date", datetime.date.today())
with col2:
    study_hours = st.number_input("Study Hours Logged:", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
with col3:
    # Dynamically define your targeted goal specifically for this date entry
    custom_daily_goal = st.slider("Set Target Goal for this Date (Hrs):", min_value=1.0, max_value=14.0, value=6.0, step=0.5)

if st.button("Save Entry to Cloud Log"):
    # Remove existing entry for the same date if it exists to avoid duplication
    if not df_log.empty:
        df_log = df_log[df_log['Date'] != log_date]
    
    # Append the new record with its specific custom goal
    new_row = pd.DataFrame({'Date': [log_date], 'Hours_Studied': [study_hours], 'Daily_Goal': [custom_daily_goal]})
    df_log = pd.concat([df_log, new_row], ignore_index=True)
    
    # Sort by date and save to CSV file
    df_log = df_log.sort_values(by='Date')
    df_log.to_csv(DATA_FILE, index=False)
    st.success(f"Successfully logged {study_hours} hrs against a {custom_daily_goal} hr goal for {log_date}!")
    st.rerun()

st.markdown("---")

# ----------------- SECTION 2: STATS & GRAPHS -----------------
if not df_log.empty:
    st.subheader("📊 Advanced Performance Metrics")
    
    # Calculate adaptive stats based on custom historical targets
    total_entries = len(df_log)
    total_hours = df_log['Hours_Studied'].sum()
    avg_hours = df_log['Hours_Studied'].mean()
    
    # Dynamic target calculations based on the sum of historical variable goals
    expected_total_hours = df_log['Daily_Goal'].sum()
    net_deficit = total_hours - expected_total_hours
    
    # Display Key Metric Cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Hours Banked", f"{total_hours:.1f} hrs")
    m2.metric("True Daily Velocity Average", f"{avg_hours:.1f} hrs/day")
    
    if net_deficit >= 0:
        m3.metric("Adaptive Goal Buffer", f"+{net_deficit:.1f} hrs ahead", delta_color="normal")
    else:
        m3.metric("Adaptive Goal Buffer", f"{net_deficit:.1f} hrs behind", delta_color="inverse")
        
    # Check target status for the latest entry dynamically
    latest_entry = df_log.iloc[-1]
    latest_hours = latest_entry['Hours_Studied']
    latest_goal = latest_entry['Daily_Goal']
    latest_date = latest_entry['Date']
    
    st.markdown("### 🎯 Target Breakdown")
    if latest_hours >= latest_goal:
        st.success(f"**Status for {latest_date}:** Escape Velocity Achieved! You crossed your custom {latest_goal} hr target by +{latest_hours - latest_goal:.1f} hours.")
    else:
        st.warning(f"**Status for {latest_date}:** Target Deficit. You achieved {latest_hours} hours, which is {latest_goal - latest_hours:.1f} hours short of your self-defined structural goal for this specific day.")

    # Render Visual Analytics
    st.markdown("### 📈 Historical Execution Trend")
    
    # Format data for chart
    chart_data = df_log.copy()
    chart_data = chart_data.set_index('Date')
    
    # The line chart will now show an adaptive target line reflecting the changes day-by-day
    st.line_chart(chart_data[['Hours_Studied', 'Daily_Goal']])
    
    # Show clean data backup table option
    with st.expander("📂 View Raw History Sheet"):
        st.dataframe(df_log, use_container_width=True)
else:
    st.info("The Master Log is currently blank. Enter your study hours above and click save to initialize the engine tracking!")
