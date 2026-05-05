# Dimba254 API

A RESTful backend API for a sports management application built with Flask and PostgreSQL. Manages teams, players, and coaches with JWT-based authentication.

## Tech Stack

- **Python / Flask** — web framework
- **PostgreSQL** — database
- **Flask-SQLAlchemy** — ORM
- **Flask-Migrate** — database migrations
- **Flask-JWT-Extended** — authentication
- **Werkzeug** — password hashing

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shikokoti/Dimba254Sever.git
   cd Dimba254Sever
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Fill in your values in `.env`.

4. Run database migrations:
   ```bash
   flask db upgrade
   ```

5. Start the server:
   ```bash
   python run.py
   ```

The API will be running at `http://127.0.0.1:5000`.

---

## Authentication

All endpoints except `/auth/register` and `/auth/login` require a JWT token.

Include the token in the request header:
```
Authorization: Bearer <access_token>
```

### Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive a JWT token |

**Register body:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

**Login body:**
```json
{
  "username": "john",
  "password": "secret123"
}
```

---

## Endpoints

### Teams

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/teams/` | List all teams |
| GET | `/teams/<id>` | Get a single team |
| POST | `/teams/` | Create a team |
| PUT | `/teams/<id>` | Update a team |
| DELETE | `/teams/<id>` | Delete a team |
| POST | `/teams/<id>/add-player/<player_id>` | Add a player to a team |
| DELETE | `/teams/<id>/remove-player/<player_id>` | Remove a player from a team |
| POST | `/teams/<id>/set-coach/<coach_id>` | Assign a coach to a team |

**Create/Update team body:**
```json
{
  "name": "Gor Mahia",
  "league_position": 1,
  "founded_year": 1968,
  "stadium": "Nyayo Stadium"
}
```

---

### Players

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/players/` | List all players |
| GET | `/players/<id>` | Get a single player |
| POST | `/players/` | Create a player |
| PUT | `/players/<id>` | Update a player |
| DELETE | `/players/<id>` | Delete a player |
| POST | `/players/<id>/add-team/<team_id>` | Add a player to a team |
| DELETE | `/players/<id>/remove-team/<team_id>` | Remove a player from a team |

**Create/Update player body:**
```json
{
  "name": "John Otieno",
  "position": "Forward",
  "goals_scored": 12
}
```

---

### Coaches

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/coaches/` | List all coaches |
| GET | `/coaches/<id>` | Get a single coach |
| POST | `/coaches/` | Create a coach |
| PUT | `/coaches/<id>` | Update a coach |
| DELETE | `/coaches/<id>` | Delete a coach |
| POST | `/coaches/<id>/set-team/<team_id>` | Assign a coach to a team |
| POST | `/coaches/<id>/remove-team` | Remove a coach from their team |

**Create/Update coach body:**
```json
{
  "name": "Samuel Onyango",
  "experience_years": 10
}
```
