import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
    conn.commit()
    conn.close()
    print("Successfully added 'role' column.")
except Exception as e:
    print(f"Error: {e}")
