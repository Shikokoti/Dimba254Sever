from flask_sqlalchemy import SQLAlchemy
#called my db and initialized it
db = SQLAlchemy()

#Creating a model for the players in the KPL
class Player (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String(100), nullable = False)
    team = db.Column (db.String(100), nullable = False)
    position = db.Column (db.String(50), nullable = False)
    goals_scored = db.Column (db.Integer, default = 0)
    signings = db.relationship ( 'Player', back_populates='Team', back_populates = "Coach", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Player {self.name} - Team: {self.team} - Position: {self.position} - Goals Scored: {self.goals_scored}>"
    
    class Team (db.Model):
        id = db.Column (db.Integer, primary_key = True)
        name = db.Column (db.String(100), nullable = False)
        team_position = db.Column (db.String(50), nullable = False)
        founded_year = db.Column (db.Integer, nullable = False)
        stadium = db.Column (db.String(100), nullable = False)
        signings = db.relationship ( 'Player', back_populates='Team', back_populates = "Coach", cascade="all, delete-orphan")


        

        def __repr__(self):
            return f"<Team {self.name} - Founded: {self.founded_year} - Stadium: {self.stadium} - Position: {self.team_position}>"
        
#Creating a model for the coaches in the KPL
class Coach (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String(100), nullable = False)
    team_id = db.Column (db.String(100), db.ForeignKey('team.id'), nullable = False)
    experience_years = db.Column (db.Integer, default = 0)
    signings = db.relationship ( 'Player', back_populates='Team', back_populates = "Coach", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Coach {self.name} - Team: {self.team_id} - Experience: {self.experience_years} years>"