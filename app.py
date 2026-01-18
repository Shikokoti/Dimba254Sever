from flask import Flask
from models import db, Player, Team, Coach

#create a Flask application Instance

app = Flask(__name__)

#set up db resources 
app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dimba254.db"
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  #Setup a pin on the map
db.init_app(app)

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

@app.route("/players")
def players():
    return f"List of players in the Kenyan Premier League"

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