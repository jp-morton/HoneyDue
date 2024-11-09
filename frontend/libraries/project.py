from libraries.user import User, Role
from libraries.category import Category

class Project:
    
    def __init__(self, name, owner):
        self.name = name
        self.description = ""
        self.collaborators = {owner : Role.OWNER}
        self.tasks = []
        self.categories = []
    
    def set_name(self, new_name):
        self.name = new_name
    
    def set_description(self, new_description):
        self.description = new_description
    
    def add_collaborator(self, collaborator: str, role: Role):
        self.collaborators[collaborator] = role
    
    def add_task(self, task):
        self.tasks.append(task)

    
    def add_category(self, category):
        self.categories.append(category)
    
    def to_dict(self):
        return {"name": self.name, "description": self.description, "owner": self.owner, "members": self.members, "categories": self.categories}
    
    def update_role(self, username: str, new_role: Role):
        self.collaborators[username] = new_role

    def remove_collaborator(self, collaborator: str):
        del self.collaborators[collaborator]
