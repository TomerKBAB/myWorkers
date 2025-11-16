# job-related logic (create job, fetch next job, etc.)
from db import get_connection
from datetime import datetime, UTC
import json


def create_job(job_type: str, payload: dict) -> int:
    now = datetime.now(UTC).isoformat()
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

def get_job(job_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()

    return row

def get_next_pending_job():
    """
    Return the oldest PENDING job (or None if none).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM jobs
        WHERE status = 'PENDING'
        ORDER BY created_at ASC
        LIMIT 1
        """
    )
    row = cur.fetchone()
    conn.close()
    return row


def update_job_status(job_id: int, status: str, result=None, error: str | None = None, increment_attempts: bool = False):
    """
    Update status, timestamps, result/error, and optionally increment attempts.
    """
    now = datetime.now(UTC).isoformat()

    conn = get_connection()
    cur = conn.cursor()

    fields = ["status = ?", "updated_at = ?"]
    params: list = [status, now]

    if result is not None:
        fields.append("result = ?")
        params.append(json.dumps(result))

    if error is not None:
        fields.append("last_error = ?")
        params.append(error)

    if increment_attempts:
        fields.append("attempts = attempts + 1")

    params.append(job_id)

    sql = f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?"
    cur.execute(sql, params)
    conn.commit()
    conn.close()
