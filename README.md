# AI-Powered Worker Productivity Dashboard

### Real-Time Factory Monitoring System (Flask + WebSockets)

---

# Why Flask?

We initially evaluated building this system using Django due to its strong ecosystem and built-in administrative tooling. However, for this assessment scope and the required architectural flexibility, **Flask was selected deliberately** for the following reasons:

- **Lightweight and modular** — minimal overhead for a focused real-time system.
- **Fine-grained control** over routing, background tasks, and WebSocket integration.
- **Better fit for streaming architectures** when combined with Flask-SocketIO.
- Simplified integration of custom middleware (IP filtering, CORS control, firewall rules).
- Clear separation between API services and dashboard rendering using Jinja templates.

For an **industrial-scale deployment**, we would strongly consider:

- **Django** (for enterprise admin tooling and larger teams), or
- **Golang** for high-throughput API and networking workloads requiring extreme concurrency and lower memory footprint.

Flask provided the optimal balance of simplicity, extensibility, and real-time capability for this system.

---

# Project Overview

This system simulates an AI-powered CCTV monitoring platform that:

1. Ingests structured AI event data.
2. Stores events in a database.
3. Computes worker, workstation, and factory productivity metrics.
4. Streams real-time updates to a dashboard using WebSockets.
5. Displays live system health (CPU and RAM usage).

The result is a **real-time industrial monitoring dashboard prototype**.

---

# Architecture Overview

```
AI Cameras (Simulated)
        │
        ▼
Flask API (Event Ingestion)
        │
        ▼
SQLite Database
        │
        ▼
Metrics Engine
        │
        ▼
Flask-SocketIO (WebSockets)
        │
        ▼
Interactive Dashboard (Tailwind + Jinja)
```

---

# Edge → Backend → Dashboard Flow

##  Edge Layer (Cameras)

- AI system generates structured JSON events.
- Events include:
  - timestamp
  - worker_id
  - workstation_id
  - event_type
  - confidence
  - count (for production)

In this implementation:

- A background simulator generates events every 5 seconds.
- Mimics live monitoring environment.

---

##  Backend Layer

### Event Ingestion API

```
POST /api/events
```

- Validates required fields.
- Parses ISO timestamps.
- Verifies worker and workstation.
- Deduplicates using SHA256 hash.
- Stores events in database.

---

### Metrics Engine

Metrics are computed dynamically by:

- Ordering events by timestamp.
- Calculating duration between consecutive events.
- Aggregating based on event type.

---

### WebSocket Streaming

Using **Flask-SocketIO + Eventlet**, the backend:

- Broadcasts live updates every 5 seconds.
- Streams:
  - Worker metrics
  - Factory metrics
  - System health

No polling is used.

---

##  Dashboard Layer

Built using:

- Jinja Templates
- Tailwind CSS
- Glassmorphism design
- WebSocket live updates

Features:

- Fixed top summary panel
- Scrollable content region
- Worker cards (CCTV-style layout)
- Search filtering
- Dark/Light theme toggle
- Health badge with CPU + RAM
- Live metric updates without reload

---

# Database Schema

## Workers

| Field     | Type    |
| --------- | ------- |
| id        | Integer |
| worker_id | String  |
| name      | String  |

---

## Workstations

| Field      | Type    |
| ---------- | ------- |
| id         | Integer |
| station_id | String  |
| name       | String  |

---

## Events

| Field          | Type     |
| -------------- | -------- |
| id             | Integer  |
| timestamp      | DateTime |
| worker_id      | FK       |
| workstation_id | FK       |
| event_type     | String   |
| confidence     | Float    |
| count          | Integer  |
| event_hash     | String   |

---

# Metric Definitions

## Worker-Level

- **Active Time** → Sum of durations where event_type = "working"
- **Idle Time** → Sum of durations where event_type = "idle"
- **Utilization %** → Active / (Active + Idle)
- **Units Produced** → Sum of product_count events
- **Units per Hour (UPH)** → Units / Active Hours

---

## Workstation-Level

- **Occupancy Time** → Working duration at station
- **Utilization %** → Occupancy / shift duration
- **Total Units**
- **Throughput Rate**

---

## Factory-Level

- Total Active Hours
- Total Units
- Average Utilization
- Average Production Rate

---

# Assumptions & Tradeoffs

- Duration = difference between current and next event timestamp.
- Last event duration = current_time - last_event_timestamp.
- Confidence values currently not weighted in calculations.
- SQLite chosen for simplicity (not high-throughput production).

Tradeoff:

- Real-time metrics computed in memory.
- Not yet optimized for 100k+ events per minute.

---

# Handling Theoretical Questions

## Intermittent Connectivity

Handled by:

- Idempotent ingestion using event_hash.
- Late events accepted.
- Metrics sorted by timestamp.
- WebSocket reconnection handled automatically.

Production improvement:

- Edge device buffering.
- Message queue (Kafka/Redis).

---

##  Duplicate Events

Handled using:

- SHA256 hash of event payload.
- Duplicate ignored before insertion.

This ensures safe retry logic.

---

##  Out-of-Order Timestamps

Metrics engine:

- Always sorts events by timestamp before aggregation.
- Late events correctly integrated.

---

##  Model Versioning

Future addition:

- Add `model_version` column in Event table.
- Store AI model metadata.
- Track performance by model version.

---

## Detecting Model Drift

Possible strategies:

- Monitor drop in average confidence.
- Monitor production rate anomalies.
- Compare distribution shifts over time.
- Alert when deviation threshold exceeded.

---

## Trigger Retraining

Automatic trigger conditions:

- Sustained confidence degradation.
- High variance in production rate.
- Manual override by supervisor.

Would integrate with:

- MLOps pipeline (MLflow or Kubeflow).

---

##  Scaling Strategy

### From 5 Cameras → 100+ Cameras

- Replace SQLite with PostgreSQL.
- Introduce Redis for caching.
- Use Gunicorn + multiple workers.
- Deploy behind Nginx.

---

### Multi-Site Deployment

Add:

- site_id column.
- Partition database by site.
- Horizontal scaling via container orchestration.

---

# Dockerization

Production server:

```
Gunicorn + Eventlet worker
```

Start system:

```
docker compose up --build
```

Access:

```
http://localhost:8000
```

---

# Security Expansion Possibilities

This architecture allows easy extension to:

- Protected login routes (JWT/Auth).
- IP-based ingestion firewall.
- IP allowlist for dashboard.
- Strict CORS enforcement.
- Rate limiting on ingestion.
- TLS termination via Nginx.
- API token validation for camera authentication.

---

# Future Improvements

- Replace polling entirely with Redis Pub/Sub.
- Add WebSocket authentication.
- Add role-based dashboard access.
- Implement anomaly detection module.
- Add real-time charts.
- Introduce Celery for heavy aggregation jobs.
- Migrate to PostgreSQL cluster.
- Add audit logs.
- Multi-tenant support.

---

# Final Summary

This project delivers:

- Full-stack real-time monitoring
- Event ingestion API
- Metrics computation engine
- WebSocket streaming architecture
- System health monitoring
- Dockerized production deployment
- Scalable architectural foundation

It goes beyond basic CRUD implementation and demonstrates:

- Systems thinking
- Real-time data engineering
- MLOps awareness
- Deployment readiness
- Scalability planning

