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
    # Add device_fingerprint to user
    run_sql("ALTER TABLE \"user\" ADD COLUMN device_fingerprint VARCHAR(255)")
    
    # Widen local_ip in both tables (syntax varies by DB but usually ALTER TABLE table ALTER COLUMN col TYPE new_type)
    # For SQLite we might need to be careful, but Render uses Postgres
    db_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    if 'postgresql' in db_url:
        run_sql("ALTER TABLE \"user\" ALTER COLUMN local_ip TYPE VARCHAR(100)")
        run_sql("ALTER TABLE \"audit_log\" ALTER COLUMN local_ip TYPE VARCHAR(100)")
    else:
        # SQLite doesn't support ALTER COLUMN TYPE easily, but we just added them as 45 so 100 should be fine if we recreate? 
        # Actually in SQLite VARCHAR(45) and VARCHAR(100) are the same (TEXT).
        pass
