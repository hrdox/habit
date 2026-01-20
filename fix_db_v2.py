import sqlite3
import os

paths = ['db.sqlite3', 'instance/db.sqlite3']

for path in paths:
    if os.path.exists(path):
        print(f"Check database at: {path}")
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            # Check if role column exists
            try:
                cursor.execute("SELECT role FROM user LIMIT 1")
                print(" - 'role' column already exists.")
            except sqlite3.OperationalError:
                print(" - 'role' column missing. Attempting to add...")
                cursor.execute("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
                conn.commit()
                print(" - Successfully added 'role' column!")
            conn.close()
        except sqlite3.OperationalError as e:
            print(f" - Error opening/modifying DB (might be locked or corrupt): {e}")
        except Exception as e:
            print(f" - Unexpected error: {e}")
    else:
        print(f"No DB found at {path}")
