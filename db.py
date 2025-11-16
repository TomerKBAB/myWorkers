 # DB connection / engine setup + initilize job table
import sqlite3

DB_PATH = "jobs.db"

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

def get_connection():
    """
    Returns a new SQLite connection.
    IMPORTANT: The caller is responsible for closing the connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # optional: allows dict-like rows
    return conn