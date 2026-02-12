from flask import Blueprint, jsonify, request
from models import Team, Player, Coach
from extensions import db

teams_bp = Blueprint("teams", __name__)

# --- List all teams ---
@teams_bp.route("/", methods=["GET"])
def list_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200

# --- Add player to a team ---
@teams_bp.route("/<int:team_id>/add-player/<int:player_id>", methods=["POST"])
def add_player_to_team(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    if player not in team.players:
        team.players.append(player)
        db.session.commit()

    return jsonify(team.to_dict()), 200

# --- Remove player from a team ---
@teams_bp.route("/<int:team_id>/remove-player/<int:player_id>", methods=["DELETE"])
def remove_player_from_team(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    if player in team.players:
        team.players.remove(player)
        db.session.commit()

    return jsonify({"message": "Player removed from team"}), 200

# --- Set coach for a team ---
@teams_bp.route("/<int:team_id>/set-coach/<int:coach_id>", methods=["POST"])
def set_coach_for_team(team_id, coach_id):
    team = Team.query.get_or_404(team_id)
    coach = Coach.query.get_or_404(coach_id)

    coach.team = team
    db.session.commit()

    return jsonify(team.to_dict()), 200

@teams_bp.route("/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    data = request.get_json()  # now this will work

    if "name" in data:
        team.name = data["name"]
    if "league_position" in data:
        team.league_position = data["league_position"]
    if "founded_year" in data:
        team.founded_year = data["founded_year"]
    if "stadium" in data:
        team.stadium = data["stadium"]

    db.session.commit()

    return jsonify(team.to_dict()), 200