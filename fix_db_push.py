from app import app, db
from models import PushSubscription
from sqlalchemy import text

with app.app_context():
    print("Creating PushSubscription table...")
    try:
        # Create table directly using SQLAlchemy metadata
        PushSubscription.__table__.create(db.engine)
        print("PushSubscription table created successfully.")
    except Exception as e:
        print(f"Error creating table (might already exist): {e}")

    print("Database update complete.")
