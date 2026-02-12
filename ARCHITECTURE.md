# System Architecture

## Overview

The AI-Powered Worker Productivity Dashboard is a real-time monitoring system designed using an event-driven architecture with WebSocket streaming.

The system ingests AI-generated events, stores them in a database, computes metrics, and streams live updates to a dashboard.

---

## High-Level Architecture

AI Cameras → Flask API → Database → Metrics Engine → WebSocket Server → Dashboard UI

---

## Logical Components

### 1. Edge Layer (AI Cameras)

- Generates structured JSON events.
- Can buffer events during connectivity loss.
- Sends data to backend over HTTP.

### 2. API Layer (Flask)

- Validates incoming events.
- Deduplicates.
- Stores in database.
- Exposes metrics APIs.

### 3. Data Layer

- SQLite (development)
- PostgreSQL (production recommended)

### 4. Metrics Engine

- Reads event history.
- Computes durations.
- Aggregates per worker, station, factory.

### 5. Streaming Layer

- Flask-SocketIO + Eventlet.
- Push-based real-time updates.

### 6. Presentation Layer

- Jinja templates.
- Tailwind CSS.
- WebSocket client.

---

## Data Flow

1. Camera sends event.
2. Backend validates and stores.
3. Simulator/background thread adds additional events.
4. Metrics engine recalculates.
5. WebSocket broadcasts update.
6. Browser updates UI.

---

## Design Principles

- Loose coupling.
- Idempotent ingestion.
- Deterministic metrics.
- Horizontal scalability.
- Security extensibility.

---

## Technology Stack

- Python
- Flask
- Flask-SocketIO
- SQLAlchemy
- Eventlet
- Tailwind CSS
- Gunicorn
- Docker

---

## Non-Functional Goals

- Low latency
- High availability
- Fault tolerant
- Modular
- Observable

---

## Fault Tolerance

- Duplicate-safe ingestion.
- Out-of-order tolerant.
- Graceful WebSocket reconnection.
- Restartable containers.

---

## Future Extensions

- Redis pub/sub
- Kafka ingestion
- Microservices split
- Kubernetes deployment
