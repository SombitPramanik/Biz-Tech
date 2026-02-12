from flask import Blueprint, jsonify
import psutil

health_bp = Blueprint("health_bp", __name__)

@health_bp.route("/health")
def health():

    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()

    return jsonify({
        "status": "ok",
        "cpu_usage": cpu,
        "ram_usage_percent": memory.percent,
        "ram_used_mb": round(memory.used / (1024**2), 2),
        "ram_total_mb": round(memory.total / (1024**2), 2)
    })
