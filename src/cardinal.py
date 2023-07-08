class Cardinal:
    pope_point_modifier = 1
    sin_coin_modifier = 2

    # init
    def __init__(self, member):
        self.member = member
        self.name = member.name
        self.id = member.id
        self.pope_points = 0
        self.sin_coins = 0

    # add pope points
    def add_pope_points(self, amount):
        self.pope_points += amount
        print(f"{self.name} received {amount} pope points")

    # add sin coins
    def add_sin_coins(self, amount):
        self.sin_coins += amount
        print(f"{self.name} received {amount} sin coins")

    # calculate popliness
    def popeliness(self):
        return self.__class__.pope_point_modifier*self.pope_points - self.__class__.sin_coin_modifier*self.sin_coins