# test_api.py
import time
from pprint import pprint

import requests

BASE_URL = "http://127.0.0.1:8000"


def health_check():
    print("=== GET /health ===")
    resp = requests.get(f"{BASE_URL}/health")
    print("Status:", resp.status_code)
    pprint(resp.json())
    print()


def create_job(job_type: str = "generate_report", payload: dict | None = None) -> int | None:
    if payload is None:
        payload = {"user_id": "123", "range": "last_week"}

    print("=== POST /jobs ===")
    body = {"type": job_type, "payload": payload}
    pprint(body)

    resp = requests.post(f"{BASE_URL}/jobs", json=body)
    print("Status:", resp.status_code)
    data = resp.json()
    pprint(data)
    print()

    return data.get("id")


def get_job(job_id: int) -> dict:
    print(f"=== GET /jobs/{job_id} ===")
    resp = requests.get(f"{BASE_URL}/jobs/{job_id}")
    print("Status:", resp.status_code)
    data = resp.json()
    pprint(data)
    print()
    return data


def demo_flow():
    """
    Simple end-to-end test:
    1. Check health
    2. Create a job
    3. Poll until DONE/FAILED or timeout
    """
    health_check()

    job_id = create_job()
    if job_id is None:
        print("Failed to create job, aborting.")
        return

    print(f"Created job with id={job_id}")
    print("Polling job status... (waiting for worker.py to process it)\n")

    for i in range(10):
        print(f"Poll #{i + 1}")
        job = get_job(job_id)

        status = job.get("status")
        if status in ("DONE", "FAILED"):
            print(f"Job finished with status={status}")
            break

        time.sleep(1)
    else:
        print("Job did not finish within the polling window.")


if __name__ == "__main__":
    demo_flow()
