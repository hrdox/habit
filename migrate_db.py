from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Check if column exists
        with db.engine.connect() as conn:
            # SQLite specific pragmas or just try adding
            # Simple way: try to select it.
            try:
                conn.execute(text("SELECT points FROM habit LIMIT 1"))
                print("Column 'points' already exists.")
            except Exception:
                print("Adding 'points' column...")
                conn.execute(text("ALTER TABLE habit ADD COLUMN points INTEGER DEFAULT 10"))
                print("Migration successful.")
                conn.commit()
    except Exception as e:
        print(f"Migration Failed: {e}")
