from flask import Flask
from .config import Config
from .extensions import db, migrate
import logging
from app.extensions import db, migrate, socketio

logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from . import models

    from app.api.events import events_bp
    from app.views.dashboard import dashboard_bp
    from app.api.metrics import metrics_bp    
    from app.api.health import health_bp
    from app.services.simulator import start_simulator
    from app.services.live_stream import stream_loop

    app.register_blueprint(events_bp, url_prefix="/api")
    app.register_blueprint(metrics_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(health_bp)
    start_simulator(app)
    socketio.start_background_task(stream_loop)


    return app
