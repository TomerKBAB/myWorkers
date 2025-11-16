# tests/test_api.py
import pytest
from fastapi.testclient import TestClient

from app import app
from db import init_db, get_connection


@pytest.fixture(autouse=True)
def clean_db():
    """
    Runs before each test:
    - ensure the DB schema exists
    - clear the jobs table so tests don't affect each other
    """
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()
    yield


@pytest.fixture
def client():
    """
    A TestClient instance for talking to the FastAPI app.
    """
    return TestClient(app)


def test_health_endpoint(client: TestClient):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_job_and_get_job(client: TestClient):
    # Create a job
    payload = {"user_id": "123", "range": "last_week"}
    body = {"type": "generate_report", "payload": payload}

    resp = client.post("/jobs", json=body)
    assert resp.status_code == 200

    data = resp.json()
    assert "id" in data
    assert data["status"] == "PENDING"

    job_id = data["id"]

    # Fetch the job
    resp2 = client.get(f"/jobs/{job_id}")
    assert resp2.status_code == 200

    job = resp2.json()
    assert job["id"] == job_id
    assert job["type"] == "generate_report"
    assert job["status"] == "PENDING"
    assert job["payload"] == payload
    assert job["attempts"] == 0
    assert job["result"] is None
    assert job["last_error"] is None


def test_get_missing_job_returns_error_object(client: TestClient):
    # This tests current behavior (200 + {"error": ...})
    # If later you change to proper 404, you’ll update this test.
    resp = client.get("/jobs/999999")
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data
    assert data["detail"] == "Job not found"
