VALID_PRIORITIES = {"low", "medium", "high", "blocking"}
VALID_STATUSES = {"pending", "in progress", "under review", "completed"}


class Task:
    def __init__(
        self,
        id=None,
        title=None,
        description=None,
        priority=None,
        effort_hours=None,
        status=None,
        assigned_to=None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.effort_hours = effort_hours
        self.status = status
        self.assigned_to = assigned_to

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority"),
            effort_hours=data.get("effort_hours"),
            status=data.get("status"),
            assigned_to=data.get("assigned_to"),
        )

    def validate(self, require_id=False):
        if require_id and self.id is None:
            raise ValueError("id is required")

        if not self.title or not str(self.title).strip():
            raise ValueError("title is required")

        if not self.description or not str(self.description).strip():
            raise ValueError("description is required")

        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}"
            )

        if self.effort_hours is None:
            raise ValueError("effort_hours is required")

        try:
            self.effort_hours = float(self.effort_hours)
        except (TypeError, ValueError) as exc:
            raise ValueError("effort_hours must be a decimal number") from exc

        if self.effort_hours < 0:
            raise ValueError("effort_hours must be greater than or equal to 0")

        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )

        if not self.assigned_to or not str(self.assigned_to).strip():
            raise ValueError("assigned_to is required")
