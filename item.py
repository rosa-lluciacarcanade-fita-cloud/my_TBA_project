"""Module containing the Item class for game items."""


class Item:  # pylint: disable=too-few-public-methods
    """Represents an item in the game.

    An item has a name, description, and weight.

    Attributes:
        name (str): The name of the item.
        description (str): A description of the item.
        weight (float): The weight of the item in kilograms.

    Methods:
        __init__(self, name, description, weight): The constructor.
        __str__(self): The string representation of the item.

    Examples:

    >>> item = Item("Épée", "Une épée en acier", 2.5)
    >>> item.name
    'Épée'
    >>> item.description
    'Une épée en acier'
    >>> item.weight
    2.5
    >>> str(item)
    'Épée : Une épée en acier (2.5 kg)'

    """

    def __init__(self, name, description, weight):
        """Initialize an item.

        Args:
            name (str): The name of the item.
            description (str): A description of the item.
            weight (float): The weight of the item in kilograms.
        """
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"
