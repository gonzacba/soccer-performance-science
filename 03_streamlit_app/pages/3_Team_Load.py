import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_readiness

st.set_page_config(page_title="Team Load", layout="wide", page_icon=None)

st.markdown("""
    <style>
        .metric-card {
            background-color: #1A1D24;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
        }
        .metric-value { font-size: 2rem; font-weight: 700; margin: 0; color: #1D9E75; }
        .metric-label { font-size: 0.85rem; color: #9B9A96; margin: 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="font-size:3rem; font-weight:800; color:#FAFAFA; border-bottom:3px solid #1D9E75; padding-bottom:0.4rem; margin-bottom:1rem;">Team Load</h1>', unsafe_allow_html=True)

df = load_readiness()

with st.sidebar:
    st.markdown("### Filters")
    teams = ["All"] + sorted(df["team"].unique().tolist())
    selected_team = st.selectbox("Team", teams)
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(max_date - pd.Timedelta(weeks=8), max_date),
        min_value=min_date,
        max_value=max_date,
    )

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]
else:
    filtered = df

if selected_team != "All":
    filtered = filtered[filtered["team"] == selected_team]

col1, col2, col3, col4 = st.columns(4)
avg_load = round(float(filtered["daily_load"].mean()), 1) if not filtered.empty else 0
avg_acwr = round(float(filtered["acwr"].mean()), 2) if not filtered.empty else 0
avg_wellness = round(float(filtered["wellness_score"].mean()), 2) if not filtered.empty else 0
total_sessions = filtered["daily_load"].notna().sum()

with col1:
    st.markdown(f'<div class="metric-card"><p class="metric-value">{avg_load}</p><p class="metric-label">Avg Daily Load (AU)</p></div>', unsafe_allow_html=True)
with col2:
    acwr_color = "#1D9E75" if 0.8 <= avg_acwr <= 1.3 else "#EF9F27" if avg_acwr <= 1.5 else "#D85A30"
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{acwr_color}">{avg_acwr}</p><p class="metric-label">Avg ACWR</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p class="metric-value">{avg_wellness}</p><p class="metric-label">Avg Wellness Score</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FAFAFA">{total_sessions}</p><p class="metric-label">Total Sessions</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("#### Weekly Team Load")
filtered["week"] = filtered["date"].dt.to_period("W").dt.start_time
weekly = filtered.groupby(["week", "team"])["daily_load"].sum().reset_index()
weekly.columns = ["Week", "Team", "Total Load"]

fig_weekly = go.Figure()
colors = {"TeamA": "#1D9E75", "TeamB": "#185FA5"}
for team in weekly["Team"].unique():
    team_data = weekly[weekly["Team"] == team]
    fig_weekly.add_trace(go.Bar(
        x=team_data["Week"],
        y=team_data["Total Load"],
        name=team,
        marker_color=colors.get(team, "#888"),
    ))

fig_weekly.update_layout(
    barmode="group",
    height=320,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(gridcolor="#2A2D34", title=""),
    yaxis=dict(gridcolor="#2A2D34", title="Total Load (AU)"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(fig_weekly, use_container_width=True)

st.markdown("---")

st.markdown("#### Daily Load Heatmap — Player × Day")

heatmap_data = filtered[filtered["daily_load"].notna()].copy()
heatmap_data["date_str"] = heatmap_data["date"].dt.strftime("%m/%d")

player_map = {}
for team in heatmap_data["team"].unique():
    team_players = sorted(heatmap_data[heatmap_data["team"] == team]["player_id"].unique())
    for i, pid in enumerate(team_players, 1):
        player_map[pid] = f"{team}-P{str(i).zfill(2)}"

heatmap_data["short_id"] = heatmap_data["player_id"].map(player_map)

pivot = heatmap_data.pivot_table(
    index="short_id",
    columns="date_str",
    values="daily_load",
    aggfunc="mean"
)

if not pivot.empty:
    cols = sorted(pivot.columns)[-30:]
    pivot = pivot[cols]

    fig_heat = px.imshow(
        pivot,
        color_continuous_scale=[[0, "#0E1117"], [0.3, "#185FA5"], [0.7, "#1D9E75"], [1, "#D85A30"]],
        title="Daily Load per Player (last 30 days)",
        aspect="auto",
        labels=dict(x="Date", y="Player", color="Load (AU)"),
    )
    fig_heat.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-45,
        coloraxis_colorbar=dict(
            tickfont=dict(color="#FAFAFA"),
            title=dict(text="Load", font=dict(color="#FAFAFA"))
        ),
    )
    st.plotly_chart(fig_heat, use_container_width=True)