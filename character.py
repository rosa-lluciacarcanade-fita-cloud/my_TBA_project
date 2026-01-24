"""Module defining the Character class for non-player characters (NPCs) in the game."""
import random

class Character:
    """
    Docstring pour Character
    """
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.inventory = {}

    def __str__(self):
        """Return a string representation of the character."""
        return f"{self.name} : {self.description}"

    #PROBLEME le PNJ peut avoir current_room = nouvelle salle mais rester listé
    # dans old_room.characters, d'où le message "n'est pas présent" quand on
    # cherche le PNJ dans la salle.
    def move(self):
        """Déplace le PNJ de manière aléatoire dans une des salles adjacentes."""
        from game import DEBUG
        # Decision de se déplacer ou non
        if not random.choice([True, False]):
            return False

        # Deplacement du PNJ
        exits = [room for room in self.current_room.exits.values()
                 if room is not None]
        # Si aucune sortie où aller
        if not exits:
            return False

        next_room = random.choice(exits)

        # Si la salle choisie est la même (au cas où), on considère que le PNJ n'a pas bougé
        if next_room is self.current_room:
            return False

        # Mettre à jour la salle actuelle du PNJ

        self.current_room.remove_characters(self)
        next_room.add_characters(self)

        self.current_room = next_room

        if DEBUG:
            print(f"DEBUG : {self.name} se déplace vers {self.current_room.name}.")
        return True

    def get_msg(self):
        """Affiche un message du PNJ de manière cyclique."""
        # Si la liste des messages est vide
        if not self.msgs:
            return None
        msg = self.msgs.pop(0)
        print(f"\n{msg}\n")
        # Remettre le message à la fin pour un affichage cyclique
        self.msgs.append(msg)
        return True
