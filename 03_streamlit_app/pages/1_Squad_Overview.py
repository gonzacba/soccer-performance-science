import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_readiness, STATUS_EMOJI, STATUS_COLORS

st.set_page_config(page_title="Squad Overview", layout="wide", page_icon=None)

st.markdown("""
    <style>
        .metric-card {
            background-color: #1A1D24;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
        }
        .metric-value { font-size: 2.2rem; font-weight: 700; margin: 0; }
        .metric-label { font-size: 0.85rem; color: #9B9A96; margin: 0; }
        .ready-val { color: #1D9E75; }
        .monitor-val { color: #EF9F27; }
        .load-val { color: #D85A30; }
        .total-val { color: #FAFAFA; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="font-size:3rem; font-weight:800; color:#FAFAFA; border-bottom:3px solid #1D9E75; padding-bottom:0.4rem; margin-bottom:1rem;">Squad Overview</h1>', unsafe_allow_html=True)

df = load_readiness()

with st.sidebar:
    st.markdown("### Filters")
    teams = ["All"] + sorted(df["team"].unique().tolist())
    selected_team = st.selectbox("Team", teams)
    dates = sorted(df["date"].dt.date.unique(), reverse=True)
    selected_date = st.selectbox("Date", dates)

filtered = df[df["date"].dt.date == selected_date]
if selected_team != "All":
    filtered = filtered[filtered["team"] == selected_team]

ready = (filtered["readiness_status"] == "Ready").sum()
monitor = (filtered["readiness_status"] == "Monitor").sum()
load_managed = (filtered["readiness_status"] == "Load-Managed").sum()
total = len(filtered)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><p class="metric-value total-val">{total}</p><p class="metric-label">Total Players</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p class="metric-value ready-val">{ready}</p><p class="metric-label">Ready</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p class="metric-value monitor-val">{monitor}</p><p class="metric-label">Monitor</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><p class="metric-value load-val">{load_managed}</p><p class="metric-label">Load-Managed</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("#### Player Readiness")
    display = filtered[[
        "player_id", "team", "readiness_status",
        "wellness_score", "acwr", "daily_load"
    ]].copy()
    display["player_id"] = display["team"] + "-P" + display.groupby("team").cumcount().add(1).astype(str).str.zfill(2)
    display["Status"] = display["readiness_status"].map(lambda s: f"{STATUS_EMOJI.get(s, '')} {s}")
    display = display.rename(columns={
        "player_id": "Player",
        "team": "Team",
        "wellness_score": "Wellness",
        "acwr": "ACWR",
        "daily_load": "Load",
    })
    display = display.drop(columns=["readiness_status"])
    display = display[["Player", "Team", "Status", "Wellness", "ACWR", "Load"]]
    display = display.sort_values("Status")
    st.dataframe(display, use_container_width=True, hide_index=True, height=420)

with col_right:
    st.markdown("#### Distribution")
    status_counts = filtered["readiness_status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig = go.Figure(go.Pie(
        labels=status_counts["Status"],
        values=status_counts["Count"],
        hole=0.55,
        marker=dict(colors=[STATUS_COLORS.get(s, "#888") for s in status_counts["Status"]]),
        textinfo="label+percent",
        textfont=dict(size=12),
    ))
    fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("#### Team Readiness Trend — Last 14 Days")

last_14 = df[df["date"].dt.date <= selected_date].copy()
last_14 = last_14.sort_values("date").tail(14 * len(df["player_id"].unique()))
if selected_team != "All":
    last_14 = last_14[last_14["team"] == selected_team]

daily_status = last_14.groupby(["date", "readiness_status"]).size().reset_index(name="count")

fig2 = px.bar(
    daily_status,
    x="date",
    y="count",
    color="readiness_status",
    color_discrete_map=STATUS_COLORS,
    barmode="stack",
    title="Daily Squad Readiness Status",
)
fig2.update_layout(
    height=300,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend_title="Status",
    xaxis_title="",
    yaxis_title="Players",
)
st.plotly_chart(fig2, use_container_width=True)