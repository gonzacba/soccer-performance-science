import duckdb
import pandas as pd
import streamlit as st
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "soccer_performance.duckdb"


@st.cache_data
def load_readiness() -> pd.DataFrame:
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    df = conn.execute("SELECT * FROM mart_readiness").df()
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def load_injury_risk() -> pd.DataFrame:
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    df = conn.execute("SELECT * FROM mart_injury_risk").df()
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df


STATUS_COLORS = {
    "Ready":        "#1D9E75",
    "Monitor":      "#EF9F27",
    "Load-Managed": "#D85A30",
}

RISK_COLORS = {
    "Normal":   "#1D9E75",
    "Elevated": "#EF9F27",
    "High":     "#D85A30",
}

STATUS_EMOJI = {
    "Ready":        "🟢",
    "Monitor":      "🟡",
    "Load-Managed": "🔴",
}