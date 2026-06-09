import streamlit as st

st.set_page_config(
    page_title="Soccer Performance Science",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚽ Soccer Performance Science")
st.markdown(
    """
    A player performance intelligence platform built on SoccerMon athlete monitoring data.
    Use the sidebar to navigate between pages.
    """
)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Squad Overview**\nDaily readiness status for the full squad.")
with col2:
    st.info("**Player Drill-Down**\nIndividual player load and wellness trends.")
with col3:
    st.info("**Team Load**\nWeekly periodization and load heatmap.")