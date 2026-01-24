from flask import Flask, request, send_from_directory, jsonify
from models import db, Player, Team, Coach

#create a Flask application Instance

app = Flask(__name__)

#set up db resources 
app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dimba.db"
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  #Setup a pin on the map
db.init_app(app) #Initialize the db with the flask app instance

with app.app_context():
    db.create_all()  #Create the database tables

@app.route('/') 
def index():
    return "Welcome to DIMBA254 Server"




#adding views from other modules
#KPL TEAMS page
@app.route ('/teams')
def teams ():
    return "2025/2026 Teams in the Kenyan Premier League"

#About Us page
@app.route ('/about')
def about():
    return "Get to know more about DIMBA254."

#contact Us page
@app.route ('/contact')
def contact ():
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

@app.route("/Players", methods=['GET'])
def get_players():
    players = Player.query.all()
    players_data = [player.to_dict() for player in players]
    return jsonify([player.to_dict() for player in players])

# @app.route("/players/bulk", methods=['POST'])
# def create_players_bulk():
#     data = request.get_json()
#     players_data = data.get("players", [])
#     players = []
#     for player_data in players_data:
#         player = Player(
#             name=player_data.get("name"),
#             position=player_data.get("position"),
#             goals_scored=player_data.get("goals_scored", 0)
#         )
#         db.session.add(player)
#         players.append(player)
#     db.session.commit()
#     return jsonify([player.to_dict() for player in players]), 201

@app.route("/stats/<KPL_STATS>")
def stats_view(KPL_STATS):
    return f"Statistics of the Kenyan Premier League:, is available here. fot this  team {KPL_STATS}"

@app.route ("/stats")
def stats ():
    return "Statistics of the Kenyan Premier League"



#Aselect team undet the teams view teams/afc leopards
@app.route('/teams/<team_name>')
def team_detail(team_name):
    return f"Details about the team: {team_name}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)