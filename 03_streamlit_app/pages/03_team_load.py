import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_readiness

st.set_page_config(page_title="Team Load", layout="wide")
st.title("📊 Team Load")

df = load_readiness()

with st.sidebar:
    st.header("Filters")
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

st.markdown("---")

# Weekly load chart
st.subheader("Weekly Team Load")
filtered["week"] = filtered["date"].dt.to_period("W").astype(str)
weekly = filtered.groupby(["week", "team"])["daily_load"].sum().reset_index()
weekly.columns = ["Week", "Team", "Total Load"]

fig_weekly = px.bar(
    weekly,
    x="Week",
    y="Total Load",
    color="Team",
    barmode="group",
    title="Total Training Load per Week",
)
fig_weekly.update_layout(height=380, xaxis_tickangle=-45)
st.plotly_chart(fig_weekly, use_container_width=True)

st.markdown("---")

# Load heatmap
st.subheader("Daily Load Heatmap")
heatmap_data = filtered[filtered["daily_load"].notna()].copy()
heatmap_data["date_str"] = heatmap_data["date"].dt.strftime("%Y-%m-%d")
heatmap_data["short_id"] = heatmap_data["player_id"].str[:8]

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
        color_continuous_scale="RdYlGn_r",
        title="Daily Load per Player (last 30 days)",
        aspect="auto",
        labels=dict(x="Date", y="Player", color="Load"),
    )
    fig_heat.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("No load data available for the selected filters.")

st.markdown("---")

# Summary stats
st.subheader("Load Summary")
summary = filtered.groupby("team").agg(
    avg_daily_load=("daily_load", "mean"),
    avg_acwr=("acwr", "mean"),
    avg_wellness=("wellness_score", "mean"),
    total_sessions=("daily_load", "count"),
).round(2).reset_index()
summary.columns = ["Team", "Avg Daily Load", "Avg ACWR", "Avg Wellness", "Total Sessions"]
st.dataframe(summary, use_container_width=True, hide_index=True)