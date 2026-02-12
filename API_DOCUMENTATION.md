# API Documentation

Base URL:
http://localhost:8000

---

## POST /api/events

Ingest AI event.

Request Body:

{
  "timestamp": "2026-01-15T10:15:00Z",
  "worker_id": "W1",
  "workstation_id": "S3",
  "event_type": "working",
  "confidence": 0.93,
  "count": 1
}

Response:

201 Created
{ "message": "Event stored" }

200 OK (duplicate)
{ "message": "Duplicate ignored" }

---

## POST /api/seed

Seeds database.

Response:

{ "message": "Database seeded successfully" }

---

## GET /api/metrics/workers

Returns worker metrics array.

---

## GET /api/metrics/stations

Returns workstation metrics.

---

## GET /api/metrics/factory

Returns factory summary.

---

## GET /health

Returns system health.

Response:

{
  "status": "ok",
  "cpu_usage": 23.5,
  "ram_usage_percent": 45.1,
  "ram_used_mb": 1890,
  "ram_total_mb": 8192
}

---

## WebSocket Event

Event Name:
live_update

Payload:

{
  "factory": {...},
  "workers": [...],
  "health": {...}
}
