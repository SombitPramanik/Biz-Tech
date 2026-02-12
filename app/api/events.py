from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Worker, Workstation, Event
from datetime import datetime, timedelta
import random

from flask import request
import hashlib
from dateutil import parser


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


@events_bp.route("/events", methods=["POST"])
def ingest_event():
    data = request.get_json()

    required = ["timestamp", "worker_id", "workstation_id", "event_type", "confidence"]

    for field in required:
        if field not in data:
            return {"error": f"{field} is required"}, 400

    worker = Worker.query.filter_by(worker_id=data["worker_id"]).first()
    station = Workstation.query.filter_by(station_id=data["workstation_id"]).first()

    if not worker or not station:
        return {"error": "Invalid worker or workstation"}, 400

    ts = parser.isoparse(data["timestamp"])

    raw = f'{data["timestamp"]}{data["worker_id"]}{data["workstation_id"]}{data["event_type"]}{data.get("count",0)}'
    event_hash = hashlib.sha256(raw.encode()).hexdigest()

    if Event.query.filter_by(event_hash=event_hash).first():
        return {"message": "Duplicate ignored"}, 200

    event = Event(
        timestamp=ts,
        worker_id=worker.id,
        workstation_id=station.id,
        event_type=data["event_type"],
        confidence=float(data["confidence"]),
        count=int(data.get("count", 0)),
        event_hash=event_hash,
    )

    db.session.add(event)
    db.session.commit()

    return {"message": "Event stored"}, 201
