import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_readiness, STATUS_EMOJI, STATUS_COLORS

st.set_page_config(page_title="Squad Overview", layout="wide")
st.title("🏟️ Squad Overview")

df = load_readiness()

with st.sidebar:
    st.header("Filters")
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

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Players", len(filtered))
col2.metric("🟢 Ready", ready)
col3.metric("🟡 Monitor", monitor)
col4.metric("🔴 Load-Managed", load_managed)

st.markdown("---")
st.subheader("Player Readiness")

display = filtered[["player_id", "team", "readiness_status", "wellness_score", "acwr", "daily_load"]].copy()
display["Status"] = display["readiness_status"].map(lambda s: f"{STATUS_EMOJI.get(s, '')} {s}")
display = display.rename(columns={
    "player_id": "Player ID",
    "team": "Team",
    "wellness_score": "Wellness Score",
    "acwr": "ACWR",
    "daily_load": "Daily Load",
})
display = display.drop(columns=["readiness_status"])
display = display[["Player ID", "Team", "Status", "Wellness Score", "ACWR", "Daily Load"]]
display = display.sort_values("Status")

st.dataframe(display, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("Readiness Distribution")

status_counts = filtered["readiness_status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig = px.bar(
    status_counts,
    x="Status",
    y="Count",
    color="Status",
    color_discrete_map=STATUS_COLORS,
    title=f"Squad Readiness — {selected_date}",
    text="Count",
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, height=350)
st.plotly_chart(fig, use_container_width=True)