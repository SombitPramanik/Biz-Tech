from app.extensions import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    worker_id = db.Column(
        db.Integer, db.ForeignKey("workers.id"), nullable=False
    )

    workstation_id = db.Column(
        db.Integer, db.ForeignKey("workstations.id"), nullable=False
    )

    event_type = db.Column(db.String(30), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, default=0)
