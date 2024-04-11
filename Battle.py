from collections import deque
import os
import random
import math
import logging
from datetime import datetime
from Boss import Boss
from Logger import Logger

class Battle:
    def __init__(self, team, boss):
        self.team = team
        self.boss = boss
        self.battle_queue = deque()

    def initialize_battle_queue(self):
        all_characters = self.team.team + [self.boss]
        # Remove players when they are defeated
        all_characters = [character for character in all_characters if character.battle_hp > 0]
        characters = sorted(all_characters, key=lambda x: x.remaining_speed, reverse=True)
        self.battle_queue = deque(characters)
        return characters

    def check_battle_end(self, logger=None):
        # boss death or all players death
        if self.boss.battle_hp <= 0:
            if logger:
                logger.log("Boss has been defeated! Congratulations!")
                print("--------------------")
                print("Boss has been defeated! Congratulations!")
            return True
        elif all(character.battle_hp <= 0 for character in self.team):
            if logger:
                logger.log("All players have been defeated! Game over!")
                print("--------------------")
                print("All players have been defeated! Game over!")
            return True
        return False
    
    def attack_phase(self, attacker, target, logger=None):
        if attacker.battle_hp > 0:
            attacker.attack_enemy(target, logger)
            if target.battle_hp <= 0:
                if isinstance(target, Boss):
                    if logger:
                        logger.log(f"Boss ({target.element}) player has been defeated!")
                else:
                    if logger:
                        logger.log(f"{target.element} player has been defeated!")

    def run_battle(self):
        logger = Logger()
        for character in self.team.team:
            logger.log(str(character))
        logger.log(str(self.boss))
        available_fighters = self.initialize_battle_queue()

        while not self.check_battle_end(logger):
            current_character = self.battle_queue[0]

            if isinstance(current_character, Boss):
                logger.log(f"Boss's turn ({current_character.element}) - REMAINING SPEED {current_character.remaining_speed}.")
                possible_attacks = [player for player in available_fighters if not isinstance(player, Boss)]
                target = random.choice(possible_attacks)
                logger.log(f"Boss {current_character.element} attacked {target.element} player.")
                self.attack_phase(current_character, target, logger)
            else:
                logger.log(f"Player's turn ({current_character.element}) - REMAINING SPEED {current_character.remaining_speed}.")
                target = self.boss
                self.attack_phase(current_character, target, logger)

            # Remove the current character from the queue
            self.battle_queue.popleft()

            # Check if the queue is empty, indicating that all characters have completed their turns
            if not self.battle_queue:
                # Reinitialize the battle queue
                available_fighters = self.initialize_battle_queue()

        logger.log("Battle has finished.")
        logger.log("------------------------------------------------------------")
        logger.log("Team current status:")
        for character in self.team.team:
            logger.log(str(character))
        logger.log("------------------------------------------------------------")
        logger.close()
        self.restart_attributes()

    def calculate_probability_of_winning(team, boss):
        # Simulate 1000 battles
        wins = 0
        for _ in range(1000):
            battle = Battle(team, boss)
            win = battle.simulate_battle()
            if win:
                wins += 1
            battle.restart_attributes()
        return (wins / 1000)

    def restart_attributes(self):
        for character in self.team.team:
            character.battle_hp = math.ceil(character.hp * (1 + (character.level - 1) * 0.12))
            character.remaining_speed = character.speed
        self.boss.battle_hp = math.ceil(self.boss.hp * (1 + (self.boss.level - 1) * 0.12))
        self.boss.remaining_speed = self.boss.speed

    def simulate_battle(self):
        available_fighters = self.initialize_battle_queue()

        while not self.check_battle_end():
            current_character = self.battle_queue[0]

            if isinstance(current_character, Boss):
                possible_attacks = [player for player in available_fighters if not isinstance(player, Boss)]
                target = random.choice(possible_attacks)
                self.attack_phase(current_character, target)
            else:
                target = self.boss
                self.attack_phase(current_character, target)

            # Remove the current character from the queue
            self.battle_queue.popleft()

            # Check if the queue is empty, indicating that all characters have completed their turns
            if not self.battle_queue:
                # Reinitialize the battle queue
                available_fighters = self.initialize_battle_queue()
        return self.boss.battle_hp <= 0
