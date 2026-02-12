from flask import Blueprint, request, jsonify
from models import Coach
from extensions import db

coaches_bp = Blueprint("coaches", __name__)

@coaches_bp.route("/", methods=["POST"])
def create_coach():
    data = request.get_json()

    coach = Coach(
        name=data.get("name"),
        experience_years=data.get("experience_years", 0),
        team_id=data.get("team_id")
    )

    db.session.add(coach)
    db.session.commit()

    return jsonify(coach.to_dict()), 201


@coaches_bp.route("/", methods=["GET"])
def get_coaches():
    coaches = Coach.query.all()
    return jsonify([coach.to_dict() for coach in coaches])