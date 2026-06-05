import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check
from pathlib import Path

PROCESSED_DIR = Path("data/processed")


def load_parquet(name: str) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED_DIR / f"{name}.parquet")


wellness_schema = DataFrameSchema({
    "date": Column(pa.DateTime),
    "player_id": Column(pa.String, nullable=False),
    "team": Column(pa.String, Check.isin(["TeamA", "TeamB"])),
    "fatigue": Column(pa.Float, Check.in_range(1, 7), nullable=True),
    "mood": Column(pa.Float, Check.in_range(1, 7), nullable=True),
    "readiness": Column(pa.Float, Check.in_range(1, 10), nullable=True),
    "sleep_duration": Column(pa.Float, Check.in_range(0, 24), nullable=True),
    "sleep_quality": Column(pa.Float, Check.in_range(1, 7), nullable=True),
    "soreness": Column(pa.Float, Check.in_range(1, 7), nullable=True),
    "stress": Column(pa.Float, Check.in_range(1, 7), nullable=True),
})

training_load_schema = DataFrameSchema({
    "date": Column(pa.DateTime),
    "player_id": Column(pa.String, nullable=False),
    "team": Column(pa.String, Check.isin(["TeamA", "TeamB"])),
    "daily_load": Column(pa.Float, Check.greater_than_or_equal_to(0), nullable=True),
    "weekly_load": Column(pa.Float, Check.greater_than_or_equal_to(0), nullable=True),
    "acwr": Column(pa.Float, Check.in_range(0, 5), nullable=True),
    "atl": Column(pa.Float, Check.greater_than_or_equal_to(0), nullable=True),
    "ctl28": Column(pa.Float, Check.greater_than_or_equal_to(0), nullable=True),
    "strain": Column(pa.Float, nullable=True),
    "monotony": Column(pa.Float, Check.greater_than_or_equal_to(0), nullable=True),
})

injury_schema = DataFrameSchema({
    "date": Column(pa.DateTime),
    "player_id": Column(pa.String, nullable=False),
    "team": Column(pa.String, Check.isin(["TeamA", "TeamB"])),
    "type": Column(pa.String, nullable=False),
})

game_performance_schema = DataFrameSchema({
    "date": Column(pa.DateTime),
    "player_id": Column(pa.String, nullable=False),
    "team": Column(pa.String, Check.isin(["TeamA", "TeamB"])),
    "team_performance": Column(pa.Float, Check.in_range(1, 10), nullable=True),
    "offensive_performance": Column(pa.Float, Check.in_range(1, 10), nullable=True),
    "defensive_performance": Column(pa.Float, Check.in_range(1, 10), nullable=True),
})


def validate_all():
    schemas = {
        "wellness": wellness_schema,
        "training_load": training_load_schema,
        "injury": injury_schema,
        "game_performance": game_performance_schema,
    }

    all_passed = True
    for name, schema in schemas.items():
        try:
            df = load_parquet(name)
            if name == "game_performance":
                for col in ["team_performance", "offensive_performance", "defensive_performance"]:
                    df[col] = df[col].astype(float)
            schema.validate(df)
            print(f"PASS {name}: {len(df)} rows validated")
        except pa.errors.SchemaError as e:
            print(f"FAIL {name}: {e}")
            all_passed = False

    print("\nAll validations passed." if all_passed else "\nSome validations failed.")
    return all_passed


if __name__ == "__main__":
    validate_all()