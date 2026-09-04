class User:
    """A base class for all users in the system."""
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

    def get_details(self):
        return f"ID: {self.id}, Name: {self.name}"

    def matches(self, term):
        return term.lower() in self.name.lower()    