# Medicaid Billing Anomaly Detection Platform

An end-to-end AI-powered platform that detects and explains anomalous billing patterns in public Medicaid claims data.

## What It Does
- Ingests 238M+ provider claims records using DuckDB (zero memory overhead)
- Detects statistically anomalous billing patterns using Isolation Forest
- Generates human-readable explanations per flagged provider
- Serves findings via FastAPI REST API
- Visualizes results in an interactive React dashboard
- Allows natural language queries via RAG chat interface

## Tech Stack
| Layer | Technology |
|---|---|
| Data ingestion | DuckDB, Python |
| ML model | Isolation Forest (scikit-learn) |
| Backend | FastAPI |
| Frontend | React, Recharts |
| AI chat | LangChain, OpenAI |
| Deployment | Docker |

## Key Finding (Demo Dataset)
Using the publicly available HHS Medicaid provider spending dataset (2018–2024), the platform flagged 127,349 anomalous provider-code combinations out of 12.7M analyzed — including providers billing 5,000x the national average for home health codes.

## How to Run
```bash
docker-compose up
```

## Author
Pooja Sri | github.com/poojasri7
