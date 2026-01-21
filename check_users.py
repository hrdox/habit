from app import app, db, User
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"Username: {u.username}, Role: {u.role}")
