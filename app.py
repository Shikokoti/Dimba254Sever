from flask import Flask
from flask_migrate import Migrate
import os
from extensions import db
from routes.teams import teams_bp
from routes.players import players_bp
from routes.coaches import coaches_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    Migrate(app, db)

    @app.route("/")
    def home():
        return "DIMBA254 API is running 🚀"

    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(players_bp, url_prefix="/players")
    app.register_blueprint(coaches_bp, url_prefix="/coaches")

    return app