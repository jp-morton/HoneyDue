from libraries.user import User
from libraries.category import Category

class Project:
    
    def __init__(self, name, owner):
        self.name = name
        self.description = ""
        self.owner = owner
        self.members = [owner]
        self.tasks = []
        self.categories = []
    
    def set_name(self, new_name):
        self.name = new_name
    
    def set_description(self, new_description):
        self.description = new_description
    
    def add_member(self, member):
        self.members.append(member)
    
    def add_task(self, task):
        self.tasks.append(task)

    
    def add_category(self, category):
        self.categories.append(category)
    
    def to_dict(self):
        return {"name": self.name, "description": self.description, "owner": self.owner, "members": self.members, "categories": self.categories}

