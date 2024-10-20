from user import User
from category import Category



class Project:
    
    def __init__(self, name, description, owner):
        self.name = name
        self.description = description
        self.owner = owner
        self.members = [owner]
        self.categories = []
    
    def set_name(self, new_name):
        self.name = new_name
    
    def set_description(self, new_description):
        self.description = new_description
    
    def add_member(self, member):
        self.members.append(member)
    
    def add_category(self, category):
        self.categories.append(category)

