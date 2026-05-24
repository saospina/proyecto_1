from flask import Flask
from flasgger import Swagger

from app.config import Config
from app.routes.task_routes import task_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": Config.SWAGGER_TITLE,
                "description": Config.SWAGGER_DESCRIPTION,
                "version": Config.SWAGGER_VERSION,
            },
            "definitions": {
                "Task": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "title": {"type": "string", "example": "Write tests"},
                        "description": {
                            "type": "string",
                            "example": "Add unit tests for TaskManager",
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "blocking"],
                            "example": "medium",
                        },
                        "effort_hours": {"type": "number", "example": 2.0},
                        "status": {
                            "type": "string",
                            "enum": [
                                "pending",
                                "in progress",
                                "under review",
                                "completed",
                            ],
                            "example": "pending",
                        },
                        "assigned_to": {"type": "string", "example": "Bob"},
                    },
                },
                "TaskInput": {
                    "type": "object",
                    "required": [
                        "title",
                        "description",
                        "priority",
                        "effort_hours",
                        "status",
                        "assigned_to",
                    ],
                    "properties": {
                        "title": {"type": "string", "example": "Write tests"},
                        "description": {
                            "type": "string",
                            "example": "Add unit tests for TaskManager",
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "blocking"],
                            "example": "medium",
                        },
                        "effort_hours": {"type": "number", "example": 2.0},
                        "status": {
                            "type": "string",
                            "enum": [
                                "pending",
                                "in progress",
                                "under review",
                                "completed",
                            ],
                            "example": "pending",
                        },
                        "assigned_to": {"type": "string", "example": "Bob"},
                    },
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "example": "Task not found"},
                    },
                },
            },
        },
    )

    app.register_blueprint(task_bp)
    return app
