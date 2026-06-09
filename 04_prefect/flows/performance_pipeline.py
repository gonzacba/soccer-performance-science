from prefect import flow, task
from prefect.logging import get_run_logger
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_DIR = ROOT / "01_data_pipeline"
DBT_DIR = ROOT / "02_dbt_models"


@task(name="Ingest Data", retries=2, retry_delay_seconds=30)
def ingest_data():
    logger = get_run_logger()
    logger.info("Starting ingestion...")
    result = subprocess.run(
        [sys.executable, str(PIPELINE_DIR / "ingest.py")],
        capture_output=True,
        text=True
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Ingestion failed: {result.stderr}")
    logger.info("Ingestion complete.")


@task(name="Validate Data", retries=1)
def validate_data():
    logger = get_run_logger()
    logger.info("Running validation...")
    result = subprocess.run(
        [sys.executable, str(PIPELINE_DIR / "validate.py")],
        capture_output=True,
        text=True
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Validation failed: {result.stderr}")
    logger.info("Validation complete.")


@task(name="Run dbt Models", retries=1)
def run_dbt_models():
    logger = get_run_logger()
    for cmd in [["dbt", "run"], ["dbt", "test"]]:
        logger.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd + ["--profiles-dir", "."],
            cwd=DBT_DIR,
            capture_output=True,
            text=True
        )
        logger.info(result.stdout)
        if result.returncode != 0:
            raise Exception(f"{cmd[1]} failed: {result.stderr}")
    logger.info("dbt complete.")


@task(name="Verify Marts")
def verify_marts():
    import duckdb
    logger = get_run_logger()
    logger.info("Verifying mart tables...")
    conn = duckdb.connect(str(ROOT / "data" / "soccer_performance.duckdb"))
    for table in ["mart_readiness", "mart_injury_risk"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        logger.info(f"{table}: {count} rows")
        if count == 0:
            raise Exception(f"{table} is empty!")
    conn.close()
    logger.info("All marts verified.")


@flow(
    name="Soccer Performance Pipeline",
    description="Daily ingest, validate, dbt run, and mart verification"
)
def performance_pipeline():
    ingest_data()
    validate_data()
    run_dbt_models()
    verify_marts()


if __name__ == "__main__":
    performance_pipeline()