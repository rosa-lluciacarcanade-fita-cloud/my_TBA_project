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
    def __init__(self, name, description, image=None):
        """
       Initialize a Room with a name and description.
      
       >>> room = Room("Hall", "dans un grand hall")
       >>> room.name
       'Hall'
       >>> room.description
       'dans un grand hall'
       >>> room.exits
       {}
       """


        self.name = name
        self.image = image  # Path to image file (PNG/JPG) for this room
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = []
    
    # Define the get_exit method.
    def get_exit(self, direction):
        """
       Return the room in the given direction if it exists.
      
       >>> room1 = Room("Room1", "dans une pièce")
       >>> room2 = Room("Room2", "dans une autre pièce")
       >>> room1.exits["N"] = room2
       >>> room1.get_exit("N") == room2
       True
       >>> room1.get_exit("S") is None
       True
       """
        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        """
       Return a string describing the room's exits.
      
       >>> room1 = Room("Room1", "dans une pièce")
       >>> room2 = Room("Room2", "dans une autre pièce")
       >>> room3 = Room("Room3", "dans une troisième pièce")
       >>> room1.exits["N"] = room2
       >>> room1.exits["E"] = room3
       >>> room1.get_exit_string() # doctest: +ELLIPSIS
       'Sorties: ...
       """
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        """
       Return a long description of this room including exits.
      
       >>> room1 = Room("Hall", "dans un grand hall")
       >>> room2 = Room("Kitchen", "dans une cuisine")
       >>> room1.exits["N"] = room2
       >>> print(room1.get_long_description()) # doctest: +ELLIPSIS
       <BLANKLINE>
       Vous êtes dans un grand hall
       <BLANKLINE>
       Sorties: ...
       <BLANKLINE>
       """
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
        for character in self.characters :
            print(f"    - {character}")
        print()

    def add_characters(self, character):
        if character not in self.characters:
            self.characters.append(character)
            character.current_room = self

    def remove_characters(self, character):
        if character in self.characters:
            self.characters.remove(character)
            character.current_room = None
    

