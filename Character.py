import math
import random

class Character:
    BASE_XP = 100
    INCREMENT = 50
    MAX_FIRST_FORMULA_LEVEL = 9
    MAX_LEVEL = 20
    MAX_XP = 1000
    CRITICAL_HIT_PROBABILITY = 0.1
    MIN_DAMAGE_THRESHOLD = 1

    def __init__(self, id, element, hp, attack, defense, speed, strength, weakness, extra_points=0, xp=0, level=1, team=None):
        self.id = id
        self.element = element
        self.hp = hp
        self.battle_hp = self.hp * (1 + (level - 1) * 0.12)
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.remaining_speed = speed
        self.extra_points = extra_points
        self.strength = strength
        self.weakness = weakness
        self.xp = xp
        self.level = level
        self.team = team

    def __str__(self):
        return f"({self.id}) {self.element} (Level {self.level}) - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, Speed: {self.speed} - XP: {self.xp} - Strength: {self.strength}, Weakness: {self.weakness} - Extra Points: {self.extra_points} - Battle HP: {self.battle_hp}, Team: {self.team}"

    def update_remaining_speed(self):
        if self.remaining_speed < self.SPEED_NEEDED and self.remaining_speed > 0:
            self.remaining_speed = 0
        elif self.remaining_speed == 0:
            self.remaining_speed = self.speed
        else:
            self.remaining_speed -= self.SPEED_NEEDED

    def attack_enemy(self, enemy, logger=None):
        self.update_remaining_speed()
        damage = self.calculate_damage(enemy, logger)
        enemy.battle_hp -= damage
        if logger:
            logger.log(f"{self.__class__.__name__}-{self.element} player attacked {enemy.__class__.__name__}-{enemy.element} for {damage} damage.")
            logger.log(f"{enemy.__class__.__name__}-{enemy.element} player has {enemy.battle_hp} HP remaining.")

    def calculate_damage(self, enemy, logger=None):
        base_damage = (self.attack * self.attack) / (self.attack + enemy.defense)

        # Critical hit check
        if random.random() < self.CRITICAL_HIT_PROBABILITY:
            if logger:
                logger.log(f"Critical hit! {self.element} player dealt more damage.")
            base_damage *= 1.5

        damage_modifier = 1.0 
        if self.element == enemy.weakness:
            if logger:
                logger.log(f"{self.element} player has the advantage over {enemy.element} player.")
            damage_modifier = 1.5 
        elif self.element == enemy.strength:
            if logger:
                logger.log(f"{self.element} player is at a disadvantage against {enemy.element} player.")
            damage_modifier = 0.5  

        total_damage = int((base_damage * damage_modifier) * (random.randint(240, 255)/255))
        return total_damage

    def type_multiplier(self, boss):
        if self.element == boss.weakness:
            return 1.5
        elif self.element == boss.strength:
            return 0.5
        else:
            return 1