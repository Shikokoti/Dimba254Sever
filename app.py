from flask import Flask
from extensions import db
from routes.teams import teams_bp
from routes.players import players_bp
from routes.coaches import coaches_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dimba.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(players_bp, url_prefix="/players")
    app.register_blueprint(coaches_bp, url_prefix="/coaches")

    return app