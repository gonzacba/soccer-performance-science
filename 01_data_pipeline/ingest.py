import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import json
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def melt_wide_to_long(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    date_col = df.columns[0]
    df = df.rename(columns={date_col: "date"})
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
    melted = df.melt(id_vars="date", var_name="player_id", value_name=value_name)
    melted["team"] = melted["player_id"].str.split("-").str[0]
    melted["player_id"] = melted["player_id"].str.split("-", n=1).str[1]
    return melted.dropna(subset=[value_name])


def ingest_wellness() -> pd.DataFrame:
    wellness_files = {
        "fatigue": "fatigue.csv",
        "mood": "mood.csv",
        "readiness": "readiness.csv",
        "sleep_duration": "sleep_duration.csv",
        "sleep_quality": "sleep_quality.csv",
        "soreness": "soreness.csv",
        "stress": "stress.csv",
    }

    dfs = []
    for metric, filename in wellness_files.items():
        df = pd.read_csv(RAW_DIR / "wellness" / filename)
        melted = melt_wide_to_long(df, value_name=metric)
        dfs.append(melted.set_index(["date", "player_id", "team"]))

    combined = pd.concat(dfs, axis=1).reset_index()
    print(f"Wellness: {combined.shape[0]} rows, {combined.shape[1]} columns")
    return combined


def ingest_training_load() -> pd.DataFrame:
    load_files = {
        "daily_load": "daily_load.csv",
        "weekly_load": "weekly_load.csv",
        "acwr": "acwr.csv",
        "atl": "atl.csv",
        "ctl28": "ctl28.csv",
        "strain": "strain.csv",
        "monotony": "monotony.csv",
    }

    dfs = []
    for metric, filename in load_files.items():
        df = pd.read_csv(RAW_DIR / "training-load" / filename)
        melted = melt_wide_to_long(df, value_name=metric)
        dfs.append(melted.set_index(["date", "player_id", "team"]))

    combined = pd.concat(dfs, axis=1).reset_index()
    print(f"Training load: {combined.shape[0]} rows, {combined.shape[1]} columns")
    return combined


def ingest_injury() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "injury" / "injury.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y")
    df = df.rename(columns={"timestamp": "date"})
    df["team"] = df["player_name"].str.split("-").str[0]
    df["player_id"] = df["player_name"].str.split("-", n=1).str[1]
    df = df.drop(columns=["player_name"])
    print(f"Injury: {df.shape[0]} rows")
    return df


def ingest_game_performance() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "game-performance" / "game-performance.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y")
    df = df.rename(columns={"timestamp": "date"})
    df["team"] = df["player_name"].str.split("-").str[0]
    df["player_id"] = df["player_name"].str.split("-", n=1).str[1]
    df = df.drop(columns=["player_name"])
    print(f"Game performance: {df.shape[0]} rows")
    return df


def save_parquet(df: pd.DataFrame, name: str):
    path = OUT_DIR / f"{name}.parquet"
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)
    print(f"Saved: {path}")


if __name__ == "__main__":
    print("Starting ingestion...\n")

    wellness = ingest_wellness()
    save_parquet(wellness, "wellness")

    training_load = ingest_training_load()
    save_parquet(training_load, "training_load")

    injury = ingest_injury()
    save_parquet(injury, "injury")

    game_perf = ingest_game_performance()
    save_parquet(game_perf, "game_performance")

    print("\nIngestion complete.")