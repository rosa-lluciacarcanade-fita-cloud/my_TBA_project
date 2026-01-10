# Define the Player class.


from quest import QuestManager
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
        """
        Initialize a new player.
       
        Args:
            name (str): The name of the player.
           
        Examples:
       
        >>> player = Player("Alice")
        >>> player.name
        'Alice'
        >>> player.move_count
        0
        >>> player.rewards
        []
        """


        
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 4
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards
      # Define the move method.


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
        
        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

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


    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
       
        Args:
            reward (str): The reward to add.
           
        Examples:
       
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")




    def show_rewards(self):
        """
        Display all rewards earned by the player.
       
        Examples:
       
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()
    


