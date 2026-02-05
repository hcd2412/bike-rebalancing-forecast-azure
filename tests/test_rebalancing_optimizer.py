import pandas as pd

from src.rebalancing_optimizer import recommend_rebalancing


def test_recommend_rebalancing_smoke():
    demand_forecast = pd.DataFrame(
        {
            "station_id": ["A", "B", "C"],
            "hour_ts": ["2024-06-01 10:00:00"] * 3,
            "predicted_demand": [20, 5, 15],
        }
    )

    current_inventory = pd.DataFrame(
        {
            "station_id": ["A", "B", "C"],
            "available_bikes": [5, 25, 10],
        }
    )

    recs = recommend_rebalancing(demand_forecast, current_inventory, max_moves=10)
    assert isinstance(recs, pd.DataFrame)
    assert set(recs.columns) == {"from_station", "to_station", "bikes_to_move"}
