import streamlit as st

st.set_page_config(
    page_title="Soccer Performance Science",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .hero {
            position: relative;
            width: 100%;
            height: 340px;
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 2rem;
        }
        .hero img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center 40%;
            filter: brightness(0.45);
        }
        .hero-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            width: 90%;
        }
        .hero-title {
            font-size: 4rem;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: -1px;
            margin: 0;
            line-height: 1.1;
        }
        .hero-title span {
            color: #1D9E75;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #D0CEC9;
            margin-top: 0.8rem;
            font-weight: 400;
        }
        .card {
            background-color: #1A1D24;
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid #1D9E75;
            height: 100%;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #1D9E75;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .card-text {
            font-size: 0.9rem;
            color: #9B9A96;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            color: #9B9A96;
            font-size: 0.85rem;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style="
        padding: 1rem 0.5rem 0.8rem 0.5rem;
        border-bottom: 1px solid #2A2D34;
        margin-bottom: 1rem;
    ">
        <p style="
            font-size: 1.1rem;
            font-weight: 800;
            color: #FAFAFA;
            margin: 0;
            letter-spacing: -0.5px;
        ">Performance<span style="color:#1D9E75;"> Science</span></p>
        <p style="
            font-size: 0.75rem;
            color: #9B9A96;
            margin: 2px 0 0 0;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        ">SoccerMon · 2020–2021</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero">
        <img src="https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1400&q=80" />
        <div class="hero-text">
            <p class="hero-title">Soccer <span>Performance</span> Science</p>
            <p class="hero-subtitle">Player performance intelligence platform — training load, readiness, and injury risk modeling for elite athletes</p>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">Squad Overview</div>
        <div class="card-text">Daily readiness status for the full squad. Green / amber / red traffic light system based on wellness score and ACWR. Filter by team and date.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">Player Drill-Down</div>
        <div class="card-text">Individual player load and wellness trends. 30-day ACWR chart with risk zones, wellness radar across 6 dimensions, and daily load history.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">Team Load</div>
        <div class="card-text">Weekly periodization view and daily load heatmap across the full squad. Track acute:chronic ratios and identify load spikes before they become injuries.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
    <div class="footer">
        Built on SoccerMon open data &nbsp;·&nbsp; Python &nbsp;·&nbsp; dbt &nbsp;·&nbsp; DuckDB &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Pandera &nbsp;·&nbsp; GitHub Actions
    </div>
""", unsafe_allow_html=True)