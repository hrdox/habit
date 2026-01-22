from app import app, db
from models import User

with app.app_context():
    users = User.query.filter(User.local_ip.isnot(None)).all()
    print(f"Users with local_ip: {len(users)}")
    for u in users:
        print(f"{u.username}: {u.local_ip}")
