import json
from fastapi import FastAPI
from db import init_db
from services import create_job, get_job
from models import JobCreate

init_db()
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job_endpoint(job: JobCreate):
    # request validation happens at pydantic level
    job_id = create_job(job.type, job.payload)
    return {"id": job_id, "status": "PENDING"}


@app.get("/jobs/{job_id}")
def get_job_endpoint(job_id: int):
    row = get_job(job_id)
    if row is None:
        return {"error": "Job not found"}

    data = dict(row)

    # Decode JSON string payload back to a dict
    if data.get("payload") is not None:
        data["payload"] = json.loads(data["payload"])

    # Decode JSON string result back to a dict (if it is JSON)
    if data.get("result") is not None:
        try:
            data["result"] = json.loads(data["result"])
        except json.JSONDecodeError:
            # if it's not valid JSON, just leave it as-is
            pass

    return data
