import time
import psutil
from app.extensions import socketio
from app.services.metrics import compute_worker_metrics, compute_factory_metrics


def stream_loop():
    while True:
        try:
            workers = compute_worker_metrics()
            factory = compute_factory_metrics(workers)

            payload = {
                "factory": factory,
                "workers": workers,
                "health": {
                    "cpu": round(psutil.cpu_percent(), 1),
                    "ram": round(psutil.virtual_memory().percent, 1),
                },
            }

            socketio.emit("live_update", payload)
        except Exception as e:
            print(f"Stream error: {e}")

        time.sleep(5)
