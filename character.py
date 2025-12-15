class Character :
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.current_room = None
        self.msgs = []

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move(self):
        if self.next_room == self.current_room:
            return True
        else:
            return False