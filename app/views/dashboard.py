from flask import Blueprint, render_template, request
from app.services.metrics import (
    compute_worker_metrics,
    compute_station_metrics,
    compute_factory_metrics
)

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/")
def dashboard():
    worker_filter = request.args.get("worker")
    station_filter = request.args.get("station")

    workers = compute_worker_metrics()
    stations = compute_station_metrics()
    factory = compute_factory_metrics(workers)

    if worker_filter:
        workers = [w for w in workers if w["worker_id"] == worker_filter]

    if station_filter:
        stations = [s for s in stations if s["station_id"] == station_filter]

    return render_template(
        "dashboard.html",
        workers=workers,
        stations=stations,
        factory=factory
    )
