import pandas as pd


def _normalize_inventory_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Accept common inventory column names and normalize to:
      - station_id
      - available_bikes
    """
    out = df.copy()

    # Normalize station id if needed (optional)
    if "station_id" not in out.columns:
        raise ValueError("current_inventory must include 'station_id'")

    # Accept either 'available_bikes' or 'bikes_available'
    if "available_bikes" in out.columns:
        pass
    elif "bikes_available" in out.columns:
        out = out.rename(columns={"bikes_available": "available_bikes"})
    else:
        raise ValueError(
            "current_inventory must include either 'available_bikes' or 'bikes_available'"
        )

    # Ensure numeric
    out["available_bikes"] = pd.to_numeric(out["available_bikes"], errors="coerce").fillna(0)

    return out


def recommend_rebalancing(
    demand_forecast: pd.DataFrame,
    current_inventory: pd.DataFrame,
    max_moves: int = 50,
) -> pd.DataFrame:
    """
    Generate rebalancing recommendations.

    demand_forecast (currently not used by this simple heuristic):
        expected columns could be: [station_id, hour_ts, predicted_demand]
        (kept for future logic)

    current_inventory:
        required columns:
          - station_id
          - available_bikes  (or bikes_available; will be normalized)

    Returns:
        DataFrame with columns:
          - from_station
          - to_station
          - bikes_to_move
    """
    inv = _normalize_inventory_columns(current_inventory)

    # Simple heuristic placeholder:
    # move bikes from stations with surplus to stations with deficit
    surplus = inv.copy()
    mean_bikes = surplus["available_bikes"].mean()
    surplus["excess"] = surplus["available_bikes"] - mean_bikes

    donors = surplus[surplus["excess"] > 0].copy()
    receivers = surplus[surplus["excess"] < 0].copy()

    recommendations = []

    for _, r in receivers.iterrows():
        if donors.empty:
            break

        d = donors.iloc[0]
        bikes = int(min(d["excess"], abs(r["excess"]), max_moves))
        if bikes <= 0:
            continue

        recommendations.append(
            {
                "from_station": d["station_id"],
                "to_station": r["station_id"],
                "bikes_to_move": bikes,
            }
        )

        donors.at[donors.index[0], "excess"] -= bikes

        # If donor no longer has excess, drop it and continue
        if donors.at[donors.index[0], "excess"] <= 0:
            donors = donors.iloc[1:]

    return pd.DataFrame(recommendations)
