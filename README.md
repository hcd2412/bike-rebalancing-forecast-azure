# Bike Rebalancing Forecast (Azure)

## Live Demo

- API base: https://bike-rebalancing-api.braveground-cb6072c0.canadacentral.azurecontainerapps.io/
- Swagger UI: https://bike-rebalancing-api.braveground-cb6072c0.canadacentral.azurecontainerapps.io/docs
- Health check: https://bike-rebalancing-api.braveground-cb6072c0.canadacentral.azurecontainerapps.io/

Portfolio project demonstrating **senior-level predictive and prescriptive analytics**, deployed as a lightweight API on **Azure Container Apps**.

The project emphasizes **end-to-end system design**, from data aggregation and demand modeling to optimization-driven decision making and cloud deployment.

## Why This Matters

Urban mobility systems fail not because of missing data, but because of
poor decision logic under constraints.

This project demonstrates how to:
- translate noisy demand signals into **actionable decisions**
- combine **forecasting + optimization + governance**
- expose decisions through a **human-reviewable API**
- deploy a decision system safely to the cloud

The same design applies to logistics, energy, telecom, smart cities,
and public-sector infrastructure.

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
                  └─────────────────────┬─────────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │      Data Aggregation (Python/Pandas)     │
                  │  src/data_aggregation.py                  │
                  │  → station_id × hour_ts → ride_count      │
                  └─────────────────────┬─────────────────────┘
                                        │
                  ┌─────────────────────┴─────────────────────┐
                  │                                           │
                  ▼                                           ▼
        ┌───────────────────────────┐   ┌────────────────────────────────────┐
        │  Demand Modeling Notebook │   │         Rebalancing Optimizer      │
        │  notebooks/02_...ipynb    │   │   src/rebalancing_optimizer.py     │
        │  Features: hour, dow      │   │   Inputs:                          │
        │  Output: predicted_demand │   │     - predicted_demand (forecast)  │
        └───────────────┬───────────┘   │     - current_inventory (state)    │
                        │               │   OR-Tools / constrained decision  │
                        └──────────────▶│   Output: move plan                │
                                        └───────────┬────────────────────────┘
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
*This architecture separates analytics, forecasting, and decision logic to ensure explainable, constraint-governed operational decisions.*


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

## Design Patterns

This system implements the **Surplus–Deficit Balancing** decision pattern,
documented in the companion repository:

- https://github.com/hcd2412/decision-systems-patterns/tree/main/patterns/01-surplus-deficit-balancing.md

The API exposes a constrained, explainable decision surface rather than
direct unconstrained optimization, allowing human review and safe
operational deployment.

## Status

* ✅ Data ingestion + hourly aggregation
* ✅ Baseline demand model (first pass)
* ✅ Rebalancing API (FastAPI)
* 🔄 Azure Container Apps deployment (cloud build + ingress setup)
* ⏭ Next: better features + time-series baseline, station clustering, and cost-aware routing constraints

