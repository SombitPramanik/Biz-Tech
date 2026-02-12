from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Worker, Workstation, Event
from datetime import datetime, timedelta
import random

events_bp = Blueprint("events_bp", __name__)


@events_bp.route("/seed", methods=["POST"])
def seed_data():
    db.session.query(Event).delete()
    db.session.query(Worker).delete()
    db.session.query(Workstation).delete()

    workers = []
    for i in range(1, 7):
        w = Worker(worker_id=f"W{i}", name=f"Worker {i}")
        db.session.add(w)
        workers.append(w)

    stations = []
    for i in range(1, 7):
        s = Workstation(station_id=f"S{i}", name=f"Station {i}")
        db.session.add(s)
        stations.append(s)

    db.session.commit()

    start = datetime.utcnow() - timedelta(hours=8)

    for _ in range(500):
        ev = Event(
            timestamp=start + timedelta(minutes=random.randint(0, 480)),
            worker_id=random.choice(workers).id,
            workstation_id=random.choice(stations).id,
            event_type=random.choice(["working", "idle", "product_count"]),
            confidence=round(random.uniform(0.85, 0.99), 2),
            count=random.randint(1, 5),
        )
        db.session.add(ev)

    db.session.commit()

    return jsonify({"message": "Database seeded successfully"})
