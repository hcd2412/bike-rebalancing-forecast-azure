from fastapi import FastAPI
import pandas as pd

from src.rebalancing_optimizer import recommend_rebalancing

app = FastAPI(title="Bike Rebalancing API")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/rebalance")
def rebalance(payload: dict):
    """
    Expected payload:
    {
        "demand_forecast": [...],
        "current_inventory": [...]
    }
    """
    demand_forecast = pd.DataFrame(payload["demand_forecast"])
    current_inventory = pd.DataFrame(payload["current_inventory"])

    recs = recommend_rebalancing(demand_forecast, current_inventory)

    return recs.to_dict(orient="records")
