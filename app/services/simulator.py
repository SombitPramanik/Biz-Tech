import random
import threading
import time
from datetime import datetime
from app.extensions import db
from app.models import Worker, Workstation, Event


EVENT_TYPES = ["working", "idle", "product_count"]


def generate_event():
    workers = Worker.query.all()
    stations = Workstation.query.all()

    if not workers or not stations:
        return

    worker = random.choice(workers)
    station = random.choice(stations)

    event_type = random.choice(EVENT_TYPES)

    event = Event(
        timestamp=datetime.utcnow(),
        worker_id=worker.id,
        workstation_id=station.id,
        event_type=event_type,
        confidence=round(random.uniform(0.85, 0.99), 2),
        count=random.randint(1, 5) if event_type == "product_count" else 0
    )

    db.session.add(event)
    db.session.commit()


def simulator_loop(app):
    with app.app_context():
        while True:
            generate_event()
            time.sleep(5)   # simulate live camera feed every 5s


def start_simulator(app):
    thread = threading.Thread(target=simulator_loop, args=(app,), daemon=True)
    thread.start()
