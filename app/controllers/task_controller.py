from app.models.task import Task
from app.services.task_manager import TaskManager


class TaskController:
    def get_all(self):
        tasks = TaskManager.load_tasks()
        return [task.to_dict() for task in tasks], 200

    def get_by_id(self, task_id):
        tasks = TaskManager.load_tasks()
        task = next((item for item in tasks if item.id == task_id), None)

        if task is None:
            return {"error": f"Task with id {task_id} not found"}, 404

        return task.to_dict(), 200

    def create(self, data):
        if not data:
            return {"error": "Request body is required"}, 400

        task = Task.from_dict(data)

        try:
            task.validate()
        except ValueError as exc:
            return {"error": str(exc)}, 400

        tasks = TaskManager.load_tasks()
        task.id = max((item.id for item in tasks), default=0) + 1
        tasks.append(task)
        TaskManager.save_tasks(tasks)

        return task.to_dict(), 201

    def update(self, task_id, data):
        if not data:
            return {"error": "Request body is required"}, 400

        tasks = TaskManager.load_tasks()
        task = next((item for item in tasks if item.id == task_id), None)

        if task is None:
            return {"error": f"Task with id {task_id} not found"}, 404

        current = task.to_dict()
        current.update(data)
        current["id"] = task_id

        updated_task = Task.from_dict(current)

        try:
            updated_task.validate(require_id=True)
        except ValueError as exc:
            return {"error": str(exc)}, 400

        task_index = next(index for index, item in enumerate(tasks) if item.id == task_id)
        tasks[task_index] = updated_task
        TaskManager.save_tasks(tasks)

        return updated_task.to_dict(), 200

    def delete(self, task_id):
        tasks = TaskManager.load_tasks()
        task = next((item for item in tasks if item.id == task_id), None)

        if task is None:
            return {"error": f"Task with id {task_id} not found"}, 404

        tasks = [item for item in tasks if item.id != task_id]
        TaskManager.save_tasks(tasks)

        return {"message": f"Task with id {task_id} deleted successfully"}, 200
