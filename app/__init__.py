from flask import Flask
from .config import Config
from .extensions import db, migrate
from app.views.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from app.api.events import events_bp
    from app.views.dashboard import dashboard_bp

    app.register_blueprint(events_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp)
    

    return app
