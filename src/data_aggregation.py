from pathlib import Path
import pandas as pd


def load_trip_data(raw_dir: Path) -> pd.DataFrame:
    """
    Load and concatenate Citi Bike trip CSV files.
    """
    files = sorted(raw_dir.glob("202406-citibike-tripdata_*.csv"))
    dfs = [pd.read_csv(f, low_memory=False) for f in files]
    return pd.concat(dfs, ignore_index=True)


def aggregate_hourly_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate rides by station and hour.
    """
    df = df.copy()
    df["started_at"] = pd.to_datetime(df["started_at"])
    df["hour_ts"] = df["started_at"].dt.floor("h")

    agg = (
        df.groupby(["start_station_id", "hour_ts"])
        .size()
        .reset_index(name="ride_count")
    )

    return agg
