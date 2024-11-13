from enum import Enum

class Status(Enum):
    TODO = 1
    DOING = 2
    DONE = 3

class Task:
    
    def __init__(self, name, description, priority, deadline, category, status, assignee):
        self.name = name
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.category = category
        self.status = status
        self.assignee = assignee

    def set_name(self, new_name):
        self.name = new_name

    def set_description(self, new_description):
        self.description = new_description

    def set_priority(self, new_priority):
        self.priority = new_priority

    def set_deadline(self, new_deadline):
        self.deadline = new_deadline

    def set_category(self, new_category):
        self.category = new_category

    def set_status(self, new_status):
        self.status = new_status

    def set_assignee(self, new_assignee):
        self.assignee = new_assignee

    def to_dict(self):
        return {"name": self.name, "description": self.description, "priority": self.priority, "deadline": self.deadline, "category": self.category, "status": self.status, "assignee": self.assignee,}
