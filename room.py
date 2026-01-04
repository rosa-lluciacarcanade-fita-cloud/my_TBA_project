# Define the Room class.

class Room:
    """"
    This class represents a the description of room.
    
    Attributes:
        name (str): name of the player
        description (str): room's description
        exits (dict): possibilities of exit

    Methods:
        __init__(self, name, description) : The constructor.

    Examples:

    >>>
    """

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\n{self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        # Affiche les items et des personnages non joueurs présents dans la pièce.
        if not self.inventory and not self.characters:
            print("\nIl n'y a aucun objet ni personnage dans cette pièce.\n")
            return

        print("\nOn voit:")
        # Afficher les objets
        for item in self.inventory.values():
            print(f"    - {item}")
        # Afficher les personnages
        for character in self.characters.values():
            print(f"    - {character}")
        print()

    

