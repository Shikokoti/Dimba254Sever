from flask import Flask

#create a Flask application Instance

app = Flask(__name__)


@app.route('/') 
def index():
    return "Welcome to DIMBA254 Server"


if __name__ == '__main__':
    app.run(port=5000, debug=True)