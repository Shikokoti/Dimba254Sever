from flask import Blueprint, jsonify
from models import Player, Team
from extensions import db

players_bp = Blueprint("players", __name__)

# --- List all players ---
@players_bp.route("/", methods=["GET"])
def list_players():
    players = Player.query.all()
    return jsonify([player.to_dict() for player in players]), 200

# --- Add a team to a player ---
@players_bp.route("/<int:player_id>/add-team/<int:team_id>", methods=["POST"])
def add_team_to_player(player_id, team_id):
    player = Player.query.get_or_404(player_id)
    team = Team.query.get_or_404(team_id)

    if team not in player.teams:
        player.teams.append(team)
        db.session.commit()

    return jsonify(player.to_dict()), 200

# --- Remove a team from a player ---
@players_bp.route("/<int:player_id>/remove-team/<int:team_id>", methods=["DELETE"])
def remove_team_from_player(player_id, team_id):
    player = Player.query.get_or_404(player_id)
    team = Team.query.get_or_404(team_id)

    if team in player.teams:
        player.teams.remove(team)
        db.session.commit()

    return jsonify({"message": "Team removed from player"}), 200