# job-related logic (create job, fetch next job, etc.)
from db import get_connection
from datetime import datetime


def create_job(job_type: str, payload: dict) -> int:
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO jobs (type, payload, status, created_at, updated_at, attempts)
    VALUES (?, ?, ?, ?, ?, 0)
    """,
    (job_type, json.dumps(payload), "PENDING", now, now),
    )
    conn.commit()
    job_id = cur.lastrowid
    conn.close()
    return job_id