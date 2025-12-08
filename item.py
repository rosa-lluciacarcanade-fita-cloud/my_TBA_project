class Item :
    def __init__(self, name, description, weight):
        self.name = ""
        self.description = ""
        self.weight = 0

    def __str__(self):
        return f"{self.name} : {self.description} (poids: {self.weight} kg)"

     



    
