# 🧵 Job Queue System

A lightweight backend **job queue** built in Python.
The system provides an HTTP API for clients to create jobs and a separate background worker process that executes those jobs asynchronously.

This project demonstrates core backend concepts such as API design, background processing, database persistence, error handling, and clean service separation — similar in spirit to tools like Celery or Sidekiq, but implemented from scratch for learning purposes.

---

## 🚀 Features

* **FastAPI HTTP API**

  * `POST /jobs` — create a new job
  * `GET /jobs/{id}` — fetch job status and result
* **Background Worker**

  * Runs independently via `python worker.py`
  * Polls the database for pending jobs
  * Executes jobs and updates status (`PENDING → RUNNING → DONE/FAILED`)
  * Tracks retries, errors, timestamps, and results
* **SQLite Database**

  * Stores all jobs persistently
  * Automatic schema initialization on startup
* **Clean Architecture**

  * API layer (FastAPI)
  * Service logic (`services.py`)
  * Database layer (`db.py`)
  * Worker process (`worker.py`)

---

## 🧱 Architecture

```
+-----------+        POST /jobs         +-----------+
|  Client   | -------------------------> |   API     |
+-----------+                           |  Server   |
                                         +-----------+
                                                |
                                                | INSERT job (PENDING)
                                                v
                                         +-----------+
                                         |   DB      |
                                         +-----------+
                                                ^
                                                | SELECT next PENDING
                                                |
                                         +-----------+
                                         |  Worker   |
                                         |  python   |
                                         +-----------+
```

The API is responsible for validating input and creating jobs in the database.
The worker is responsible for picking up jobs, running them, and storing results.

---

## 📦 Installation

```bash
git clone <your-repo>
cd jobQueueSystem
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ▶️ Running the Services

### 1. Start the API server

```bash
uvicorn app:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Test it:

```
GET /health
```

---

### 2. Start the worker

In a separate terminal:

```bash
python worker.py
```

The worker will continuously poll the DB for new jobs and execute them.

---

## 📝 API Endpoints

### **POST /jobs**

Create a new job.

#### Request body:

```json
{
  "type": "generate_report",
  "payload": {
    "user_id": "123",
    "range": "last_week"
  }
}
```

#### Response:

```json
{
  "id": 1,
  "status": "PENDING"
}
```

---

### **GET /jobs/{id}**

Retrieve job information and result.

```json
{
  "id": 1,
  "type": "generate_report",
  "status": "DONE",
  "attempts": 1,
  "result": {"report": "ok"},
  "last_error": null
}
```

---

## 📂 Project Structure

```
jobQueueSystem/
│
├── app.py          # FastAPI app and endpoints
├── worker.py       # Background worker loop
├── db.py           # DB connection + schema initialization
├── services.py     # Business logic for job management
├── models.py       # SQL helpers or ORM models
├── config.py       # Constants (DB path, retry limits, etc.)
├── requirements.txt
└── README.md
```

---

## 🧩 Job Lifecycle

```
PENDING → RUNNING → DONE
           ↓
         FAILED
```

The worker handles transitions, retries, and error logging.

---

## 🎯 Future Improvements

* Multiple worker processes
* Priority queues
* Scheduled jobs (`run_at`)
* Job cancellation
* Replace SQLite with PostgreSQL
* Add metrics or logging dashboard

---

## 📜 License

MIT — free to use and modify.

---
