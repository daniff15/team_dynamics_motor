from Element import Element
from Player import Player

class Team:
    def __init__(self, team=None):
        self.team = team if team is not None else []

    def display_team(self):
        for player in self.team:
            print(player)

    def display_team_indexes(self):
        for i, player in enumerate(self.team):
            print(f"{i} - {player.element}")

    def display_available_extra_points(self):
        for i, player in enumerate(self.team):
            print(f"{i} - {player.element} - Extra Points: {player.extra_points}")

    # this method allows to be used in the main file has team[index] instead of team.team[index]
    def __getitem__(self, index):
        return self.team[index]

    @classmethod
    def build_team(cls):
        while True:
            team = []
            # Choose between default or custom elements
            option = input("Enter 'D' for default elements or 'C' for custom elements: ").upper()

            if option == 'D':
                default_elements = ["WATER", "FIRE", "AIR", "EARTH"]

                for element in default_elements:
                    type_player = Element.get_element_from_string(element)
                    hp, atk, defense, speed = Element.get_element_stats(type_player)
                    strength = Element.get_strength(type_player)
                    weakness = Element.get_weakness(type_player)

                    player = Player(len(team), type_player, hp, atk, defense, speed, strength, weakness)

                    # CHEATS
                    #player.level_up_to_n_items(14)
                    team.append(player)
                
                break

            elif option == 'C':
                while len(team) < 4:
                    # element picker
                    element = input("Enter element for player: ")
                    type_player = Element.get_element_from_string(element)

                    if type_player is None:
                        print(f"{element} is not a valid element. Please enter a valid element.")
                        continue

                    hp, atk, defense, speed = Element.get_element_stats(type_player)
                    strength = Element.get_strength(type_player)
                    weakness = Element.get_weakness(type_player)

                    player = Player(len(team), type_player, hp, atk, defense, speed, strength, weakness)

                    # CHEATS
                    #player.level_up_to_n_items(14)
                    team.append(player)
                
                break

            else:
                print("Invalid option. Please enter 'D' or 'C.'")

        return cls(team)

    def __str__(self):
        return "\n".join(str(player) for player in self.team)
