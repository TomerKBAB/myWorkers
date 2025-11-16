from fastapi import FastAPI
from db import init_db
from pydantic import BaseModel


class JobCreate(BaseModel):
    type: str
    payload: dict


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs")
def create_job_endpoint(job: JobCreate):
    # call services create job
    pass



def main():
    init_db()
    app = FastAPI()
    

if __name__ == "__main__":
    main()