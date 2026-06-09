# soccer-performance-science

![CI](https://github.com/gonzacba/soccer-performance-science/actions/workflows/ci.yml/badge.svg)

🚀 **[Live Dashboard](https://soccer-performance-science.streamlit.app)** — Player Readiness App

A player performance intelligence platform built on SoccerMon athlete monitoring data — modeling training load, readiness, and injury risk for elite soccer athletes.

---

## Architecture

```mermaid
flowchart TD
    A[SoccerMon Open Data\nZenodo · CC BY 4.0] --> B

    subgraph B[01_data_pipeline]
        B1[ingest.py\nwide to long · Parquet] --> B2[validate.py\nPandera schemas]
        B2 --> B3[pytest · 7 tests]
    end

    B --> C[(data/processed/\nwellness · training_load\ninjury · game_performance)]

    C --> D

    subgraph D[02_dbt_models · DuckDB]
        D1[base/\nclean + cast] --> D2[staging/\njoin + composite score]
        D2 --> D3[marts/\nreadiness + injury risk]
        D3 --> D4[schema.yml\n21 dbt tests]
    end

    D --> E[(soccer_performance.duckdb\nmart_readiness · mart_injury_risk)]

    E --> F

    subgraph F[03_streamlit_app]
        F1[Squad Overview\ngreen · amber · red status]
        F2[Player Drill-Down\nACWR trend · wellness radar]
        F3[Team Load\nperiodization · heatmap]
    end

    G[04_prefect\nDaily 6AM schedule] -->|orchestrates| B
    G -->|orchestrates| D
    G -->|verifies| E

    F --> H[Live Dashboard\nsoccer-performance-science.streamlit.app]
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
├── 01_data_pipeline/        # Python ETL — ingest, validate, test
├── 02_dbt_models/           # dbt Core — base, staging, mart layers
├── 03_streamlit_app/        # Streamlit dashboard — 3 pages
├── 04_prefect/              # Prefect orchestration — daily pipeline
└── data/
    ├── raw/                 # SoccerMon source CSVs (not committed)
    └── processed/           # Parquet outputs
```

---

## Key Insights from the Data

- **TeamA showed consistently higher ACWR spikes** than TeamB throughout the 2021 season — suggesting different periodization philosophies between the two squads
- **162 injury events across 50 players** over 2 seasons — 1.6 injuries per player per year, consistent with elite soccer benchmarks
- **Wellness scores dip the day after match days** — validating the readiness model's classification logic against real athlete behavior

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
