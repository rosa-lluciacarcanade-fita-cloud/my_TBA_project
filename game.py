# Description: Game class
# Import modules
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from quest import Quest
from character import Character

DEBUG = True
class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.directions = set()
        self.characters = {}

    # Setup the game
    def setup(self, player_name=None):
        """Initialize the game with  commands, rooms, items, characters and quests."""
        self._setup_commands()
        self._setup_rooms()
        self._setup_player(player_name)
        self._setup_quests()

    # Setup commands
    def _setup_commands(self):
        """Initialize all game commands."""
        self.commands["help"] = Command("help"
                                        , " : afficher cette aide"
                                        , Actions.help
                                        , 0)
        self.commands["quit"] = Command("quit"
                                        , " : quitter le jeu"
                                        , Actions.quit
                                        , 0)
        self.commands["go"] = Command("go"
                                      , "<N|E|S|O|U|D> : se déplacer dans une direction cardinale"
                                      , Actions.go
                                      , 1)
        self.commands["take"] = Command("take"
                                        , "<nom_objet> : prendre un objet"
                                        , Actions.take
                                        , 1)
        self.commands["drop"] = Command("drop"
                                        , "<nom_objet> : déposer un objet"
                                        , Actions.drop
                                        , 1)
        self.commands["back"] = Command("back"
                                        , " : revenir en arrière"
                                        , Actions.back
                                        , 0)
        self.commands["look"] = Command("look"
                                        , " : observer la pièce"
                                        , Actions.look
                                        , 0)
        self.commands["check"] = Command("check"
                                         , " : vérifier l'inventaire"
                                         , Actions.check
                                         , 0)
        self.commands["talk"] = Command("talk"
                                        , "<nom_personnage> : parler à un personnage non-joueur"
                                        , Actions.talk
                                        , 1)
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , "<nom_quête> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                           , "<nom_objet> : activer un objet spécial"
                                           , Actions.activate
                                           , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)

     # Setup rooms
    def _setup_rooms(self):
        """Initialize all rooms and their exits."""
        # Create rooms
        s =  "Exterieur " \
        "\n Le trottoir devant la boîte : gens qui fument, Uber en warning " \
        "\n et toi qui as peur de te faire recaler à l'entrée."
        exterieur = Room("Exterieur", s)

        s = "Billetterie " \
        "\n Petite file, vigile blasé, machine à CB qui fait plus de bruit que la sono. " \
        "\n Tu pries pour que ta carte passe."
        billetterie = Room("Billetterie", s)

        s = "Vestiaire " \
        "\n Mega pile de manteaux, ticket froissé dans ta main, et la peur d’oublier " \
        "\n le numéro à 3h du matin."
        vestiaire = Room("Vestiaire", s)

        s = "Salle Techno " \
        "\n Stroboscopes, basses qui te font vibrer les organes, DJ qui ne sourit jamais " \
        "\n mais tout le monde l’adore."
        salle_techno = Room("Salle Techno", s)

        s = "Salle Rap US / FR " \
        "\n Ça crie les lyrics plus fort que le son, tout le monde " \
        "\n fait semblant de connaître tous les couplets."
        salle_rap = Room("Salle Rap US / FR", s)

        s = "Salle House " \
        "\n Ambiance house, kicks propres, mélodies qui donnent envie de lever les bras " \
        "\n même si tu sais pas danser. Les gens ici font genre qu'ils comprennent le mix."
        salle_house = Room("Salle House", s)

        s = "Salle Latino / Shatta " \
        "\n Ambiance caliente, déhanchés sérieux, gens qui dansent trop bien pour que " \
        "\n tu restes fidèle. Tu hésites entre te laisser tenter ou fuir."
        salle_latino = Room("Salle Latino / Shatta", s)

        s = "Fumoir " \
        "\n Aqua enfumée, discussions philosophiques à 2h du mat, " \
        "\n et quelqu’un qui parle de lancer un start-up à chaque bouffée."
        fumoir = Room("Fumoir", s)

        s = "Secret Room " \
        "\n Une petite salle cachée dont personne ne connaît vraiment la règle d’accès. " \
        "\n Si tu es là, soit t’es VIP, soit tu t’es perdu."
        secret_room = Room("Secret Room", s)

        s = "Rooftop " \
        "\n Vue sur la ville, guirlandes lumineuses, air frais qui sauve des coups de chaud. " \
        "\n Endroit parfait pour pécho ton pain autour d'un verre de rosé."
        rooftop = Room("Rooftop", s)


        # Add rooms to game
        for room in [exterieur, billetterie, vestiaire, salle_techno, salle_rap,
                     salle_house, salle_latino, fumoir, secret_room, rooftop]:
            self.rooms.append(room)


        # Create exits for rooms
        exterieur.exits = {"N" : billetterie,
                           "E" : None,
                           "S" : None,
                           "O" : None,
                           "U" : None,
                           "D" : None}

        billetterie.exits = {"N" : None,
                             "E" : vestiaire,
                             "S" : None,
                             "O" : None,
                             "U" : None,
                             "D" : None}

        vestiaire.exits = {"N" : None,
                           "E" : None,
                           "S" : None,
                           "O" : billetterie,
                           "U" : salle_house,
                           "D" : fumoir}

        salle_house.exits = {"N" : salle_techno,
                             "E" : None,
                             "S" : None,
                             "O" : salle_latino,
                             "U" : rooftop,
                             "D" : vestiaire}

        salle_latino.exits = {"N" : salle_rap,
                              "E" : salle_house,
                              "S" : None,
                              "O" : None,
                              "U" : None,
                              "D" : None}

        salle_rap.exits = {"N" : None,
                           "E" : None,
                           "S" : salle_latino,
                           "O" : None,
                           "U" : None,
                           "D" : None}

        salle_techno.exits = {"N" : None,
                              "E" : None,
                              "S" : salle_house,
                              "O" : None,
                              "U" : None,
                              "D" : None}

        rooftop.exits = {"N" : None,
                         "E" : None,
                         "S" : None,
                         "O" : None,
                         "U" : None,
                         "D" : salle_house}

        fumoir.exits = {"N" : None,
                        "E" : None,
                        "S" : None,
                        "O" : secret_room,
                        "U" : vestiaire,
                        "D" : None}

        secret_room.exits = {"N" : None,
                             "E" : None,
                             "S" : None,
                             "O" : None,
                             "U" : None,
                             "D" : None}

        # Setup items
        vestiaire.inventory = {
            "ticket_vestiaire": Item("ticket_vestiaire", "Indispensable pour récupérer ton manteau plus tard.", 1),
            "bouteille_de_sirop_magiques": Item("bouteille_de_sirop_magiques", "Pour une soirée de farfadet où ton cerveau va alluciner.", 1)
        }
        salle_rap.inventory = {
            "pass_carré_VIP": Item("pass_carré_VIP", "Essentiel pour accéder à la soirée de la secret room, seulement pour les plus hots...", 1),
            "un_mètre_de_shooter": Item("un_mètre_de_shooter", "Un long shooter à partager, ou non. Ton foie va-t-il résister ?", 1)
        }
        rooftop.inventory = {
            "sex_on_the_beach": Item("sex_on_the_beach", "Un cocktail sucré et coloré, parfait pour débuter la soirée.", 1)
        }
        fumoir.inventory = {
            "casque_DJ": Item("casque_DJ", "Le casque du DJ, sans lequel elle ne peut pas mixer.", 1),
        }

        # Setup characters/PNJ
        salle_house.characters = {
            "DJ_Rosita": Character("DJ_Rosita", "La reine des platines house, toujours prête à faire danser la foule avec ses mixes enflammés.", salle_house, ["Salut toi ! Prêt à bouger sur mes beats ?", "La house, c'est plus qu'un genre musical, c'est un mode de vie.", "Si tu veux que je te prépare un set spécial, faut que tu me montres ton énergie sur le dancefloor."]),  
            "Tony_le_barman_bg": Character("Tony", "Le barman le plus cool de la boîte, toujours prêt à te servir un cocktail avec le sourire.", salle_house, ["Qu'est-ce que je te sers ce soir ? J'ai des cocktails qui font danser même les plus timides !", "Tu sais, la clé d'une bonne soirée, c'est un bon cocktail et une bonne compagnie.", "Si tu cherches quelque chose de spécial, demande-moi, j'ai des recettes secrètes."])      
        }
        salle_latino.characters = {
            "Anadélys": Character("Anadélys", "Tu sais la pote que tu perds tout le temps car elle part en quête secondaire pendant la soirée, c'est elle !", salle_latino, ["Tu cherches à pimenter ta soirée ? J'ai ce qu'il te faut...", "Attention à ne pas te perdre dans la danse, ou tu pourrais finir comme moi, coincé ici pour l'éternité !", "Un conseil d'ami : ne sous-estime jamais le pouvoir d'une bonne salsa pour charmer la foule."])
        }
        salle_rap.characters = {
            "DJ_rap": Character("DJ_Rap", "Le DJ qui fait vibrer la salle avec les meilleurs sons rap US et FR.", salle_rap, ["Yo, t'as déjà entendu le dernier son de Niska ? Ça déchire !", "Le rap, c'est pas juste de la musique, c'est une culture.", "Si tu veux que je te chauffe le public, faut que tu sois à fond dans le délire."])
        }
        salle_techno.characters = {
            "DJ_techno": Character("DJ", "Le maître des platines, toujours à la recherche de nouvelles vibes pour faire bouger la foule.", salle_techno, ["Hey, t'as vu mon casque ? Je peux pas mixer sans lui !", "La musique, c'est la vie. Sans elle, je suis perdu.", "Si tu trouves mon casque, je te serai éternellement reconnaissant."])
        }
        rooftop.characters = {
            "Daniel_le_farfadet_malicieux": Character("Daniel", "Un petit être espiègle qui aime jouer des tours aux fêtards imprudents.", rooftop, ["Tu cherches à pimenter ta soirée ? J'ai ce qu'il te faut...", "Attention à ne pas te perdre dans la danse, ou tu pourrais finir comme moi, coincé ici pour l'éternité !", "Un conseil d'ami : ne sous-estime jamais le pouvoir d'une bonne salsa pour charmer la foule."])
        }
        secret_room.characters = {
            "Vigile": Character("Vigile", "Le gardien de la secret room, toujours à l'affût des intrus.", secret_room, ["Hé toi, tu cherches à entrer ici ? Montre-moi ce que t'as dans les poches.", "Seuls les plus méritants peuvent accéder à la secret room. Tu penses en faire partie ?", "Je ne laisse passer que ceux qui ont le pass carré VIP. T'en as un ?"])
        }




        

        
        

    # Setup player and starting room
    def _setup_player(self, player_name=None):
        """Initialize the player."""
        if player_name is None:
            player_name = input("\nEntrez votre nom: ")


        self.player = Player(player_name)
        self.player.current_room = self.rooms[0]  # exterieur

    # Setup quests
    def _setup_quests(self):
        """Initialize all quests."""
        # Quete principale
        main_quest = Quest(
        title="Survivre à la Nuit",
        description=(
            "Objectif : survivre jusqu'à la fermeture et entrer dans la salle VIP. "
            "Pas de drama, pas de sécurité, et surtout… assez de jetons."
        ),
        objectives=[
            "Obtenir pass VIP",
            "Obtenir le code de Daniel",
            "Avoir 3 jetons",
            "Ne pas se faire virer",
            "Visiter Secret Room"
        ],
        reward="Victoire : VIP avant fermeture 🥂"
    )

    # Petite quête secondaire 1 — Pass carré VIP
    pass_carre_VIP_quest = Quest(
        title="Chercher le pass carré VIP",
        description=(
            "Un client a perdu son pass d’accès au carré VIP. "
            "Si tu le retrouves, tu gagnes un jeton et tu pourras infiltrer la secret room."
        ),
        objectives=[
            "Visiter Rooftop",
            "Fouiller le sol",
            "Obtenir le pass carré VIP",
            "Retourner à secret room",
            "Donner le pass au vigile de la secret room"
        ],
        reward="+1 jeton"
    )

    # Petite quête 2 — DJ tête en l'air
    dj_quest = Quest(
        title="DJ tête en l'air",
        description=(
            "Le DJ a perdu son casque dans la soirée... il ne peut pas commencer son set. "
            "Si tu l'aides à le retrouver, il te devra une grosse ambiance."
        ),
        objectives=[
            "Parler au DJ",
            "Visiter le fumoir",
            "Récupérer le casque du DJ",
            "Le déposer à la salle techno"
        ],
        reward="+1 jeton"
    )

     # Petite quête 3 — Le cocktail Daniel
    cocktail_quest = Quest(
        title="Le cocktail Daniel",
        description=(
            "Tony le barman a créé un nouveau cocktail à l'éfigie du fameux Daniel. "
            "\nCependant, il n'a plus de sirop magique. Retrouve la bouteille de sirop pour lui, "
            "et il te préparera sa spécialité."
        ),
        objectives=[
            "Visiter la salle house",
            "Trouver la bouteille de sirop magique au vestiaire",
            "Déposer le sirop à la salle house."
        ],
        reward="+1 jeton"
    )

     # Petite quête 4 — Chauffeur de salle
    hype_quest = Quest(
        title="Chauffeur de Salle",
        description=(
            "Le DJ Rap cherche quelqu’un pour chauffer le public. "
            "Pour être l'heureux élu, tu dois avoir bu un sex on the beach au rooftoop..."
        ),
        objectives=[
            "Visiter le rooftop",
            "Boire un sex on the beach",
            "Retourner à la salle rap",
        ],
        reward="+1 jeton"
    )

    # Petite quête 5 — Retrouve ta pote Anadélys
    research_quest = Quest(
        title="Retrouve ta pote Anadélys",
        description=(
            "Anadélys a disparu dans la soirée. "
            "Trouve-la vite avant qu'elle ne soit dans une situation critique. "
            "Pour cela tu dois éviter qu'elle boive un mètre de shooter."
        ),
        objectives=[
            "Visiter la salle rap",
            "Prendre les 1 mètre de shooter",
            "Retrouver Anadélys",
        ],
        reward="+1 jeton"
    )  



    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message*
        if command_word == "":
            return None
        elif command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans L'Anarø CLUB !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())

def main():
    # Create a game object and play the game
    Game().play()

if __name__ == "__main__":
    main()