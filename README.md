# Aerospace Supply Chain Verification System

**Python · SQLite · REST API · Workflow Automation · SHA-256 Verification**

A runnable portfolio prototype for tracking aerospace purchase orders through supplier approval, delivery, and verification. Includes a browser dashboard, local REST API, SQL database, and tamper-evident event history.

## Quick start

Requires Python 3.9+; no third-party dependencies.

```bash
python app.py
```

Open **http://localhost:8000**. On first launch the application creates a local SQLite database and inserts three sample orders.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | / | Interactive dashboard |
| GET | /api/orders | List purchase orders |
| GET | /api/metrics | Aggregate counts and order value |
| POST | /api/orders | Create order |
| POST | /api/orders/{id}/approve | Approve order |
| POST | /api/orders/{id}/deliver | Record delivery |
| POST | /api/orders/{id}/verify | Verify delivery |
| GET | /api/orders/{id}/verify | Validate event hash chain |

Create order example:

```bash
curl -X POST http://localhost:8000/api/orders -H "Content-Type: application/json" -d '{"supplier":"Northstar","part":"ACT-204","quantity":12,"unit_cost":845.50}'
```

## Tests

```bash
python -m unittest -v test_app.py
```

## Architecture

Browser dashboard → Python HTTP REST API → SQLite purchase orders and chained audit events.

Each workflow transition appends a SHA-256 hash referencing the previous event. Verification recomputes the hashes to detect changes to stored event data.

## Scope and limitations

This is a **local functional demonstration**, not a production aerospace system or deployed customer solution. It uses sample suppliers and purchase orders. It does **not** connect to SAP, Oracle, SQL Server, or Hedera. Its hash chain is local and is **not a blockchain**. Production deployment would require authentication, authorization, external anchoring, hardened request validation, concurrency controls, and security testing.

**Architecture reference version:** 1.0 | June 2022 (document label, not a deployment date).
