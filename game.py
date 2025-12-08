# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.directions = set()
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        back = Command("back", " : pour revenir en arrière", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : pour observer ce que contient la pièce", Actions.look, 0)
        self.commands["look"] = look 
        take = Command("take", " <nom_objet> : pour prendre un objet dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <nom_objet> : pour déposer un objet de votre inventaire dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : pour vérifier le contenu de votre inventaire", Actions.check, 0)
        self.commands["check"] = check

        # Setup rooms — Boîte de nuit

        exterieur = Room(
            "Exterieur",
            "Le trottoir devant la boîte : gens qui fument, Uber en warning, "
            "et toi qui as peur de te faire recaler à l'entrée."    
        )
        
        self.rooms.append(exterieur)

        billetterie = Room(
            "Billetterie",
            "Petite file, vigile blasé, machine à CB qui fait plus de bruit que la sono. "
            "Tu pries pour que ta carte passe."
        )
        self.rooms.append(billetterie)

        vestiaire = Room(
            "Vestiaire",
            "Mega pile de manteaux, ticket froissé dans ta main, et la peur d’oublier "
            "le numéro à 3h du matin."
        )
        self.rooms.append(vestiaire)

        salle_techno = Room(
            "Salle Techno",
            "Stroboscopes, basses qui te font vibrer les organes, DJ qui ne sourit jamais "
            "mais tout le monde l’adore."
        )
        self.rooms.append(salle_techno)

        salle_rap = Room(
            "Salle Rap US / FR",
            "Ça crie les lyrics plus fort que le son, tout le monde "
            "fait semblant de connaître tous les couplets."
        )
        self.rooms.append(salle_rap)

        salle_house = Room(
            "Salle House",
            "Ambiance house, kicks propres, mélodies qui donnent envie de lever les bras "
            "même si tu sais pas danser. Les gens ici font genre qu'ils comprennent le mix."
        )
        self.rooms.append(salle_house)

        salle_latino = Room(
            "Salle Latino / Shatta",
            "Ambiance caliente, déhanchés sérieux, gens qui dansent trop bien pour que " 
            "tu restes fidèle. Tu hésites entre te laisser tenter ou fuir."
        )
        self.rooms.append(salle_latino)

        fumoir = Room(
            "Fumoir",
            "Aqua enfumée, discussions philosophiques à 2h du mat, "
            "et quelqu’un qui parle de lancer un start-up à chaque bouffée."
        )
        self.rooms.append(fumoir)

        secret_room = Room(
            "Secret Room",
            "Une petite salle cachée dont personne ne connaît vraiment la règle d’accès. "
            "Si tu es là, soit t’es VIP, soit tu t’es perdu."
        )
        self.rooms.append(secret_room)

        rooftop = Room(
            "Rooftop",
            "Vue sur la ville, guirlandes lumineuses, air frais qui sauve des coups de chaud. "
            "Endroit parfait pour pécho ton pain autour d'un verre de rosé."
        )
        self.rooms.append(rooftop)


        # Create inventory items in rooms
        vestiaire.inventory = {}

        # Create items
        ticket_vestiaire = Item("ticket_vestiaire", "Ton ticket du vestiaire, indispensable pour récupérer ton manteau plus tard.", 1)
        vestiaire.inventory ["ticket_vestiaire"] = ticket_vestiaire

        # Create exits for rooms
        exterieur.exits = {"N" : billetterie, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        billetterie.exits = {"N" : None, "E" : vestiaire, "S" : None, "O" : None, "U" : None, "D" : None}
        vestiaire.exits = {"N" : None, "E" : None, "S" : None, "O" : billetterie, "U" : salle_house, "D" : fumoir}
        salle_house.exits = {"N" : salle_techno, "E" : None, "S" : None, "O" : salle_latino, "U" : rooftop, "D" : vestiaire}
        salle_latino.exits = {"N" : salle_rap, "E" : salle_house, "S" : None, "O" : None, "U" : None, "D" : None}
        salle_rap.exits = {"N" : None, "E" : None, "S" : salle_latino, "O" : None, "U" : None, "D" : None}
        salle_techno.exits = {"N" : None, "E" : None, "S" : salle_house, "O" : None, "U" : None, "D" : None}
        rooftop.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : salle_house}
        fumoir.exits = {"N" : None, "E" : None, "S" : None, "O" : secret_room, "U" : vestiaire, "D" : None}
        secret_room.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}



        # Setup directions
        #print(self.rooms)
        for room in self.rooms :
            self.directions.update(room.exits.keys())
            #print(room.exits.keys())
            #print(room.name)

        #print(self.directions)

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = exterieur

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
        print(f"\nBienvenue {self.player.name} dans Le Anarø CLUB !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
