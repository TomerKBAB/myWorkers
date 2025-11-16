# worker.py
import time
import json
from datetime import datetime, UTC

from services import get_next_pending_job, update_job_status

POLL_INTERVAL_SECONDS = 1.0


def process_job(row) -> dict:
    """
    Simulate doing work for a job and return a result dict.
    """
    job_id = row["id"]
    job_type = row["type"]
    payload_raw = row["payload"]
    payload = json.loads(payload_raw) if payload_raw else None

    print(f"[{datetime.now(UTC).isoformat()}] Processing job {job_id} ({job_type}) with payload={payload}")

    # Very simple branching per job type
    if job_type == "generate_report":
        time.sleep(2)
        return {
            "message": "Report generated",
            "job_id": job_id,
            "payload": payload,
        }
    else:
        # generic fallback
        time.sleep(1)
        return {
            "message": "Job completed",
            "job_id": job_id,
            "type": job_type,
            "payload": payload,
        }


def main():
    print("Worker started. Polling for jobs...")

    while True:
        row = get_next_pending_job()
        if row is None:
            # no jobs right now
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        job_id = row["id"]

        # Mark as RUNNING and increment attempts
        update_job_status(job_id, status="RUNNING", increment_attempts=True)

        try:
            result = process_job(row)
            update_job_status(job_id, status="DONE", result=result)
        except Exception as exc:
            # If something goes wrong, mark as FAILED
            update_job_status(job_id, status="FAILED", error=str(exc))

        # Small delay before checking for the next job
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
