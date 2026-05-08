import re
import unicodedata
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


def slugify(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    return name


# -------------------------
# User Model
# -------------------------
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}

# Association Table (Many-to-Many)
player_team = db.Table(
    "player_team",
    db.Column("player_id", db.Integer, db.ForeignKey("player.id")),
    db.Column("team_id", db.Integer, db.ForeignKey("team.id")),
)


# -------------------------
# Player Model
# -------------------------
class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    goals_scored = db.Column(db.Integer, default=0)

    teams = db.relationship(
        "Team",
        secondary=player_team,
        back_populates="players",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "goals_scored": self.goals_scored,
            "teams": [team.name for team in self.teams],
        }


# -------------------------
# Team Model
# -------------------------
class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=True)
    league_position = db.Column(db.Integer, nullable=False)
    founded_year = db.Column(db.Integer, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(500), nullable=True)

    players = db.relationship(
        "Player",
        secondary=player_team,
        back_populates="teams",
    )

    coach = db.relationship(
        "Coach",
        back_populates="team",
        uselist=False,
        cascade="all, delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "league_position": self.league_position,
            "founded_year": self.founded_year,
            "stadium": self.stadium,
            "logo_url": self.logo_url,
            "players": [player.name for player in self.players],
            "coach": self.coach.name if self.coach else None,
        }

    def to_full_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "league_position": self.league_position,
            "founded_year": self.founded_year,
            "stadium": self.stadium,
            "logo_url": self.logo_url,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "position": p.position,
                    "goals_scored": p.goals_scored,
                }
                for p in self.players
            ],
            "coach": {
                "name": self.coach.name,
                "experience_years": self.coach.experience_years,
            } if self.coach else None,
        }


# -------------------------
# Coach Model
# -------------------------
class Coach(db.Model):
    __tablename__ = "coach"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, default=0)

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("team.id"),
        nullable=True,
        unique=True  # ensures one-to-one
    )

    team = db.relationship("Team", back_populates="coach")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "experience_years": self.experience_years,
            "team": self.team.name if self.team else None,
        }