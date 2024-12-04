class Task:
    """
    A class representing a task with attributes for organization and tracking.

    Attributes:
        name (str): The name of the task.
        description (str): A description of the task.
        priority (int): The priority level of the task (1-5).
        deadline (str): The deadline for completing the task (e.g., in 'YYYY-MM-DD' format).
        category (str): The name of the category of the task.
        status (str): The current status of the task (TODO, DOING, DONE).
        assignee (str): The username of the user responsible for the task.
    """

    def __init__(self, name, description, priority, deadline, category, status, assignee):
        """
        Initializes a Task instance.

        Args:
            name (str): The name of the task.
            description (str): A description of the task.
            priority (int): The priority level of the task.
            deadline (str): The deadline for the task.
            category (str): The category of the task.
            status (str): The current status of the task.
            assignee (str): The name of the person assigned to the task.
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.category = category
        self.status = status
        self.assignee = assignee

    def to_dict(self):
        """
        Converts the task instance into a dictionary.

        Returns:
            dict: A dictionary representation of the task.
        """

        return {"name": self.name, "description": self.description, "priority": self.priority, "deadline": self.deadline, "category": self.category, "status": self.status, "assignee": self.assignee,}
