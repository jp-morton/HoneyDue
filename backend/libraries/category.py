from task import Status

class Category:
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.status = Status.TODO
        self.task_list = []
    
    def set_name(self, new_name):
        self.name = new_name
    
    def set_description(self, new_description):
        self.description = new_description
    
    def add_task(self, task):
        self.task_list.append(task)