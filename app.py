from flask import Flask

#create a Flask application Instance

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)