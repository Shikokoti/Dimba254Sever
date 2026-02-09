from flask_sqlalchemy import SQLAlchemy
#called my db and initialized it
db = SQLAlchemy()

#Creating a model for the players in the KPL

player_team = db.Table(
    'player_team',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    goals_scored = db.Column(db.Integer, default=0)

    teams = db.relationship(
        "Team",
        secondary=player_team,
        back_populates="players"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "goals_scored": self.goals_scored,
            "teams": [team.name for team in self.teams]
            
        }
    


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    league_position = db.Column(db.Integer, nullable=False)
    founded_year = db.Column(db.Integer, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)

    players = db.relationship(
        "Player",
        secondary=player_team,
        back_populates="teams"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "league_position": self.league_position,
            "founded_year": self.founded_year,
            "stadium": self.stadium,
            "players": [player.name for player in self.players]
        }

    coach = db.relationship("Coach", back_populates="team", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "league_position": self.league_position,
            "founded_year": self.founded_year,
            "stadium": self.stadium,
            "players": [player.name for player in self.players],
            "coach": self.coach.name if self.coach else None
        }


#Creating a model for the coaches in the KPL
class Coach(db.Model):
    __tablename__ = "coach"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, default=0)

    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    team = db.relationship("Team", back_populates="coach")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "experience_years": self.experience_years,
            "team": self.team.name if self.team else None
        }