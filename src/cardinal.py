class Cardinal:
    pope_point_modifier = 1
    sin_coin_modifier = 2

    # init
    def __init__(self, member):
        self.member = member
        self.name = member.display_name
        self.id = member.id
        self.pope_points = 0
        self.sin_coins = 0


    # add pope points
    def add_pope_points(self, amount):
        self.pope_points += amount
        if self.pope_points > 4611686018427387903:
            self.pope_points = 1000000
            print(f"{self.name} pope points reset to 1000000")
        else:
            print(f"{self.name} received {amount} pope points")


    # add sin coins
    def add_sin_coins(self, amount):
        self.sin_coins += amount
        if self.sin_coins > 4611686018427387903:
            self.sin_coins = 1000000
            print(f"{self.name} sin coins reset to 1000000")
        else:
            print(f"{self.name} received {amount} sin coins")


    # calculate popliness
    def popeliness(self):
        return self.__class__.pope_point_modifier*self.pope_points - self.__class__.sin_coin_modifier*self.sin_coins
    

    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "pope_points": self.pope_points,
            "sin_coins": self.sin_coins
        }
    

    def from_json(self, json):
        self.name = json["name"]
        self.id = json["id"]
        self.pope_points = json["pope_points"]
        self.sin_coins = json["sin_coins"]
