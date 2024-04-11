from Player import Player
from Team import Team
from Element import Element
from Boss import Boss
from Battle import Battle

def main():

    team = Team()
    team = team.build_team()

    def check_player_index(index):
        if index < 0 or index >= len(team.team):
            print(f"Invalid index. Please enter a number between 0 and {len(team.team) - 1}.")
            return False
        return True

    def check_stat_to_increase(stat):
        if stat not in ["hp", "atk", "def", "spd"]:
            print("Invalid stat. Please enter a valid stat (HP/ATK/DEF/SPD).")
            return False
        return True

    while True:
        print("\n=== Menu ===")
        print("1. Display Team Stats")
        print("2. Add XP to a Player")
        print("3. Level up a Player")
        print("4. Assign Extra Points to a Player")
        print("5. Battle Simulator")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == "1":
            team.display_team()
        elif choice == "2":
            team.display_team_indexes()
            player_index = int(input("Enter player index (0 to {}): ".format(len(team.team) - 1)))
            if not check_player_index(player_index):
                continue
            xp_amount = int(input("Enter XP amount to add: "))
            team[player_index].add_xp(xp_amount)
            print(f"XP added to the {team[player_index].element} player.")
        elif choice == "3":
            team.display_team_indexes()
            player_index = int(input("Enter player index (0 to {}): ".format(len(team.team) - 1)))
            if not check_player_index(player_index):
                continue
            level_amount = int(input("Enter the level that the player should have: "))
            team[player_index].level_up_to_n_items(level_amount)
            print(f"{team[player_index].element} player leveled up.")
        elif choice == "4":
            team.display_available_extra_points()
            player_index = int(input("Enter player index (0 to {}): ".format(len(team.team) - 1)))
            if not check_player_index(player_index):
                continue
            extra_points = team[player_index].extra_points

            if extra_points > 0:
                stat_to_increase = input("Enter the stat to increase (HP/ATK/DEF/SPD): ")
                if not check_stat_to_increase(stat_to_increase):
                    continue
                else:
                    points_to_assign = int(input(f"Enter the number of extra points to assign (Available: {team[player_index].extra_points}): "))
                    team[player_index].add_extra_points_to_stat(stat_to_increase.lower(), points_to_assign)
            else:
                print(f"{team[player_index].element} player has no extra points to assign.")



        elif choice == "5":
            def print_battle_menu_with_probabilities(probs):
                bosses = [
                    "AIR Boss (Level 5)",
                    "EARTH Boss (Level 10)",
                    "WATER Boss (Level 15)",
                    "FIRE Boss (Level 20)"
                ]

                print("\n=== Battle Monster Menu ===")

                for i, boss in enumerate(bosses):
                    probability = probs[i]
                    color_code = get_color_code(probability)

                    print(f"{i+1}. {boss} - Win Probability: {probability:.2%} {color_code}●\033[0m", end="\n")

                print("0. Exit")


            def get_color_code(probability):
                r = int(255 * (1 - probability))
                g = int(255 * probability)
                b = 0

                # ANSI escape code for setting text color
                color_code = f"\033[38;2;{r};{g};{b}m"

                return color_code


            def choose_boss_to_fight():
                probability_win_bosses = [
                    Battle.calculate_probability_of_winning(team, boss1),
                    Battle.calculate_probability_of_winning(team, boss2),
                    Battle.calculate_probability_of_winning(team, boss3),
                    Battle.calculate_probability_of_winning(team, boss4)
                ]

                print_battle_menu_with_probabilities(probability_win_bosses)

                monster_choice = input("Choose the monster to fight (1/2/3/4): ")

                if monster_choice.isdigit() and 1 <= int(monster_choice) <= 4:
                    return int(monster_choice)
                else:
                    print("Invalid monster choice. Please enter a valid option.")
                    return 0


            boss1 = Boss(1, Element.AIR, 65, 20, 20, 20, Element.EARTH, Element.FIRE, 5)
            boss2 = Boss(2, Element.EARTH, 200, 40, 40, 40, Element.WATER, Element.AIR, 10)
            boss3 = Boss(3, Element.WATER, 400, 60, 60, 60, Element.FIRE, Element.EARTH, 15)
            boss4 = Boss(4, Element.FIRE, 600, 135, 135, 135, Element.AIR, Element.WATER, 20)

            while True:
                monster_choice = choose_boss_to_fight()

                if monster_choice == 0:
                    break

                boss_to_fight = [boss1, boss2, boss3, boss4][monster_choice - 1]
                battle = Battle(team, boss_to_fight)
                battle.run_battle()

        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
