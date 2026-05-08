import os
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, val = line.partition('=')
                os.environ.setdefault(key.strip(), val.strip())

from app import create_app
from extensions import db
from models import Team

LOGO_MAP = {
    'gor mahia':           '/teams/GorMahia.png',
    'afc leopards':        '/teams/afcLeopards.png',
    'aps bomet':           '/teams/apsbomet.jpeg',
    'bandari':             '/teams/bandari.png',
    'bidco united':        '/teams/bidcounited.png',
    'kakamega homeboyz':   '/teams/kakamegahomeboyz.png',
    'kariobängi sharks':   '/teams/kariobangisharks.png',
    'kariobangi sharks':   '/teams/kariobangisharks.png',
    'kcb':                 '/teams/kcb.png',
    'kenya police':        '/teams/kenyapolice.png',
    'mara sugar':          '/teams/marasugar.jpeg',
    'mathare united':      '/teams/mathareunited.png',
    "murang'a seal":       '/teams/murangaseal.png',
    'muranga seal':        '/teams/murangaseal.png',
    'nairobi united':      '/teams/nairobiunited.jpg',
    'posta rangers':       '/teams/postarangers.png',
    'shabana':             '/teams/shabana.jpeg',
    'sofapaka':            '/teams/sofapaka.png',
    'tusker':              '/teams/tusker.png',
    'ulinzi stars':        '/teams/ulinzistars.png',
}

app = create_app()

with app.app_context():
    teams = Team.query.all()
    updated = 0

    for team in teams:
        key = team.name.lower().strip()
        logo = LOGO_MAP.get(key)

        if not logo:
            for map_name, map_logo in LOGO_MAP.items():
                if map_name in key or key in map_name:
                    logo = map_logo
                    break

        if logo:
            team.logo_url = logo
            updated += 1
            print(f"  ✓  {team.name} → {logo}")
        else:
            print(f"  ✗  {team.name} — no match found")

    db.session.commit()
    print(f"\nDone. {updated}/{len(teams)} teams updated.")
