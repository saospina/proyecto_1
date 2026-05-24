from flask import Blueprint, jsonify, request

from app.controllers.task_controller import TaskController

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
task_controller = TaskController()


@task_bp.route("", methods=["GET"])
def get_tasks():
    """Get all tasks
    ---
    tags:
      - Tasks
    responses:
      200:
        description: List of all tasks
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
    """
    result, status_code = task_controller.get_all()
    return jsonify(result), status_code


@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a task by ID
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: Task identifier
    responses:
      200:
        description: Task found
        schema:
          $ref: '#/definitions/Task'
      404:
        description: Task not found
        schema:
          $ref: '#/definitions/Error'
    """
    result, status_code = task_controller.get_by_id(task_id)
    return jsonify(result), status_code


@task_bp.route("", methods=["POST"])
def create_task():
    """Create a new task
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/TaskInput'
    responses:
      201:
        description: Task created
        schema:
          $ref: '#/definitions/Task'
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json(silent=True)
    result, status_code = task_controller.create(data)
    return jsonify(result), status_code


@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: Task identifier
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/TaskInput'
    responses:
      200:
        description: Task updated
        schema:
          $ref: '#/definitions/Task'
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Task not found
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json(silent=True)
    result, status_code = task_controller.update(task_id, data)
    return jsonify(result), status_code


@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: Task identifier
    responses:
      200:
        description: Task deleted
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Task not found
        schema:
          $ref: '#/definitions/Error'
    """
    result, status_code = task_controller.delete(task_id)
    return jsonify(result), status_code
