from libraries.user import Role

class Project:
    """
    A class used to represent a project.

    Attributes:
        name (str): The name of the project.
        description (str): A description of the project.
        collaborators (dict): A dictionary of collaborators and their roles in the project.
        tasks (list): A list of tasks associated with the project.
        categories (list): A list of task categories for the project.

    Methods:
        add_collaborator(collaborator, role):
            Adds a collaborator to the project's collaborator dictionary.
        update_role(username, new_role):
            Updates a collaborator's role in the project.
        remove_collaborator(collaborator):
            Removes a collaborator from the project.
        remove_category(category):
            Removes a category from the project's category list.
    """
    
    def __init__(self, name, owner):
        """
        Initializes a Project instance.

        Args:
            name (str): The name of the project.
            owner (str): The username of the project's creator.
        """
        self.name = name
        self.description = ""
        self.collaborators = {owner : Role.OWNER}
        self.tasks = []
        self.categories = ["None"]
    
    def add_collaborator(self, collaborator: str, role: Role):
        """
        Adds a collaborator to the project.

        Args:
            collaborator (str): The username of the collaborator to be added.
            role (Role): The role assigned to the collaborator (OWNER, MEMBER, or GUEST).
        """
        self.collaborators[collaborator] = role

    def update_role(self, username: str, new_role: Role):
        """
        Updates the role of an existing collaborator.

        Args:
            username (str): The username of the collaborator whose role is to be updated.
            new_role (Role): The new role to assign to the collaborator (OWNER, MEMBER, or GUEST).
        """
        self.collaborators[username] = new_role

    def remove_collaborator(self, collaborator: str):
        """
        Removes a collaborator from the project.

        Args:
            collaborator (str): The username of the collaborator to remove.
        """
        del self.collaborators[collaborator]

    def remove_category(self, category: str):
        """
        Removes a category from the project.

        Args:
            category (str): The name of the category to remove.
        """
        self.categories.remove(category)
