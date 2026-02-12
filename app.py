from datetime import date
from flask import Flask, request, send_from_directory, jsonify
from models import db, Player, Team, Coach

#create a Flask application Instance

app = Flask(__name__)

#set up db resources 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dimba.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app) #Initialize the db with the flask app instance

with app.app_context():
    db.create_all()  #Create the database tables

@app.route('/') 
def index():
    return "Welcome to DIMBA254 Server"




#adding views from other modules
#KPL TEAMS page
@app.route('/teams', methods=['POST'])
def create_teams():
    data = request.get_json()
    if not data:
     return jsonify({"error": "Invalid JSON"}), 400
    name = data.get("name")
    league_position = data.get("league_position")
    founded_year = data.get("founded_year")
    stadium = data.get("stadium")
    team = Team(name=name, league_position=league_position, founded_year=founded_year, stadium=stadium)
    db.session.add(team)
    db.session.commit()
    return jsonify(team.to_dict()), 201

@app.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200

#About Us page
@app.route('/about')
def about():
    return "Get to know more about DIMBA254."

@app.route('/contact')
def contact():
    return "Reach out to DIMBA254 for any inquiries."

@app.route("/contact/<data>")
def contact_form(data):
 
    return f"Contact form submitted with data: {data}"


@app.route("/players/<player_name>")
def player_list(player_name):
    return f"This Player plays for the Kenyan Premier League: {player_name}"

@app.route("/players", methods=['POST'])
def create_player():
    data = request.get_json()
    name = data.get("name")
    position = data.get("position")
    goals_scored = data.get("goals_scored", 0)
    player = Player(name=name, position=position, goals_scored=goals_scored)

    db.session.add(player)
    db.session.commit()

    return jsonify(player.to_dict()), 201 

@app.route("/players", methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([player.to_dict() for player in players])



@app.route("/stats/<KPL_STATS>")
def stats_view(KPL_STATS):
    return f"Statistics of the Kenyan Premier League:, is available here. fot this  team {KPL_STATS}"

@app.route("/stats")
def stats():
    return "Statistics of the Kenyan Premier League"



#Aselect team undet the teams view teams/afc leopards
@app.route('/teams/<team_name>')
def team_detail(team_name):
    return f"Details about the team: {team_name}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)