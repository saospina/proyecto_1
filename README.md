# Task Management API

A Flask REST API for managing user tasks. Data is stored in a JSON file, and the API is documented with Swagger via Flasgger.

## Features

- Full CRUD operations for tasks
- JSON file persistence (`data/tasks.json`)
- Layered architecture: routes → controller → service → model
- Swagger UI at `/apidocs/`
- Input validation for task fields and allowed enum values

## Requirements

- Python 3.9+
- pip

## Installation

1. Clone or download the project and enter the directory:

```bash
cd proyecto_1
```

2. Create and activate a virtual environment (if you do not already have one):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

With the virtual environment activated:

```bash
python run.py
```

Or using the Flask CLI:

```bash
flask --app run run --debug
```

The API runs at **http://127.0.0.1:5000**.

Swagger documentation is available at **http://127.0.0.1:5000/apidocs/**.

### Production (Gunicorn)

For production or deployment, use Gunicorn instead of Flask's built-in server:

```bash
gunicorn --bind 0.0.0.0:8000 run:app
```

## Deploying on Render

Create a **Web Service** with these settings:

| Setting | Value |
|---------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn --bind 0.0.0.0:$PORT run:app` |

Render sets the `$PORT` environment variable automatically. After deploy, the API will be available at your Render URL (e.g. `https://your-service.onrender.com/tasks`).

> **Note:** On Render, the filesystem is ephemeral. Data in `data/tasks.json` may be lost on redeploys unless you add persistent storage.

## Project Structure

```
proyecto_1/
├── run.py                          # Application entry point
├── requirements.txt
├── data/
│   └── tasks.json                  # Task storage
└── app/
    ├── __init__.py                 # App factory and Swagger setup
    ├── config.py                   # Configuration
    ├── models/
    │   └── task.py                 # Task domain model
    ├── services/
    │   └── task_manager.py         # JSON persistence (TaskManager)
    ├── controllers/
    │   └── task_controller.py      # Business logic
    └── routes/
        └── task_routes.py          # HTTP routes (Blueprint)
```

## Architecture

```
Client → Routes → TaskController → TaskManager → tasks.json
                                      ↓
                                    Task
```

| Layer | Responsibility |
|-------|----------------|
| **Routes** | HTTP bindings, request parsing, JSON responses |
| **Controller** | CRUD orchestration and validation |
| **TaskManager** | Load and save tasks from/to JSON |
| **Task** | Domain model with serialization helpers |

## Task Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Primary key (auto-generated on create) |
| `title` | string | Task title (required) |
| `description` | string | Full task description (required) |
| `priority` | string | `low`, `medium`, `high`, or `blocking` |
| `effort_hours` | number | Estimated hours to complete (≥ 0) |
| `status` | string | `pending`, `in progress`, `under review`, or `completed` |
| `assigned_to` | string | Team member assigned to the task (required) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks |
| GET | `/tasks/<id>` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/<id>` | Update an existing task |
| DELETE | `/tasks/<id>` | Delete a task |

### Example: Create a Task

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write tests",
    "description": "Add unit tests for TaskManager",
    "priority": "medium",
    "effort_hours": 2.0,
    "status": "pending",
    "assigned_to": "Bob"
  }'
```

Response (`201 Created`):

```json
{
  "id": 1,
  "title": "Write tests",
  "description": "Add unit tests for TaskManager",
  "priority": "medium",
  "effort_hours": 2.0,
  "status": "pending",
  "assigned_to": "Bob"
}
```

### Example: Update a Task

```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write tests",
    "description": "Updated description",
    "priority": "high",
    "effort_hours": 3.5,
    "status": "in progress",
    "assigned_to": "Bob"
  }'
```

### Error Responses

| Status | When |
|--------|------|
| `400` | Invalid or missing fields, invalid enum values |
| `404` | Task ID not found |

Error body format:

```json
{
  "error": "Task with id 999 not found"
}
```

## Data Storage

Tasks are persisted in `data/tasks.json` as a JSON array. The file is created automatically if it does not exist.

Example stored record:

```json
[
  {
    "id": 1,
    "title": "Setup CI",
    "description": "Configure pipeline",
    "priority": "high",
    "effort_hours": 4.5,
    "status": "pending",
    "assigned_to": "Alice"
  }
]
```

## Dependencies

- [Flask](https://flask.palletsprojects.com/) — web framework
- [Flasgger](https://github.com/flasgger/flasgger) — Swagger/OpenAPI documentation
- [Gunicorn](https://gunicorn.org/) — production WSGI server
