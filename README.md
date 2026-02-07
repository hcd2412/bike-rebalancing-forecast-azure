# Bike Rebalancing Forecast (Azure)

Portfolio project demonstrating **senior-level predictive and prescriptive analytics**, deployed as a lightweight API on **Azure Container Apps**.

The project emphasizes **end-to-end system design**, from data aggregation and demand modeling to optimization-driven decision making and cloud deployment.

## What this project does
1) **Aggregate demand** from Citi Bike trip data into **station × hour** demand signals  
2) Train a **baseline demand model** (hour-of-day / day-of-week features)  
3) Generate **rebalancing recommendations** (move bikes from surplus → deficit stations) using **OR-Tools**  
4) Serve recommendations via a **FastAPI** endpoint

## High-level architecture

```text
                  ┌───────────────────────────────────────────┐
                  │        NYC Citi Bike Trip Data (CSV)      │
                  │   data/raw/202406-..._1..5.csv (ignored)  │
                  └─────────────────────────┬─────────────────┘
                                            │
                                            ▼
                  ┌───────────────────────────────────────────┐
                  │      Data Aggregation (Python/Pandas)     │
                  │  src/data_aggregation.py                  │
                  │  → station_id × hour_ts → ride_count      │
                  └─────────────────────────┬─────────────────┘
                                            │
                                            ├───────────────┐
                                            │               │
                                            ▼               ▼
        ┌───────────────────────────┐   ┌────────────────────────────┐
        │  Demand Modeling Notebook │   │   Rebalancing Optimizer    │
        │  notebooks/02_...ipynb    │   │   src/rebalancing_optimizer│
        │  Features: hour, dow      │   │   OR-Tools                 │
        │  Output: predicted_demand │   │   Output: move plan        │
        └───────────────┬───────────┘   └───────────────┬────────────┘
                        │                               │
                        └───────────────┬───────────────┘
                                        │
                                        ▼
                         ┌────────────────────────────────┐
                         │         FastAPI Service        │
                         │         src/api.py             │
                         │  GET  /  → {"status":"ok"}     │
                         │  POST /rebalance → move plan   │
                         └────────────────┬───────────────┘
                                          │
                                          ▼
                         ┌────────────────────────────────┐
                         │      Azure Container Apps      │
                         │   (build from GitHub repo)     │
                         │   Public ingress (HTTP)        │
                         └────────────────────────────────┘
```


## Dataset
- Source: NYC Citi Bike Trip Data (monthly exports)
- Raw files are kept in `data/raw/` (ignored in git). Only `data/raw/README.md` is tracked.

## Repo structure
- `src/data_aggregation.py` — load + hourly demand aggregation
- `notebooks/01_data_exploration.ipynb` — schema + basic patterns
- `notebooks/02_demand_modeling.ipynb` — baseline model + evaluation
- `src/rebalancing_optimizer.py` — optimization logic (OR-Tools)
- `src/api.py` — FastAPI service (`/` health + `/rebalance` endpoint)

## API (local)
Run:
```bash
uvicorn src.api:app --reload --port 8000
```

Test:

```bash
curl http://127.0.0.1:8000/
```

Rebalance example:

```bash
curl -X POST http://127.0.0.1:8000/rebalance \
  -H "Content-Type: application/json" \
  -d '{
    "demand_forecast": [
      {"station_id": "A", "hour_ts": "2024-06-01T10:00:00", "predicted_demand": 20},
      {"station_id": "B", "hour_ts": "2024-06-01T10:00:00", "predicted_demand": 5},
      {"station_id": "C", "hour_ts": "2024-06-01T10:00:00", "predicted_demand": 15}
    ],
    "current_inventory": [
      {"station_id": "A", "available_bikes": 5},
      {"station_id": "B", "available_bikes": 25},
      {"station_id": "C", "available_bikes": 10}
    ]
  }'
```

## Status

* ✅ Data ingestion + hourly aggregation
* ✅ Baseline demand model (first pass)
* ✅ Rebalancing API (FastAPI)
* 🔄 Azure Container Apps deployment (cloud build + ingress setup)
* ⏭ Next: better features + time-series baseline, station clustering, and cost-aware routing constraints

