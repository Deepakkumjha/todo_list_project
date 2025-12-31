import sqlite3
from settings import BASE_DIR

conn = sqlite3.connect(BASE_DIR/'db.sqlite3')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks_task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'pending'
);
""")

conn.commit()

conn.close()
print("Table created successfully!")