# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        # Get the direction from the list of words.
        directions = {"NORD": "N", "N": "N", "SUD": "S", "S": "S", "OUEST": "O", "O": "O",
                      "EST": "E", "E": "E", "DOWN": "D", "D": "D", "UP":"U", "U": "U"}
        
        direction = list_of_words[1].upper() #upper = meme minuscule marche
        
        if direction in directions:
            direction = directions[direction]
            # Move the player in the direction specified by the parameter.
            player.move(direction)
        else :
            print("\nDirection", direction, "non reconnue")
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def back(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player

        if not player.history:
            print("\nVous ne pouvez pas revenir en arrière.\n")
            return False

        player.current_room = player.history.pop()
        print(player.current_room.get_long_description())
        player.get_history()
        return True
    
    def look(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        # Afficher la description longue de la pièce
        print(game.player.current_room.get_long_description())
        # Puis afficher l'inventaire de la pièce (la méthode s'occupe du message si vide)
        game.player.current_room.get_inventory()
        return True

    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        player = game.player
        item_name = list_of_words[1]
        current_room = player.current_room

        if item_name not in current_room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans cette pièce.\n")
            return False
        
        if sum(item.weight for item in player.inventory.values()) + current_room.inventory[item_name].weight > player.max_weight:
            print(f"\nVous ne pouvez pas prendre l'objet '{item_name}' car il dépasserait la limite de poids de votre inventaire ({player.max_weight} kg).\n")
            return False
            
        item = current_room.inventory.pop(item_name)
        player.inventory[item_name] = item
        print(f"\nVous avez pris l'objet '{item_name}'.\n")
        return True
    
    def drop(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        player = game.player
        item_name = list_of_words[1]

        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.\n")
            return False

        item = player.inventory.pop(item_name)
        current_room = player.current_room
        current_room.inventory[item_name] = item
        print(f"\nVous avez déposé l'objet '{item_name}'.\n")
        return True

    def check(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        # Utiliser la méthode utilitaire du joueur pour afficher l'inventaire
        player.get_inventory()
        return True

    def talk(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        player = game.player
        current_room = player.current_room

        if not current_room.characters :
            print("\nIl n'y a aucun personnage dans cette pièce avec qui parler.\n")
            return False
        
        Pnj_name = list_of_words[1].lower()

        for pnj in current_room.characters.values():
            if pnj.name.lower() == Pnj_name or Pnj_name in pnj.name.lower():
                pnj.get_msg()
                return True

        print(f"\nLe personnage '{list_of_words[1]}' n'est pas présent dans cette pièce.\n")
        return False