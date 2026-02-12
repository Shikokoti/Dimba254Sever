from flask import Blueprint
from models import Team, Player, Coach
from extensions import db

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/<int:team_id>/add-player/<int:player_id>", methods=["POST"])
def add_player_to_team(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    if player not in team.players:
        team.players.append(player)
        db.session.commit()

    return jsonify(team.to_dict()), 200


@teams_bp.route("/<int:team_id>/remove-player/<int:player_id>", methods=["DELETE"])
def remove_player_from_team(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    if player in team.players:
        team.players.remove(player)
        db.session.commit()

    return jsonify({"message": "Player removed from team"}), 200

@teams_bp.route("/<int:team_id>/set-coach/<int:coach_id>", methods=["POST"])
def set_coach_for_team(team_id, coach_id):
    team = Team.query.get_or_404(team_id)
    coach = Coach.query.get_or_404(coach_id)

    coach.team = team
    db.session.commit()

    return jsonify(team.to_dict()), 200