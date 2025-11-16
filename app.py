from fastapi import FastAPI
from db import init_db
from pydantic import BaseModel
from services import create_job


class JobCreate(BaseModel):
    type: str
    payload: dict


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs")
def create_job_endpoint(job: JobCreate):
    # request validation happens at pydantic level
    job_id = create_job(job.type, job.payload)
    return {"id": job_id, "status": "PENDING"}
    



def main():
    init_db()
    app = FastAPI()
    

if __name__ == "__main__":
    main()