import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ingest import melt_wide_to_long, ingest_wellness, ingest_training_load, ingest_injury, ingest_game_performance
from validate import validate_all


def test_melt_wide_to_long_shape():
    """Melted output has correct columns and no date nulls."""
    sample = pd.DataFrame({
        "Date": ["01.01.2020", "02.01.2020"],
        "TeamA-abc-123": [5.0, 6.0],
        "TeamB-xyz-456": [3.0, None],
    })
    result = melt_wide_to_long(sample, "load")
    assert "date" in result.columns
    assert "player_id" in result.columns
    assert "team" in result.columns
    assert "load" in result.columns
    assert result["date"].isnull().sum() == 0


def test_melt_wide_to_long_drops_nulls():
    """Null values in the metric column are dropped."""
    sample = pd.DataFrame({
        "Date": ["01.01.2020"],
        "TeamA-abc-123": [None],
        "TeamB-xyz-456": [5.0],
    })
    result = melt_wide_to_long(sample, "load")
    assert len(result) == 1
    assert result.iloc[0]["team"] == "TeamB"


def test_wellness_output_shape():
    """Wellness ingestion produces expected columns."""
    df = ingest_wellness()
    expected_cols = {"date", "player_id", "team", "fatigue", "mood",
                     "readiness", "sleep_duration", "sleep_quality", "soreness", "stress"}
    assert expected_cols.issubset(set(df.columns))
    assert len(df) > 0


def test_training_load_output_shape():
    """Training load ingestion produces expected columns."""
    df = ingest_training_load()
    expected_cols = {"date", "player_id", "team", "daily_load", "acwr", "atl", "ctl28"}
    assert expected_cols.issubset(set(df.columns))
    assert len(df) > 0


def test_injury_output_shape():
    """Injury ingestion produces expected columns and row count."""
    df = ingest_injury()
    assert set(df.columns) == {"date", "player_id", "team", "type"}
    assert len(df) == 162


def test_game_performance_output_shape():
    """Game performance ingestion produces expected columns and row count."""
    df = ingest_game_performance()
    assert set(df.columns) == {"date", "player_id", "team",
                                "team_performance", "offensive_performance", "defensive_performance"}
    assert len(df) == 248


def test_all_validations_pass():
    """All Pandera schemas validate cleanly against processed parquet files."""
    assert validate_all() is True