from enum import Enum

class Role(Enum):
    OWNER = 'Owner'
    MEMBER = 'Member'
    GUEST = 'Guest'

class User:
    
    def __init__(self, name, password):
        self.username = name
        self.password = password
        self.projects = {}
    
    def add_project(self, project, role):
        self.projects[project] = role