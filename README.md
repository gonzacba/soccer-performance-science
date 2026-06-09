# soccer-performance-science

![CI](https://github.com/gonzacba/soccer-performance-science/actions/workflows/ci.yml/badge.svg)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://soccer-performance-science.streamlit.app)

A player performance intelligence platform built on SoccerMon data —
modeling training load, readiness, and injury risk for elite soccer athletes.

## Architecture
01_data_pipeline → 02_dbt_models → 03_streamlit_app → 04_prefect

## Stack
Python · dbt · DuckDB · Streamlit · Prefect · Pandera · GitHub Actions