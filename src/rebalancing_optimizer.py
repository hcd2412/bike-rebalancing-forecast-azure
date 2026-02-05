import pandas as pd


def recommend_rebalancing(
    demand_forecast: pd.DataFrame,
    current_inventory: pd.DataFrame,
    max_moves: int = 50,
) -> pd.DataFrame:
    """
    Generate rebalancing recommendations.

    demand_forecast:
        columns = [station_id, hour_ts, predicted_demand]

    current_inventory:
        columns = [station_id, available_bikes]

    Returns:
        DataFrame with columns:
        [from_station, to_station, bikes_to_move]
    """
    # Simple heuristic placeholder:
    # move bikes from stations with surplus to stations with deficit
    surplus = current_inventory.copy()
    surplus["excess"] = surplus["available_bikes"] - surplus["available_bikes"].mean()

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

    return pd.DataFrame(recommendations)
