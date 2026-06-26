import streamlit as st

st.title("🚀 The AIR 1 Velocity Engine")
st.subheader("Turn Potential into Execution")
st.markdown("---")

confidence = st.slider("Your Self-Belief/Confidence (%)", 50, 100, 100)
self_study_hours = st.slider("Daily PURE Self-Study Hours (No Lectures)", 0.0, 14.0, 3.3, 0.5)
consistency_days = st.slider("Days Per Week You Maintain This", 1.0, 7.0, 6.5, 0.5)

effective_units = self_study_hours * consistency_days * (confidence / 100.0)

st.markdown("---")
st.metric(label="Your Effective Weekly Practice Units", value=f"{effective_units:.2f} Units")

if effective_units < 15:
    st.error("🔴 CURRENT TIER: Unfulfilled Potential / No Rank")
elif 15 <= effective_units < 36:
    st.warning("🟡 CURRENT TIER: Qualified / Middle-Tier NITs")
elif 36 <= effective_units < 60:
    st.success("🟢 CURRENT TIER: Top 5000 / Top NITs & Choice IITs")
else:
    st.info("⚡ CURRENT TIER: Top 500 / Choice IIT Branches (IIT Bombay CSE Zone)")

st.caption("Press Ctrl+S in VS Code anytime you change the code to update your app!")