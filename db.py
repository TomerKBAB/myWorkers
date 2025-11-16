 # DB connection / engine setup + initilize job table
import sqlite3

def init_db():
    con = sqlite3.connect("Jobs.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        payload TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        attempts INTEGER DEFAULT 0,
        result TEXT,
        last_error TEXT
    );
    """)
    con.commit()
    con.close()
