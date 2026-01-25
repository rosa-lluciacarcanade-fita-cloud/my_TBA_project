"""Game class"""

# Import modules
from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from quest import Quest
from character import Character

DEBUG = True
class Game:
    """Main class for the text-based adventure game."""

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.directions = set()
        self.characters = []

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
        "\nLe trottoir devant la boîte : gens qui fument, Uber en warning " \
        "\net toi qui as peur de te faire recaler à l'entrée."
        exterieur = Room("Exterieur", s, image="exterieur.png")

        s = "Billetterie " \
        "\nPetite file, videur blasé, machine à CB qui fait plus de bruit que la sono. " \
        "\nTu pries pour que ta carte passe."
        billetterie = Room("Billetterie", s, image="billetterie.png")

        s = "Vestiaire " \
        "\nMega pile de manteaux, ticket froissé dans ta main, et la peur d’oublier " \
        "\nle numéro à 3h du matin."
        vestiaire = Room("Vestiaire", s, image="vestiaire.png")

        s = "Salle Techno " \
        "\nStroboscopes, basses qui te font vibrer les organes, DJ qui ne sourit jamais " \
        "\nmais tout le monde l’adore."
        salle_techno = Room("Salle Techno", s, image="salle_techno.png")

        s = "Salle Rap US / FR " \
        "\nÇa crie les lyrics plus fort que le son, tout le monde " \
        "\nfait semblant de connaître tous les couplets."
        salle_rap = Room("Salle Rap US / FR", s, image="salle_rap.png")

        s = "Salle House " \
        "\nAmbiance house, kicks propres, mélodies qui donnent envie de lever les bras " \
        "\nmême si tu sais pas danser. Les gens ici font genre qu'ils comprennent le mix."
        salle_house = Room("Salle House", s, image="salle_house.png")

        s = "Salle Latino / Shatta " \
        "\nAmbiance caliente, déhanchés sérieux, gens qui dansent trop bien pour que " \
        "\ntu restes fidèle. Tu hésites entre te laisser tenter ou fuir."
        salle_latino = Room("Salle Latino / Shatta", s, image="salle_latino.png")

        s = "Fumoir " \
        "\nAqua enfumée, discussions philosophiques à 2h du mat, " \
        "\net quelqu’un qui parle de lancer un start-up à chaque bouffée." \
        "\nJuste a coté se cache la secret room, veux-tu t'y aventurer ? " \
        "\nSPOILER ALERTE : tu risques de ne jamais en ressortir si tu n'est pas un vrai membre..."
        fumoir = Room("Fumoir", s, image="fumoir.png")

        s = "Secret Room " \
        "\nUne petite salle cachée dont personne ne connaît vraiment la règle d’accès. " \
        "\nSi tu es là, soit t’es VIP, soit tu t’es perdu."
        secret_room = Room("Secret Room", s, image="secret_room.png")

        s = "Rooftop " \
        "\nVue sur la ville, guirlandes lumineuses, air frais qui sauve des coups de chaud. " \
        "\nEndroit parfait pour pécho ton pain autour d'un verre de rosé."
        rooftop = Room("Rooftop", s, image="rooftop.png")


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
        billetterie.inventory = {
            "note_du_videur": Item(
                "note_du_videur",
                "Un bout de papier froissé avec un code écrit dessus : '7429'. " +
                "Aucune idée à quoi ça sert, mais ça a l'air important...",
                1)
        }
        vestiaire.inventory = {
            "bouteille_de_sirop_magiques": Item(
                "bouteille_de_sirop_magiques",
                "Pour une soirée de farfadet où ton cerveau va alluciner.",
                1)
        }
        salle_house.inventory = {
            "mojito": Item(
                "mojito",
                "Un mojito plein de glace, deux feuilles de menthe fatiguées " +
                "et assez de sucre pour te faire croire que t’es encore sobre.",
                0)
        }
        salle_rap.inventory = {
            "un_mètre_de_shooter": Item(
                "un_mètre_de_shooter",
                "Un long shooter à partager, ou non. Ton foie va-t-il " +
                "résister ?",
                1)
        }
        salle_techno.inventory = {
            "lunette_stylé": Item(
                "lunette_stylé",
                "Des lunettes de gros BDG qui crie 'JE SUIS VIP' même si t'as une tête de touriste perdu. " +
                "Avec ça, t'es sûr de pécho plus facilement.",
                1)
        }
        salle_latino.inventory = {
            "ticket_vestiaire": Item(
                "ticket_vestiaire",
                "Un ticket de vestiaire un peu froissé avec le numéro 27 dessus. " +
                "Indispensable pour récupérer ton manteau plus tard.",
                1),
            "sex_on_the_beach": Item(
                "sex_on_the_beach",
                "Un cocktail sucré et coloré, parfait pour débuter " +
                "la soirée.",
                0),
        }
        rooftop.inventory = {
            "gin_tonic": Item(
                "gin_tonic",
                "Un gin tonic servi beaucoup trop fort. "
                "Tu dis ‘ça passe’, mais dans 20 minutes tu regretteras tout.",
                0),
            "pass_carré_VIP": Item(
                "pass_carré_VIP",
                "Essentiel pour accéder à la soirée de la secret room, " +
                "seulement pour les plus hots...",
                1)
        }
        fumoir.inventory = {
            "casque_DJ": Item(
                "casque_DJ",
                "Le casque de Rosa, sans lequel elle ne peut pas mixer.",
                1),
            "cigarette_de_luxe": Item(
                "cigarette_de_luxe",
                "Une cigarette de marque premium, un accessoire indispensable pour les VIP. " +
                "Ça fait classe dans une boîte de nuit.",
                1)
        }

        # Setup characters/PNJ
        salle_house.characters = [
            Character(
                "DJ_Rosita",
                "La reine des platines house, toujours prête à faire " +
                "danser la foule avec ses mixes enflammés.",
                salle_house,
                ["Salut toi ! Prêt à bouger sur mes beats ?",
                 "La house, c'est plus qu'un genre musical, c'est un " +
                 "mode de vie.",
                 "Si tu veux que je te prépare un set spécial, faut que " +
                 "tu me montres ton énergie sur le dancefloor."]),
        ]
        salle_latino.characters = [
            Character(
                "Anadélys",
                "Tu sais la pote que tu perds tout le temps car elle " +
                "part en quête secondaire pendant la soirée, c'est elle !",
                salle_latino,
                ["Elle est en pétard la soirée ! On va bien s'amuser !",
                 "Tu veux danser la salsa avec moi ? Allez, viens !",
                 "J'adore cette ambiance caliente, ça me donne envie de " +
                 "faire la fête toute la nuit !"]),
            Character(
                "Tony",
                "Le barman le plus cool de la boîte, toujours prêt à " +
                "te servir un cocktail avec le sourire.",
                salle_house,
                ["Qu'est-ce que je te sers ce soir ? J'ai des cocktails " +
                 "qui font danser même les plus timides !",
                 "Tu sais, la clé d'une bonne soirée, c'est un bon " +
                 "cocktail et une bonne compagnie.",
                 "Si tu cherches quelque chose de spécial, demande-moi, " +
                 "j'ai des recettes secrètes."])
        ]
        salle_rap.characters = [
            Character(
                "DJ_Rap",
                "Le DJ qui fait vibrer la salle avec les meilleurs " +
                "sons rap US et FR.",
                salle_rap,
                ["Yo, t'as déjà entendu le dernier son de Niska ? Ça " +
                 "déchire !",
                 "Le rap, c'est pas juste de la musique, c'est une " +
                 "culture.",
                 "Si tu veux que je te chauffe le public, faut que tu " +
                 "sois à fond dans le délire."])
        ]
        salle_techno.characters = [
            Character(
                "DJ",
                "Le maître des platines, toujours à la recherche de " +
                "nouvelles vibes pour faire bouger la foule.",
                salle_techno,
                ["Hey, t'as vu mon casque ? Je peux pas mixer sans lui !",
                 "La musique, c'est la vie. Sans elle, je suis perdu.",
                 "Si tu trouves mon casque, je te serai éternellement " +
                 "reconnaissant."])
        ]
        rooftop.characters = [
            Character(
                "Daniel",
                "Un petit être espiègle qui aime jouer des tours aux " +
                "fêtards imprudents.",
                rooftop,
                ["Tu cherches à pimenter ta soirée ? J'ai ce qu'il te " +
                 "faut...",
                 "Attention à ne pas te perdre dans la danse, ou tu " +
                 "pourrais finir comme moi, coincé ici pour l'éternité !",
                 "Un conseil d'ami : ne sous-estime jamais le pouvoir " +
                 "d'une bonne salsa pour charmer la foule."])
        ]
        fumoir.characters = [
            Character(
                "Secret_vigile",
                "Le gardien de la secret room, toujours à l'affût des " +
                "intrus.",
                fumoir,
                ["Hé toi, tu cherches à entrer ici ? Montre-moi ce que " +
                 "t'as dans les poches.",
                 "Seuls les plus méritants peuvent accéder à la secret " +
                 "room. Tu penses en faire partie ?",
                 "Je ne laisse passer que ceux qui ont le pass carré VIP. " +
                 "T'en as un ?"])
        ]
        vestiaire.characters = [
            Character(
                "Dora",
                "La dame du vestiaire, toujours prête à aider les " +  
                "clients à retrouver leurs affaires.",
                vestiaire,
                ["Pas de ticket pas de manteau !"],)  
        ]

        # Collect all characters into game.characters for movement
        for room in self.rooms:
            for character in room.characters:
                self.characters.append(character)

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
        Secret_room_quest = Quest(
            title="Secret Room",
            description=(
                "Infiltrer la secret room. Il faut avoir le bon look et les bons codes."
            ),
            objectives=[
                "prendre le pass_carré_VIP",
                "prendre la cigarette_de_luxe",
                "prendre lunette_stylé",
                "prendre le note_du_videur",
                "parler avec Secret_vigile",
                "Entrer dans la Secret Room"
            ],
            reward="Escroc Membre VIP"
        )

        Manteau_quest = Quest(
            title="Sauver le manteau",
            description=(
                "Mince j'ai perdu mon ticket de vestiaire ! Peux-tu m'aider à le retrouver ? " \
                "\nSinon je ne pourrais pas récupérer mon manteau en partant..."
            ),
            objectives=[
                "prendre le ticket_vestiaire",
                "Visiter Vestiaire",
                "parler avec Dora"
            ],
            reward="Manteau"
        )

        # Petite quête 2 — DJ Rosa
        Rosa_quest = Quest(
            title="DJ Rosa",
            description=(
                "Rosa a perdu son casque dans la soirée... elle ne peut pas commencer son set. "
                "Si tu l'aides à le retrouver, elle te devra une grosse ambiance."
            ),
            objectives=[
                "prendre le casque_DJ",
                "parler avec DJ_Rosita"
            ],
            reward="Titre de sauveur soirée house"
        )

        # Petite quête 3 — Le cocktail Daniel
        Cocktail_quest = Quest(
            title="Cocktail Daniel",
            description=(
                "Tony le barman a créé un nouveau cocktail à l'éfigie " +
                "du fameux Daniel le farfadet malicieux. " +
                "\nCependant, il n'a plus de sirop magique que Daniel lui avait donné. Retrouve " +
                "la bouteille de sirop pour lui, " +
                "et il te préparera sa spécialité."
            ),
            objectives=[
                "parler avec Daniel",
                "prendre la bouteille_de_sirop_magiques",
                "parler avec Tony"
            ],
            reward="Un nouveau bestie Daniel le farfadet + Le fameux cocktail Daniel"
        )

        # Petite quête 5 — Retrouve Anadélys
        Anadelys_quest = Quest(
            title="Retrouve Anadélys",
            description=(
                "Anadélys a disparu dans la soirée. "
                "Trouve-la vite avant qu'elle ne soit dans une situation critique. "
                "Pour cela tu dois éviter qu'elle boive un mètre de shooter."
            ),
            objectives=[
                "prendre un_mètre_de_shooter",
                "parler avec Anadélys",
            ],
            reward="Anadélys en pétard, vous allez bien vous amuser ensemble !"
        )

        # Add all quests to the player's quest manager
        self.player.quest_manager.add_quest(Manteau_quest)
        self.player.quest_manager.add_quest(Rosa_quest)
        self.player.quest_manager.add_quest(Anadelys_quest)
        self.player.quest_manager.add_quest(Cocktail_quest)
        self.player.quest_manager.add_quest(Secret_room_quest)

    # Check if the player has won the game
    def win(self):
        """
        Check if the player has won the game by completing all quests.

        Returns:
            bool: True if all quests are completed, False otherwise.
        """
        # Get all quests from the player's quest manager
        all_quests = self.player.quest_manager.quests

        for quest in all_quests:
            if quest.title == "Secret Room" and  quest.is_completed :
                print("\n🎉 FÉLICITATIONS! TU AS RÉUSSI À T'INFILTRER DANS LA SECRET ROOM !\n")
                return True
        
        # If there are no quests, the player cannot win
        if not all_quests:
            return False

        # Check if all quests are completed
        for quest in all_quests:
            if not quest.is_completed:
                return False

        # All quests are completed
        print("\n🎉 FÉLICITATIONS! TU AS COMPLÉTÉ TOUTES LES QUÊTES DU JEU !\n")
        return True

    # Check if the player has lost the game
    def lose(self):
        """
        Check if the player has lost the game due to specific conditions.

        Losing conditions:
        1. Entering the Secret Room without the "pass carré VIP" item
        2. Allowing Anadélys to drink the "1 mètre de shooter" (failing the rescue quest)
        3. Entering the Secret Room without completing the "Secret Room" quest
        4. Taking the "bouteille_de_sirop_magiques" before talking to Daniel
        5. Drinking too much .

        Returns:
            bool: True if the player has lost, False otherwise.
        """
        # Check if the player is in the Secret Room
        if self.player.current_room.name == "Secret Room":
            # Check if the player has the "pass carré VIP" item
            if "pass_carré_VIP" not in self.player.inventory:
                print("\n❌ GAME OVER! Tu n'avais pas le pass carré VIP " +
                      "pour accéder à la Secret Room!")
                print("Le vigile t'a jeté dehors comme une merde. C'est la fin de ta " +
                      "soirée...\n")
                return True
          

        # Check if Anadélys quest is active and if the player failed to save her
        for quest in self.player.quest_manager.quests:
            if quest.title == "Retrouve Anadélys" and quest.is_active:
                # If the objective "Prendre les 1 mètre de shooter" is completed but
                # "Retrouver Anadélys" is not, the player failed to save her in time
                if ("parler avec Anadélys" in quest.completed_objectives and
                    "prendre un_mètre_de_shooter" not in quest.completed_objectives):
                        print("\n❌ GAME OVER! Tu n'as pas sauvé Anadélys à temps!")
                        print("Elle a bu le mètre de shooter toute seule.")
                        print("C'est un désastre... Elle est complètement déchaînée maintenant.")
                        print("Depuis, elle danse non-stop : salsa, bachata, shatta… même quand la musique s’arrête.")
                        print("Elle a élu domicile dans la salle latino.")
                        print("Tu ne la feras jamais partir.")
                        print("Tu es coincé ici pour toujours avec elle.\n")
                        return True
                    
        # Check if you talk with Daniel before taking the bottle of sirop magique
        for quest in self.player.quest_manager.quests:
            if quest.title == "Cocktail Daniel" and quest.is_active:
                if ("prendre la bouteille_de_sirop_magiques" in quest.completed_objectives and
                    "parler avec Daniel" not in quest.completed_objectives):
                    print("\n❌ GAME OVER!")
                    print("Tu as pris le sirop magique sans parler à Daniel!")
                    print("Grave erreur!!")
                    print("Furieux, le farfadet hurle, siffle et claque des doigts.")
                    print("Une malédiction malicieuseeee s’abat sur toi.")
                    print("Désormais, tous les cocktails que tu bois ont un goût de jus de chaussette.")
                    print("Jamais tu connaîtras le fameux Cocktail Daniel de Tony.\n")
                    return True
        
        
        # Check if player's has drunk too much
        if self.player.drink_count >= 6:
            print("\n❌ GAME OVER!")
            print("Tu as trop bu, tes jambes ont décidé de quitter la soirée sans toi.")
            print("Tu t’effondres sur le dancefloor sous les regards gênés.")
            print("La sécurité arrive et te sort comme un sac de patates.")
            print("La soirée est finie. Ta dignité aussi...\n")
            return True

        # Player has not lost
        return False

    # Play the game
    def play(self):
        """Main game loop."""
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Check if the player has lost or won the game
            if self.lose() or self.win():
                self.finished = True
                break
            #Actions.move_pnj(self, [], 0)
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Process the command entered by the player."""

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word == "":
            return None
        elif command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez " +
                  "'help' pour voir la liste des commandes " +
                  "disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        """Print the welcome message at the start of the game."""
        print(f"\nBienvenue {self.player.name} dans L'Anarø CLUB !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())


##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("L'Anarø CLUB - Aventure Textuelle")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_monter = tk.PhotoImage(file=str(assets_dir / 'monter-arrow-50.png'))
        self._btn_descendre = tk.PhotoImage(file=str(assets_dir / 'descendre-arrow-50.png'))
        self._btn_back = tk.PhotoImage(file=str(assets_dir / 'back-50.png'))
        self._btn_look = tk.PhotoImage(file=str(assets_dir / 'look-50.png'))
        self._btn_check = tk.PhotoImage(file=str(assets_dir / 'check-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)

        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_monter,
                  command=lambda: self._send_command("go U"),
                  bd=0).grid(row=3, column=0)
        tk.Button(move_frame,
                  image=self._btn_descendre,
                  command=lambda: self._send_command("go D"),
                  bd=0).grid(row=3, column=1)

        # Back button
        tk.Button(buttons_frame,
                  text="Back",
                  command=lambda: self._send_command("back"),
                  bg="#444",
                  fg="#eee").grid(row=2, column=0, sticky="ew", pady=(2,2))

        # Look button
        tk.Button(buttons_frame,
                  text="Look",
                  command=lambda: self._send_command("look"),
                  bg="#444",
                  fg="#eee").grid(row=3, column=0, sticky="ew", pady=(2,2))

        # Check inventory button
        tk.Button(buttons_frame,
                  text="Check",
                  command=lambda: self._send_command("check"),
                  bg="#444",
                  fg="#eee").grid(row=4, column=0, sticky="ew", pady=(2,2))


        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=5, column=0, sticky="ew", pady=(2,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available (try PPM first, then PNG)
        if room.image:
            # Try PPM first (converted from PNG), then PNG
            ppm_path = assets_dir / room.image.replace('.png', '.ppm')
            if ppm_path.exists():
                image_path = ppm_path
            else:
                image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        # Check if the player has lost or won the game
        if self.game.lose() or self.game.win():
            self.game.finished = True
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except (tk.TclError, Exception) as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()


if __name__ == "__main__":
    main()
