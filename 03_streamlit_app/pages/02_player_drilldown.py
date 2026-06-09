import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_readiness, load_injury_risk, STATUS_COLORS, RISK_COLORS

st.set_page_config(page_title="Player Drill-Down", layout="wide")
st.title("👤 Player Drill-Down")

df = load_readiness()
risk_df = load_injury_risk()

with st.sidebar:
    st.header("Filters")
    teams = sorted(df["team"].unique().tolist())
    selected_team = st.selectbox("Team", teams)
    team_players = sorted(df[df["team"] == selected_team]["player_id"].unique().tolist())
    selected_player = st.selectbox("Player", team_players)
    dates = sorted(df["date"].dt.date.unique(), reverse=True)
    selected_date = st.selectbox("Date", dates)

player_df = df[df["player_id"] == selected_player].sort_values("date")
today = player_df[player_df["date"].dt.date == selected_date]

if today.empty:
    st.warning("No data for this player on the selected date.")
    st.stop()

row = today.iloc[0]

st.subheader(f"Player: {selected_player[:8]}... | {selected_team} | {selected_date}")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Wellness Score", round(row["wellness_score"], 2) if pd.notna(row["wellness_score"]) else "N/A")
col2.metric("ACWR", round(row["acwr"], 3) if pd.notna(row["acwr"]) else "N/A")
col3.metric("Daily Load", int(row["daily_load"]) if pd.notna(row["daily_load"]) else "N/A")
col4.metric("Readiness Status", row["readiness_status"])

st.markdown("---")

# 7-day ACWR trend
st.subheader("ACWR Trend — Last 30 Days")
last_30 = player_df[player_df["date"].dt.date <= selected_date].tail(30)

fig_acwr = px.line(
    last_30,
    x="date",
    y="acwr",
    title="Acute:Chronic Workload Ratio",
    markers=True,
)
fig_acwr.add_hrect(y0=0.8, y1=1.3, fillcolor="green", opacity=0.1, annotation_text="Sweet spot")
fig_acwr.add_hrect(y0=1.5, y1=5, fillcolor="red", opacity=0.1, annotation_text="Danger zone")
fig_acwr.add_hline(y=1.5, line_dash="dash", line_color="red", opacity=0.5)
fig_acwr.add_hline(y=0.8, line_dash="dash", line_color="green", opacity=0.5)
fig_acwr.update_layout(height=350)
st.plotly_chart(fig_acwr, use_container_width=True)

st.markdown("---")

col_left, col_right = st.columns(2)

# Wellness radar
with col_left:
    st.subheader("Wellness Radar")
    metrics = ["fatigue", "mood", "readiness", "sleep_quality", "soreness", "stress"]
    labels = ["Fatigue", "Mood", "Readiness", "Sleep Quality", "Soreness", "Stress"]
    values = [row[m] if pd.notna(row[m]) else 0 for m in metrics]

    fig_radar = go.Figure(go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        line_color="#185FA5",
        fillcolor="rgba(24,95,165,0.2)",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        height=350,
        title="Wellness Dimensions"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Daily load bar
with col_right:
    st.subheader("Daily Load — Last 30 Days")
    fig_load = px.bar(
        last_30,
        x="date",
        y="daily_load",
        title="Daily Training Load",
        color="daily_load",
        color_continuous_scale="Blues",
    )
    fig_load.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_load, use_container_width=True)