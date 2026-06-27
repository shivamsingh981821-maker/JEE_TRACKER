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
tab1, tab2 = st.tabs(["📊 Daily Execution Log", "🎯 Advanced Preparation Meter & Rank Engine"])

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
# TAB 2: ADVANCED PREPARATION & RANK METER
# ==========================================
with tab2:
    st.subheader("🛡️ Strategic Preparation Profile")
    st.markdown("Input your exact syllabus parameters to compute your current location on the national competitive vector.")
    
    # 3-Column Subject Inputs
    p_col, c_col, m_col = st.columns(3)
    
    with p_col:
        st.markdown("#### ⚛️ Physics Profile")
        p_cov = st.slider("Physics Syllabus Covered (%):", 0, 100, 15, key="p_cov")
        p_lvl = st.radio("Depth Level reached:", ["Mains Only (Formula/Basic PYQs)", "Advanced Level (Deep Theory/Irodov/Tough PYQs)"], key="p_lvl")
        
    with c_col:
        st.markdown("#### 🧪 Chemistry Profile")
        c_cov = st.slider("Chemistry Syllabus Covered (%):", 0, 100, 15, key="c_cov")
        c_lvl = st.radio("Depth Level reached:", ["Mains Only (Formula/Basic PYQs)", "Advanced Level (Deep Theory/Irodov/Tough PYQs)"], key="c_lvl")
        
    with m_col:
        st.markdown("#### 📐 Mathematics Profile")
        m_cov = st.slider("Math Syllabus Covered (%):", 0, 100, 15, key="m_cov")
        m_lvl = st.radio("Depth Level reached:", ["Mains Only (Formula/Basic PYQs)", "Advanced Level (Deep Theory/Irodov/Tough PYQs)"], key="m_lvl")
        
    # Consistency Modifier from historical logging data
    st.markdown("---")
    st.markdown("#### ⚡ Execution Consistency Modifiers")
    daily_pace = st.slider("Current Consistent Daily Self-Study Hours:", 1.0, 16.0, 6.0)
    test_accuracy = st.slider("Average Test/Mock Problem Accuracy Level (%):", 10, 100, 75)

    # ---------------- CALCULATIONS ENGINE ----------------
    # Weight factors based on choice of depth level
    p_weight = 1.0 if p_lvl == "Advanced Level (Deep Theory/Irodov/Tough PYQs)" else 0.65
    c_weight = 1.0 if c_lvl == "Advanced Level (Deep Theory/Irodov/Tough PYQs)" else 0.65
    m_weight = 1.0 if m_lvl == "Advanced Level (Deep Theory/Irodov/Tough PYQs)" else 0.65
    
    # Compute base score out of 300 maximum normalized units
    net_p_score = p_cov * p_weight
    net_c_score = c_cov * c_weight
    net_m_score = m_cov * m_weight
    
    raw_preparation_score = (net_p_score + net_c_score + net_m_score) / 3.0
    
    # Apply operational multipliers based on study hours and problem accuracy
    hours_multiplier = min(1.2, daily_pace / 7.0)
    accuracy_multiplier = test_accuracy / 100.0
    
    final_readiness_index = raw_preparation_score * hours_multiplier * accuracy_multiplier
    
    # Prevent edge boundary math errors
    final_readiness_index = max(1.0, min(100.0, final_readiness_index))

    st.markdown("---")
    st.subheader("📊 Live Strategic Positioning Metrics")
    
    # Progress Trackers for Mains vs Advanced
    mains_readiness = min(100.0, (p_cov + c_cov + m_cov) / 3.0 * (test_accuracy / 100.0) * (daily_pace / 5.0 if daily_pace < 5 else 1.1))
    adv_readiness = final_readiness_index

    prog_col1, prog_col2 = st.columns(2)
    with prog_col1:
        st.markdown(f"**JEE Mains Preparation Meter:** `{mains_readiness:.1f}%` Complete")
        st.progress(mains_readiness / 100.0)
    with prog_col2:
        st.markdown(f"**JEE Advanced Preparation Meter:** `{adv_readiness:.1f}%` Complete")
        st.progress(adv_readiness / 100.0)

    # Dynamic Rank Projection Brackets based on math vector mapping
    st.markdown("### 🎯 National Rank Coordinate Prediction")
    
    if adv_readiness >= 75.0:
        st.success("🔥 **CRITICAL VELOCITY reached: AIR < 500 Predicted (JEE Advanced Tier)**\nYou are exhibiting conceptual mastery coupled with exceptional execution metrics. Eligible for IIT Bombay / IIT Delhi core branches.")
    elif adv_readiness >= 55.0:
        st.success("🚀 **HIGH VELOCITY reached: AIR 500 - 2,500 Predicted**\nStrong core structure. If you push your lowest subject profile further into the Advanced zone, you can breach the triple-digit absolute national rank barrier.")
    elif mains_readiness >= 60.0 and adv_readiness >= 35.0:
        st.info("⚡ **COMPETITIVE STABILITY: AIR 2,500 - 12,000 (Top NIT / Core IIT Zone)**\nYou have built a reliable framework for JEE Mains and clear the basic Advanced thresholds. Transitioning remaining chapters to advanced question banks will scale your rank.")
    elif mains_readiness >= 40.0:
        st.warning("⚠️ **QUALIFIER SPACE: AIR 12,000 - 35,000 (NIT / State Elite)**\nYour tracking reveals structural holes or depth limitations. Your formula base is forming, but daily execution pace must scale up immediately to build conceptual stamina.")
    else:
        st.error("🚨 **FOUNDATIONAL RECONSTRUCTION ZONE**\nCurrent readiness indices are sub-optimal for high competitive tiers. Focus strictly on maximizing problem-solving consistency and mastering your fundamental theory modules.")
        
