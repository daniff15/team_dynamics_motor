import math
import random
from Character import Character

class Player(Character):
    SPEED_NEEDED = 5

    def __init__(self, id, element, hp, attack, defense, speed, strength, weakness, extra_points=0, xp=0, level=1, team=None):
        super().__init__(id, element, hp, attack, defense, speed, strength, weakness, extra_points, xp, level, team)
    
    def __str__(self):
        return super().__str__()

    def add_xp(self, xp):
        # XP NEEDS TO BE MULTIPLE OF 5
        if xp % 5 == 0:
            if self.level < self.MAX_LEVEL and xp <= self.MAX_XP:
                self.xp += xp
                self.check_level_up()
            else: 
                print("Invalid XP amount or REACHED MAX LEVEL. Please enter a number between 0 and 1000.")
        else:
            print("Invalid XP amount. Please enter a number that is a multiple of 5.")

    def check_level_up(self):
        if self.level < self.MAX_LEVEL:
            xp_needed = self.calculate_xp_needed()
            
            if self.xp >= xp_needed:
                self.level += 1
                self.xp -= xp_needed
                self.update_stats()
                
                # # Generate extra points with a 30% probability
                # if random.random() < 0.3:
                #     self.extra_points += 1
                
                self.check_level_up()

    def calculate_xp_needed(self):
        if self.level < self.MAX_FIRST_FORMULA_LEVEL:
            xp_needed = self.BASE_XP + ((self.level - 1) * self.INCREMENT)
        else:
            #xp_needed = self.BASE_XP + ((self.MAX_FIRST_FORMULA_LEVEL - 1) * self.INCREMENT) + ((self.level - self.MAX_FIRST_FORMULA_LEVEL) * self.INCREMENT * 2)
            xp_needed = 500
        
        return xp_needed

    def update_stats(self, scaling_factor=0.11):
        old_hp = self.hp
        self.hp += math.ceil(self.hp * scaling_factor * random.uniform(1, 1.1))

        # Update battle_hp based on the current hp value
        self.battle_hp = math.ceil(self.hp * (1 + (self.level - 1) * 0.12))

        self.attack += math.ceil(self.attack * scaling_factor * random.uniform(1, 1.1))
        self.defense += math.ceil(self.defense * scaling_factor * random.uniform(1, 1.1))
        self.speed += math.ceil(self.speed * scaling_factor * random.uniform(1, 1.1))

    def level_up_to_n(self, n):
        if self.level < n:
            self.level_up()
            self.level_up_to_n(n)

    def level_up(self):
        self.level += 1
        self.update_stats()
        
        # Generate extra points with a 30% probability
        if random.random() < 0.25:
            self.extra_points += 1

    def add_extra_points_to_stat(self, stat, points):
        print(f"Available points to assign: {self.extra_points}")
        if self.extra_points >= points and points > 0:
            if stat == "hp":
                self.hp += points
            elif stat == "atk":
                self.attack += points
            elif stat == "def":
                self.defense += points
            elif stat == "spd":
                self.speed += points
            self.extra_points -= points

            print(f"{points} points assigned to {stat.upper()}. Remaining points: {self.extra_points}")
        else:
            print("Not enough extra points.")

    # def add_extra_points_to_stat(self, stat, points): 
    #     #This function is gonna be used to a demonstration so it needs to be able to always add the number of points
    #     #to the stat, even if the number of points is bigger than the extra_points available.
    #     if stat == "hp":
    #         self.hp += points
    #     elif stat == "atk":
    #         self.attack += points
    #     elif stat == "def":
    #         self.defense += points
    #     elif stat == "spd":
    #         self.speed += points