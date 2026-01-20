import sqlite3
import os

db_path = os.path.join('instance', 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking schedule_log table structure...")

# Get current columns
cursor.execute("PRAGMA table_info(schedule_log)")
columns = [col[1] for col in cursor.fetchall()]

# Columns to add
to_add = [
    ('task', 'TEXT'),
    ('time', 'TEXT'),
    ('is_routine', 'BOOLEAN DEFAULT 0')
]

for col_name, col_type in to_add:
    if col_name not in columns:
        print(f"Adding column {col_name}...")
        try:
            cursor.execute(f"ALTER TABLE schedule_log ADD COLUMN {col_name} {col_type}")
        except Exception as e:
            print(f"Error adding {col_name}: {e}")
    else:
        print(f"Column {col_name} already exists.")

# Check if routine_id is nullable (SQLite doesn't support ALTER COLUMN easily)
# However, we can just ensure it doesn't crash if we pass NULL
# PRAGMA doesn't show 'nullable' directly in a simple way to change, 
# but we can try to drop the NOT NULL constraint if mandatory.
# In SQLite, the easiest way to make a column nullable if it wasn't is to recreate the table.
# But let's check if it actually has NOT NULL.

cursor.execute("PRAGMA table_info(schedule_log)")
col_info = cursor.fetchall()
routine_id_info = next((c for c in col_info if c[1] == 'routine_id'), None)

if routine_id_info and routine_id_info[3] == 1: # 1 means NOT NULL
    print("routine_id has NOT NULL constraint. Recreating table to remove it...")
    # This is a bit risky but necessary for ad-hoc tasks
    cursor.execute("CREATE TABLE schedule_log_new AS SELECT * FROM schedule_log")
    cursor.execute("DROP TABLE schedule_log")
    # Recreate with proper schema
    cursor.execute("""
    CREATE TABLE schedule_log (
        id INTEGER PRIMARY KEY,
        routine_id INTEGER,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        task TEXT,
        time TEXT,
        status BOOLEAN DEFAULT 0,
        points INTEGER DEFAULT 10,
        is_routine BOOLEAN DEFAULT 0,
        day_id INTEGER,
        FOREIGN KEY(routine_id) REFERENCES routine_item (id),
        FOREIGN KEY(user_id) REFERENCES user (id),
        FOREIGN KEY(day_id) REFERENCES day (id)
    )
    """)
    # Copy data back
    # We need to list columns explicitly to match names
    cursor.execute("INSERT INTO schedule_log SELECT * FROM schedule_log_new")
    cursor.execute("DROP TABLE schedule_log_new")
    print("Table schedule_log recreated successfully.")

conn.commit()
conn.close()
print("Migration complete.")
