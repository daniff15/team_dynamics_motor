from collections import deque
import os
import random
import math
import logging
from datetime import datetime
from Boss import Boss
from Logger import Logger

class TeamBattle:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.battle_queue = deque()

    def initialize_battle_queue(self):
        all_characters = self.team1.team + self.team2.team
        # Remove players when they are defeated
        all_characters = [character for character in all_characters if character.battle_hp > 0]
        characters = sorted(all_characters, key=lambda x: x.remaining_speed, reverse=True)
        self.battle_queue = deque(characters)
        return characters

    def check_battle_end(self, logger=None):
        # boss death or all players death
        if all(character.battle_hp <= 0 for character in self.team1.team):
            if logger:
                logger.log("Team 1 has been defeated! Game over!")
            return True
        elif all(character.battle_hp <= 0 for character in self.team2.team):
            if logger:
                logger.log("Team 2 has been defeated! Game over!")
            return True
        return False
    
    def attack_phase(self, attacker, target, logger=None):
        if attacker.battle_hp > 0:
            attacker.attack_enemy(target, logger)

    def run_battle(self):
        logger = Logger(log_folder="Log/TeamBattle")

        logger.log("Team 1:")
        for character in self.team1.team:
            logger.log(str(character))
        logger.log("Team 2:")
        for character in self.team2.team:
            logger.log(str(character))

        available_fighters = self.initialize_battle_queue()

        while not self.check_battle_end(logger):
            current_character = self.battle_queue[0]

            logger.log(f"Player's turn ({current_character.element}) - REMAINING SPEED {current_character.remaining_speed}.")

            possible_attacks = [player for player in available_fighters if current_character.team != player.team and player.battle_hp > 0]
            target = random.choice(possible_attacks)
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
        logger.log("-------------------------TEAM 1-----------------------------")
        for character in self.team1.team:
            logger.log(str(character))
        logger.log("-------------------------TEAM 2-----------------------------")
        for character in self.team2.team:
            logger.log(str(character))
        logger.log("------------------------------------------------------------")
        logger.close()
        self.restart_attributes()

    def restart_attributes(self):
        for character in self.team1.team + self.team2.team:
            character.battle_hp = math.ceil(character.hp * (1 + (character.level - 1) * 0.12))
            character.remaining_speed = character.speed
