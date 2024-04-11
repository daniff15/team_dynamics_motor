import math
from Character import Character

class Boss(Character):
    SPEED_NEEDED = 5

    def __init__(self, id, element, hp, attack, defense, speed, strength, weakness, level=5):
        super().__init__(id, element, hp, attack, defense, speed, strength, weakness, level=level)
        self.battle_hp = self.calculate_battle_hp()

    def calculate_battle_hp(self):
        return math.ceil(self.hp * (1 + (self.level - 1) * 0.12))

    def __str__(self):
        return f"({self.id}) Boss - {self.element} (Level {self.level}) - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, Speed: {self.speed} - XP: {self.xp} - Strength: {self.strength}, Weakness: {self.weakness}, Battle HP: {self.battle_hp}"
