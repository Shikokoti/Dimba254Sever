from flask import Blueprint, request, jsonify
from models import Coach, Team
from extensions import db

coaches_bp = Blueprint("coaches", __name__)

# --- List all coaches ---
@coaches_bp.route("/", methods=["GET"])
def list_coaches():
    coaches = Coach.query.all()
    return jsonify([coach.to_dict() for coach in coaches]), 200

# --- Create a new coach ---
@coaches_bp.route("/", methods=["POST"])
def create_coach():
    data = request.get_json()

    coach = Coach(
        name=data.get("name"),
        experience_years=data.get("experience_years", 0),
        team_id=data.get("team_id")  # optional: assign to a team on creation
    )

    db.session.add(coach)
    db.session.commit()

    return jsonify(coach.to_dict()), 201

# --- Assign coach to a team ---
@coaches_bp.route("/<int:coach_id>/set-team/<int:team_id>", methods=["POST"])
def set_team_for_coach(coach_id, team_id):
    coach = Coach.query.get_or_404(coach_id)
    team = Team.query.get_or_404(team_id)

    coach.team = team
    db.session.commit()

    return jsonify(coach.to_dict()), 200

# --- Remove coach from a team ---
@coaches_bp.route("/<int:coach_id>/remove-team", methods=["POST"])
def remove_team_from_coach(coach_id):
    coach = Coach.query.get_or_404(coach_id)
    coach.team = None
    db.session.commit()

    return jsonify({"message": "Coach removed from team"}), 200

@coaches_bp.route("/<int:coach_id>", methods=["PUT"])
def update_coach(coach_id):
    coach = Coach.query.get_or_404(coach_id)
    data = request.get_json()

    if "name" in data:
        coach.name = data["name"]
    if "experience_years" in data:
        coach.experience_years = data["experience_years"]

    db.session.commit()

    return jsonify(coach.to_dict()), 200