import os, re, unicodedata

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

def slugify(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    return name

url = urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(
    host=url.hostname, port=url.port or 5432,
    dbname=url.path.lstrip('/'), user=url.username, password=url.password,
)
conn.autocommit = True
cur = conn.cursor()

# Add column if missing
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name='team' AND column_name='slug'
""")
if not cur.fetchone():
    cur.execute("ALTER TABLE team ADD COLUMN slug VARCHAR(120) UNIQUE")
    print("slug column added.")
else:
    print("slug column already exists.")

# Populate slugs for existing teams
cur.execute("SELECT id, name FROM team ORDER BY id")
teams = cur.fetchall()
used_slugs = set()
for team_id, name in teams:
    base = slugify(name)
    slug = base
    count = 2
    while slug in used_slugs:
        slug = f"{base}-{count}"
        count += 1
    used_slugs.add(slug)
    cur.execute("UPDATE team SET slug = %s WHERE id = %s", (slug, team_id))
    print(f"  {name} → {slug}")

print(f"\nDone. {len(teams)} teams updated.")
cur.close()
conn.close()
