import os
import sys

# Load .env manually
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, val = line.partition('=')
                os.environ.setdefault(key.strip(), val.strip())

import psycopg2
from urllib.parse import urlparse

url = urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(
    host=url.hostname,
    port=url.port or 5432,
    dbname=url.path.lstrip('/'),
    user=url.username,
    password=url.password,
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name='team' AND column_name='logo_url'
""")
if cur.fetchone():
    print("Column already exists — nothing to do.")
else:
    cur.execute("ALTER TABLE team ADD COLUMN logo_url VARCHAR(500)")
    print("logo_url column added successfully.")

cur.close()
conn.close()
