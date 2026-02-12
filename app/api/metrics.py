from flask import Blueprint, jsonify
from app.services.metrics import (
    compute_worker_metrics,
    compute_station_metrics,
    compute_factory_metrics
)

metrics_bp = Blueprint("metrics_bp", __name__)

@metrics_bp.route("/metrics/workers")
def worker_metrics():
    return jsonify(compute_worker_metrics())

@metrics_bp.route("/metrics/stations")
def station_metrics():
    return jsonify(compute_station_metrics())

@metrics_bp.route("/metrics/factory")
def factory_metrics():
    workers = compute_worker_metrics()
    return jsonify(compute_factory_metrics(workers))
