import streamlit as st

st.set_page_config(
    page_title="Soccer Performance Science",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1D9E75;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #9B9A96;
            margin-bottom: 2rem;
        }
        .card {
            background-color: #1A1D24;
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid #1D9E75;
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1D9E75;
            margin-bottom: 0.4rem;
        }
        .card-text {
            font-size: 0.9rem;
            color: #9B9A96;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">⚽ Soccer Performance Science</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Player performance intelligence platform built on SoccerMon athlete monitoring data.</p>', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">🏟️ Squad Overview</div>
        <div class="card-text">Daily readiness status for the full squad. Green / amber / red traffic light system based on wellness score and ACWR.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">👤 Player Drill-Down</div>
        <div class="card-text">Individual player load and wellness trends. 30-day ACWR chart with risk zones, wellness radar, and daily load history.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Team Load</div>
        <div class="card-text">Weekly periodization view and daily load heatmap across the full squad. Filter by team and date range.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
    <div style='text-align: center; color: #9B9A96; font-size: 0.85rem; margin-top: 1rem;'>
        Built on SoccerMon open data · Python · dbt · DuckDB · Streamlit · Pandera · GitHub Actions
    </div>
""", unsafe_allow_html=True)