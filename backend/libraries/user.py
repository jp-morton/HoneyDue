from enum import Enum

class Role(Enum):
    GUEST = 1
    MEMBER = 2
    OWNER = 3

class User:
    
    def __init__(self, name, password):
        self.username = name
        self.password = password
        self.projects = {}
    
    def add_project(self, project, role):
        self.projects[project] = role