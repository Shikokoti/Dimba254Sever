from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import Team, Player, Coach, slugify
from extensions import db

teams_bp = Blueprint("teams", __name__)


# --- List all teams ---
@teams_bp.route("/", methods=["GET"])
@jwt_required()
def list_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200

# --- Create a new team ---
@teams_bp.route("/", methods=["POST"])
@jwt_required()
def create_team():
    data = request.get_json()
    name = data.get("name")
    team = Team(
        name=name,
        slug=slugify(name) if name else None,
        league_position=data.get("league_position"),
        founded_year=data.get("founded_year"),
        stadium=data.get("stadium"),
        logo_url=data.get("logo_url"),
    )
    db.session.add(team)
    db.session.commit()
    return jsonify(team.to_dict()), 201

# --- Get a single team by ID ---
@teams_bp.route("/<int:team_id>", methods=["GET"])
@jwt_required()
def get_team(team_id):
    team = Team.query.get_or_404(team_id)
    return jsonify(team.to_full_dict()), 200

# --- Get a single team by slug ---
@teams_bp.route("/slug/<string:slug>", methods=["GET"])
@jwt_required()
def get_team_by_slug(slug):
    team = Team.query.filter_by(slug=slug).first_or_404()
    return jsonify(team.to_full_dict()), 200

# --- Add player to a team ---
@teams_bp.route("/<int:team_id>/add-player/<int:player_id>", methods=["POST"])
@jwt_required()
def add_player_to_team(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    if player not in team.players:
        team.players.append(player)
        db.session.commit()

    return jsonify(team.to_dict()), 200

# --- Remove player from a team ---
@teams_bp.route("/<int:team_id>/remove-player/<int:player_id>", methods=["DELETE"])
@jwt_required()
def remove_player_from_team(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    if player in team.players:
        team.players.remove(player)
        db.session.commit()

    return jsonify({"message": "Player removed from team"}), 200

# --- Set coach for a team ---
@teams_bp.route("/<int:team_id>/set-coach/<int:coach_id>", methods=["POST"])
@jwt_required()
def set_coach_for_team(team_id, coach_id):
    team = Team.query.get_or_404(team_id)
    coach = Coach.query.get_or_404(coach_id)

    coach.team = team
    db.session.commit()

    return jsonify(team.to_dict()), 200

# --- Delete a team ---
@teams_bp.route("/<int:team_id>", methods=["DELETE"])
@jwt_required()
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({"message": "Team deleted"}), 200

# --- Update a team ---
@teams_bp.route("/<int:team_id>", methods=["PUT"])
@jwt_required()
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    data = request.get_json()

    if "name" in data:
        team.name = data["name"]
        team.slug = slugify(data["name"])
    if "league_position" in data:
        team.league_position = data["league_position"]
    if "founded_year" in data:
        team.founded_year = data["founded_year"]
    if "stadium" in data:
        team.stadium = data["stadium"]
    if "logo_url" in data:
        team.logo_url = data["logo_url"]

    db.session.commit()

    return jsonify(team.to_dict()), 200
