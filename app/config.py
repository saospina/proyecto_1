import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    TASKS_FILE = os.path.join(BASE_DIR, "data", "tasks.json")
    SWAGGER_TITLE = "Task Management API"
    SWAGGER_VERSION = "1.0.0"
    SWAGGER_DESCRIPTION = "REST API for managing user tasks with JSON file storage"
