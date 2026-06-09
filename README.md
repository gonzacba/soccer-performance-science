# soccer-performance-science

![CI](https://github.com/gonzacba/soccer-performance-science/actions/workflows/ci.yml/badge.svg)

🚀 **[Live Dashboard](https://soccer-performance-science.streamlit.app)** → Player Readiness App

A player performance intelligence platform built on SoccerMon athlete monitoring data, modeling training load, readiness, and injury risk for elite soccer athletes.

---

## Architecture

```mermaid
flowchart LR
    SRC([SoccerMon Open Data])

    subgraph P1["01 · Data Pipeline"]
        direction TB
        ING["ingest.py — 16 CSVs to Parquet"]
        VAL["validate.py — Pandera schemas"]
        TST["pytest — 7 tests"]
        ING --> VAL --> TST
    end

    subgraph P2["02 · dbt Models — DuckDB"]
        direction TB
        BASE["base — clean + cast"]
        STG["staging — join + ACWR score"]
        MRT["marts — readiness + injury risk"]
        DBT["21 dbt tests"]
        BASE --> STG --> MRT --> DBT
    end

    subgraph P3["03 · Streamlit Dashboard"]
        direction TB
        PG1["Squad Overview"]
        PG2["Player Drill-Down"]
        PG3["Team Load"]
    end

    subgraph P4["04 · Prefect"]
        SCH["Daily 6AM schedule"]
    end

    SRC --> P1
    P1 --> P2
    P2 --> P3
    P4 -->|orchestrates| P1
    P4 -->|orchestrates| P2
    P3 --> LIVE([Live Dashboard — streamlit.app])

    style P1 fill:#003366,stroke:#003366,color:#fff
    style P2 fill:#003366,stroke:#003366,color:#fff
    style P3 fill:#003366,stroke:#003366,color:#fff
    style P4 fill:#CC0000,stroke:#CC0000,color:#fff
    style SRC fill:#126BD9,stroke:#126BD9,color:#fff
    style LIVE fill:#126BD9,stroke:#126BD9,color:#fff
```

---

## Stack

| Layer | Technology |
|---|---|
| Ingestion | Python · pandas · PyArrow |
| Validation | Pandera · pytest |
| Transformation | dbt Core · DuckDB |
| Dashboard | Streamlit · Plotly |
| Orchestration | Prefect |
| CI/CD | GitHub Actions |
| Data | SoccerMon (Zenodo · CC BY 4.0) |

---

## Project Structure

```
soccer-performance-science/
├── 01_data_pipeline/        # Python ETL: ingest, validate, test
├── 02_dbt_models/           # dbt Core: base, staging, mart layers
├── 03_streamlit_app/        # Streamlit dashboard: 3 pages
├── 04_prefect/              # Prefect orchestration: daily pipeline
└── data/
    ├── raw/                 # SoccerMon source CSVs (not committed)
    └── processed/           # Parquet outputs
```

---

## Key Insights from the Data

- **TeamA showed consistently higher ACWR spikes** than TeamB throughout the 2021 season — suggesting different periodization philosophies between the two squads
- **162 injury events across 50 players** over 2 seasons: 1.6 injuries per player per year, consistent with elite soccer benchmarks
- **Wellness scores dip the day after match days**, validating the readiness model's classification logic against real athlete behavior

---

## How to Run Locally

```bash
# 1. Clone and install
git clone https://github.com/gonzacba/soccer-performance-science.git
cd soccer-performance-science
pip install -r 01_data_pipeline/requirements.txt
pip install dbt-core dbt-duckdb streamlit plotly prefect

# 2. Download SoccerMon subjective data from Zenodo
# https://zenodo.org/records/10033832 → subjective.zip → extract to data/raw/

# 3. Run the full pipeline
python 04_prefect/flows/performance_pipeline.py

# 4. Launch the dashboard
cd 03_streamlit_app
streamlit run app.py
```

---

## Data Source

SoccerMon: A Soccer Monitoring Dataset  
Zenodo · https://zenodo.org/records/10033832  
License: CC BY 4.0
