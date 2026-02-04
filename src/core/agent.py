class Calcifer:
    def __init__(self):
        self.identity = None
        self.memory = None
        self.skills = {}

    def load_context(self):
        """
        Load:
        - SOUL.md (identity)
        - USER.md (user model)
        - daily memory
        """
        pass

    def route(self, message):
        """
        Determine which skill should handle request
        """
        pass

    def run(self):
        print("Calcifer online.")
