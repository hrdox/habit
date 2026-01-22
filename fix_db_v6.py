from app import app, db
from sqlalchemy import text

def run_sql(sql):
    try:
        with app.app_context():
            db.session.execute(text(sql))
            db.session.commit()
            print(f"Executed: {sql}")
    except Exception as e:
        print(f"Error executing {sql}: {e}")

if __name__ == "__main__":
    run_sql("ALTER TABLE \"audit_log\" ADD COLUMN ipv6_address VARCHAR(45)")
