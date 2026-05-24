import json
import os

from app.config import Config
from app.models.task import Task


class TaskManager:
    @staticmethod
    def load_tasks():
        tasks_file = Config.TASKS_FILE

        if not os.path.exists(tasks_file):
            return []

        with open(tasks_file, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []

            data = json.loads(content)

        return [Task.from_dict(item) for item in data]

    @staticmethod
    def save_tasks(tasks):
        tasks_file = Config.TASKS_FILE
        os.makedirs(os.path.dirname(tasks_file), exist_ok=True)

        with open(tasks_file, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=2)
