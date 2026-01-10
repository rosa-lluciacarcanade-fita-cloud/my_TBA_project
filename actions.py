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

    #PROBLEME le PNJ peut avoir current_room = nouvelle salle mais rester listé dans old_room.characters, d'où le message "n'est pas présent" quand on cherche le PNJ dans la salle.
    def move_pnj(game, list_of_words, number_of_parameters):
        for character in game.characters:
            character.move()
        return True
    

@staticmethod

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
        >>> game.setup("TestPlayer")
        >>> Actions.go(game, ["go", "N"], 1)
        <BLANKLINE>
        Vous êtes dans une immense tour en pierre qui s'élève au dessus des nuages.
        <BLANKLINE>
        Sorties: N, S, O
        <BLANKLINE>
        True
        >>> Actions.go(game, ["go", "N", "E"], 1)
        <BLANKLINE>
        La commande 'go' prend 1 seul paramètre.
        <BLANKLINE>
        False
        >>> Actions.go(game, ["go"], 1)
        <BLANKLINE>
        La commande 'go' prend 1 seul paramètre.
        <BLANKLINE>
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
            Actions.move_pnj(game, [], 0)
            player.move(direction)
        else :
            print("\nDirection", direction, "non reconnue")
        return True


@staticmethod

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
        >>> game.setup("TestPlayer")
        >>> Actions.quit(game, ["quit"], 0)
        <BLANKLINE>
        Merci TestPlayer d'avoir joué. Au revoir.
        <BLANKLINE>
        True
        >>> Actions.quit(game, ["quit", "N"], 0)
        <BLANKLINE>
        La commande 'quit' ne prend pas de paramètre.
        <BLANKLINE>
        False
        >>> Actions.quit(game, ["quit", "N", "E"], 0)
        <BLANKLINE>
        La commande 'quit' ne prend pas de paramètre.
        <BLANKLINE>
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

@staticmethod

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
        >>> game.setup("TestPlayer")
        >>> Actions.help(game, ["help"], 0) # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        Voici les commandes disponibles:
            - help : afficher cette aide
            - quit : quitter le jeu
            - go <direction> : se déplacer dans une direction cardinale (N, E, S, O)
            - quests : afficher la liste des quêtes
            - quest <titre> : afficher les détails d'une quête
            - activate <titre> : activer une quête
            - rewards : afficher vos récompenses
        <BLANKLINE>
        True
        >>> Actions.help(game, ["help", "N"], 0)
        <BLANKLINE>
        La commande 'help' ne prend pas de paramètre.
        <BLANKLINE>
        False
        >>> Actions.help(game, ["help", "N", "E"], 0)
        <BLANKLINE>
        La commande 'help' ne prend pas de paramètre.
        <BLANKLINE>
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


@staticmethod
    
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


@staticmethod
    
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


@staticmethod

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


@staticmethod
    
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


@staticmethod

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


@staticmethod

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

        for pnj in current_room.characters:
            if pnj.name.lower() == Pnj_name or Pnj_name in pnj.name.lower():
                pnj.get_msg()
                return True

        print(f"\nLe personnage '{list_of_words[1]}' n'est pas présent dans cette pièce.\n")
        return False


@staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
       
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False


        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False


        # Show all quests
        game.player.quest_manager.show_quests()
        return True




    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
       
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False


        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False


        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])


        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }


        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True




    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
       
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False


        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False


        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])


        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True


        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
       
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False


        # Show all rewards
        game.player.show_rewards()
        return True