import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_readiness, load_injury_risk, STATUS_COLORS, RISK_COLORS

st.set_page_config(page_title="Player Drill-Down", layout="wide", page_icon=None)

st.markdown("""
    <style>
        .metric-card {
            background-color: #1A1D24;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
        }
        .metric-value { font-size: 2rem; font-weight: 700; margin: 0; }
        .metric-label { font-size: 0.85rem; color: #9B9A96; margin: 0; }
        .player-info {
            font-size: 1rem;
            color: #9B9A96;
            margin-bottom: 1.5rem;
        }
        .player-info strong {
            color: #FAFAFA;
            font-size: 1.05rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="font-size:3rem; font-weight:800; color:#FAFAFA; border-bottom:3px solid #1D9E75; padding-bottom:0.4rem; margin-bottom:1rem;">Player Drill-Down</h1>', unsafe_allow_html=True)

df = load_readiness()
risk_df = load_injury_risk()

player_map = {}
for team in df["team"].unique():
    team_players = sorted(df[df["team"] == team]["player_id"].unique())
    for i, pid in enumerate(team_players, 1):
        player_map[pid] = f"{team}-P{str(i).zfill(2)}"

reverse_map = {v: k for k, v in player_map.items()}

with st.sidebar:
    st.markdown("### Filters")
    teams = sorted(df["team"].unique().tolist())
    selected_team = st.selectbox("Team", teams)
    team_labels = sorted([v for k, v in player_map.items() if df[df["player_id"] == k]["team"].iloc[0] == selected_team])
    selected_label = st.selectbox("Player", team_labels)
    selected_player = reverse_map[selected_label]
    dates = sorted(df["date"].dt.date.unique(), reverse=True)
    selected_date = st.selectbox("Date", dates)

player_df = df[df["player_id"] == selected_player].sort_values("date")
today = player_df[player_df["date"].dt.date == selected_date]

if today.empty:
    st.warning("No data for this player on the selected date.")
    st.stop()

row = today.iloc[0]
status = row["readiness_status"]
status_color = STATUS_COLORS.get(status, "#888")

st.markdown(f"""
    <div class="player-info">
        <strong>{selected_label}</strong>
        <span style="margin: 0 0.5rem; color:#2A2D34;">|</span>
        {selected_team}
        <span style="margin: 0 0.5rem; color:#2A2D34;">|</span>
        {selected_date}
        <span style="margin-left:1rem; color:{status_color}; font-weight:600;">● {status}</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
wellness = round(float(row["wellness_score"]), 2) if pd.notna(row["wellness_score"]) else "N/A"
acwr = round(float(row["acwr"]), 3) if pd.notna(row["acwr"]) else "N/A"
load = int(row["daily_load"]) if pd.notna(row["daily_load"]) else "N/A"

acwr_color = "#1D9E75" if isinstance(acwr, float) and 0.8 <= acwr <= 1.3 else "#EF9F27" if isinstance(acwr, float) and acwr <= 1.5 else "#D85A30"
wellness_color = "#1D9E75" if isinstance(wellness, float) and wellness >= 6 else "#EF9F27" if isinstance(wellness, float) and wellness >= 4.5 else "#D85A30"

with col1:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{wellness_color}">{wellness}</p><p class="metric-label">Wellness Score</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{acwr_color}">{acwr}</p><p class="metric-label">ACWR</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FAFAFA">{load}</p><p class="metric-label">Daily Load (AU)</p></div>', unsafe_allow_html=True)
with col4:
    risk_row = risk_df[(risk_df["player_id"] == selected_player) & (risk_df["date"].dt.date == selected_date)]
    risk = risk_row.iloc[0]["risk_level"] if not risk_row.empty else "N/A"
    risk_color = RISK_COLORS.get(risk, "#888")
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{risk_color}">{risk}</p><p class="metric-label">Injury Risk</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

last_30 = player_df[player_df["date"].dt.date <= selected_date].tail(30)

fig_acwr = go.Figure()
fig_acwr.add_hrect(y0=0.8, y1=1.3, fillcolor="#1D9E75", opacity=0.08, line_width=0, annotation_text="Sweet spot", annotation_position="top left")
fig_acwr.add_hrect(y0=1.5, y1=5, fillcolor="#D85A30", opacity=0.08, line_width=0, annotation_text="Danger zone", annotation_position="top left")
fig_acwr.add_trace(go.Scatter(
    x=last_30["date"], y=last_30["acwr"],
    mode="lines+markers",
    line=dict(color="#1D9E75", width=2.5),
    marker=dict(size=6, color="#1D9E75"),
    name="ACWR"
))
fig_acwr.add_hline(y=1.5, line_dash="dash", line_color="#D85A30", opacity=0.6)
fig_acwr.add_hline(y=0.8, line_dash="dash", line_color="#1D9E75", opacity=0.6)
fig_acwr.update_layout(
    title=dict(text="Acute:Chronic Workload Ratio — Last 30 Days", font=dict(size=14)),
    height=320,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(gridcolor="#2A2D34"),
    yaxis=dict(gridcolor="#2A2D34"),
    showlegend=False,
)
st.plotly_chart(fig_acwr, use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Wellness Radar")
    metrics = ["fatigue", "mood", "readiness", "sleep_quality", "soreness", "stress"]
    labels = ["Fatigue", "Mood", "Readiness", "Sleep", "Soreness", "Stress"]
    values = [row[m] if pd.notna(row[m]) else 0 for m in metrics]

    fig_radar = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        line=dict(color="#1D9E75", width=2),
        fillcolor="rgba(29,158,117,0.2)",
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="#2A2D34", color="#9B9A96"),
            angularaxis=dict(gridcolor="#2A2D34"),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=30),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.markdown("#### Daily Load — Last 30 Days")
    fig_load = go.Figure(go.Bar(
        x=last_30["date"],
        y=last_30["daily_load"],
        marker=dict(
            color=last_30["daily_load"],
            colorscale=[[0, "#185FA5"], [0.5, "#1D9E75"], [1, "#D85A30"]],
            showscale=False,
        ),
    ))
    fig_load.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#2A2D34"),
        yaxis=dict(gridcolor="#2A2D34", title="Load (AU)"),
        showlegend=False,
    )
    st.plotly_chart(fig_load, use_container_width=True)