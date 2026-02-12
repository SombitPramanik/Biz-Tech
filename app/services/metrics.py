from collections import defaultdict
from datetime import datetime
from app.models import Event, Worker, Workstation
from app.extensions import db


def compute_worker_metrics():
    results = []

    workers = Worker.query.all()

    for worker in workers:
        events = (
            Event.query
            .filter_by(worker_id=worker.id)
            .order_by(Event.timestamp)
            .all()
        )

        active = 0
        idle = 0
        units = 0

        for i in range(len(events)):
            current = events[i]
            next_time = (
                events[i + 1].timestamp
                if i + 1 < len(events)
                else datetime.utcnow()
            )

            duration = (next_time - current.timestamp).total_seconds()

            if current.event_type == "working":
                active += duration

            if current.event_type == "idle":
                idle += duration

            if current.event_type == "product_count":
                units += current.count

        total_time = active + idle

        utilization = (
            round((active / total_time) * 100, 2)
            if total_time > 0 else 0
        )

        uph = (
            round(units / (active / 3600), 2)
            if active > 0 else 0
        )

        results.append({
            "worker_id": worker.worker_id,
            "name": worker.name,
            "active_hours": round(active / 3600, 2),
            "idle_hours": round(idle / 3600, 2),
            "utilization": utilization,
            "units": units,
            "uph": uph
        })

    return results


def compute_station_metrics():
    results = []

    stations = Workstation.query.all()

    for station in stations:
        events = (
            Event.query
            .filter_by(workstation_id=station.id)
            .order_by(Event.timestamp)
            .all()
        )

        occupied = 0
        units = 0

        for i in range(len(events)):
            current = events[i]
            next_time = (
                events[i + 1].timestamp
                if i + 1 < len(events)
                else datetime.utcnow()
            )

            duration = (next_time - current.timestamp).total_seconds()

            if current.event_type == "working":
                occupied += duration

            if current.event_type == "product_count":
                units += current.count

        utilization = (
            round((occupied / (8 * 3600)) * 100, 2)
        )

        throughput = (
            round(units / (occupied / 3600), 2)
            if occupied > 0 else 0
        )

        results.append({
            "station_id": station.station_id,
            "name": station.name,
            "occupied_hours": round(occupied / 3600, 2),
            "utilization": utilization,
            "units": units,
            "throughput": throughput
        })

    return results


def compute_factory_metrics(worker_metrics):
    total_active = sum(w["active_hours"] for w in worker_metrics)
    total_units = sum(w["units"] for w in worker_metrics)

    avg_util = (
        round(
            sum(w["utilization"] for w in worker_metrics) /
            len(worker_metrics),
            2
        )
        if worker_metrics else 0
    )

    avg_rate = (
        round(total_units / total_active, 2)
        if total_active > 0 else 0
    )

    return {
        "total_active_hours": round(total_active, 2),
        "total_units": total_units,
        "avg_utilization": avg_util,
        "avg_rate": avg_rate
    }
