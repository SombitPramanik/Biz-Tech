# Scalability Strategy

---

## Vertical Scaling

- Increase CPU/RAM
- Increase Gunicorn workers

---

## Horizontal Scaling

- Multiple web containers
- Load balancer

---

## Data Layer Scaling

- SQLite → PostgreSQL
- Read replicas
- Partition by site

---

## Streaming Scaling

- Redis Pub/Sub backend for SocketIO
- Message broker fan-out

---

## Ingestion Scaling

- Kafka / RabbitMQ
- Async consumers

---

## Multi-Site Architecture

- Add site_id column
- Route events per site
- Separate dashboards

---

## Expected Capacity

Small:
10 cameras

Medium:
500 cameras

Large:
10k+ cameras with message queue

---

## Bottleneck Mitigation

- Caching
- Batch inserts
- Pre-aggregations
- Background jobs

---

## High Availability

- Multiple containers
- Health checks
- Auto-restart
- Rolling updates

---

## Disaster Recovery

- Database backups
- Snapshot volumes
- Infrastructure as code

---

## Security at Scale

- OAuth/JWT
- mTLS
- IP allowlist
- Secrets manager
