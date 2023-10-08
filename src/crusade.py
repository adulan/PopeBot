from math import log
import exceptions
from utils import get_member_from_cardinal_list


class Crusade:

    def __init__(self, name, attacking_city, defending_city):
        self.name = name
        self.attacking_city = attacking_city
        self.attacking_army = []
        self.attacking_funding = 0
        self.attacking_general = None

        self.defending_city = defending_city
        self.defending_army = []
        self.defending_funding = 0
        self.defending_general = None

    def get_attack_funding(self):
        return self.attacking_funding
    
    def add_attacking_soldier(self, cardinal):
        if get_member_from_cardinal_list(cardinal.member) is not None:
            self.attacking_army.append(cardinal)
        else:
            raise exceptions.MemberNotCardinal("You can't add a soldier that is not a cardinal.")
    
    def add_defending_soldier(self, cardinal):
        if get_member_from_cardinal_list(cardinal.member) is not None:
            self.defending_army.append(cardinal)
        else:
            raise exceptions.MemberNotCardinal("You can't add a soldier that is not a cardinal.")

    def set_attacking_general(self, cardinal):
        if cardinal in self.attacking_army:
            self.attacking_general = cardinal
        else:
            raise exceptions.CardinalNotDeployed("You can't set a general that is not deployed.")
        
    def set_defending_general(self, cardinal):
        if cardinal in self.defending_army:
            self.defending_general = cardinal
        else:
            raise exceptions.CardinalNotDeployed("You can't set a general that is not deployed.")

    def add_attacking_funding(self, cardinal, amount):
        if cardinal.pope_points < amount:
            raise exceptions.NotEnoughPopePoints("You don't have enough pope points to fund this crusade.")
        if cardinal in self.attacking_army:
            self.attacking_funding += amount
            cardinal.add_pope_points(-amount)
        else:
            if cardinal in self.defending_army:
                raise exceptions.CardinalAlreadyDeployed("You can't fund the enemy army.")
            else:
                self.add_attacking_soldier(cardinal)
                self.attacking_funding += amount
                cardinal.pope_points -= amount
            

    def add_defending_funding(self, cardinal, amount):
        if cardinal in self.defending_army:
            self.defending_funding += amount
        else:
            if cardinal in self.attacking_army:
                raise exceptions.CardinalAlreadyDeployed("You can't fund the enemy army.")
            else:
                self.add_defending_soldier(cardinal)
                self.defending_funding += amount


    def add_funds(self, city, cardinal, amount):
        if city == self.attacking_city:
            self.add_attacking_funding(cardinal, amount)
        elif city == self.defending_city:
            self.add_defending_funding(cardinal, amount)
        else:
            raise exceptions.CityNotInCrusade("You can't fund a city that is not in this crusade.")


    def attacking_army_size(self):
        return len(self.attacking_army)
    
    def defending_army_size(self):
        return len(self.defending_army)
    
    def attacking_army_strength(self):
        strength = 0
        for cardinal in self.attacking_army:
            strength += cardinal.popeliness() - cardinal.sin_coins
        strength += self.attacking_funding/self.attacking_army_size()

        return log(strength, 2)
    
    def defending_army_strength(self):
        strength = 0
        for cardinal in self.defending_army:
            strength += cardinal.popeliness() - cardinal.sin_coins
        strength += self.defending_funding/self.defending_army_size()

        return log(strength, 2)
    
    def soldier_is_deployed(self, cardinal):
        return cardinal in self.attacking_army or cardinal in self.defending_army
