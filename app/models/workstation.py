from app.extensions import db

class Workstation(db.Model):
    __tablename__ = "workstations"

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    events = db.relationship("Event", backref="workstation", lazy=True)
