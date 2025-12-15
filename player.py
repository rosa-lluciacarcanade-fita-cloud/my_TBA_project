# Define the Player class.
class Player():
    """"
    This class represents the player and the room where he is .
    
    Attributes:
        name (str): name of the player
        current_room (Room): the room where the player is

    Methods:
        __init__(self, name) : The constructor.

    Examples:

    >>>
    """

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 4

    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.history.append(self.current_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())
        self.get_history()
        return True

    def get_history (self):
        print (f"\nVous avez déjà visité les pièces suivantes:")
        for pieces in self.history:
            # `pieces` est un objet Room ; afficher son nom si possible
            try:
                print(f"    - {pieces.name}")
            except Exception:
                print(f"    - {pieces}")

    def get_inventory(self):
        if not self.inventory:
            print("\nVotre inventaire est vide.\n")
            return
        print("\nVoici les objets dans votre inventaire:")
        for item in self.inventory.values():
            print(f"    - {item}")
        print()

    


