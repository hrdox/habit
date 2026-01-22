from app import app, db
from sqlalchemy import text

def add_column(table, column, type):
    try:
        with app.app_context():
            db.session.execute(text(f"ALTER TABLE \"{table}\" ADD COLUMN {column} {type}"))
            db.session.commit()
            print(f"Added {column} to {table}")
    except Exception as e:
        print(f"Error adding {column} to {table}: {e}")

if __name__ == "__main__":
    add_column("user", "local_ip", "VARCHAR(45)")
    add_column("audit_log", "local_ip", "VARCHAR(45)")
