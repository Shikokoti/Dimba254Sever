from dotenv import load_dotenv
load_dotenv()

from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        result = db.session.execute(text("SELECT id, name, logo_url FROM team LIMIT 1"))
        print("logo_url column EXISTS — migration was applied")
        for row in result:
            print(f"  sample row: {dict(row._mapping)}")
    except Exception as e:
        print(f"ERROR: {e}")
