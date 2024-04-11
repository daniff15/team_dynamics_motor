from Player import Player
from Team import Team
from Element import Element
from Boss import Boss
from BossBattle import BossBattle
from TeamBattle import TeamBattle

def create_team(id):
    team = Team(id)
    team.build_team()
    return team

def check_player_index(team, index):
    if index < 0 or index >= len(team.team):
        print(f"Invalid index. Please enter a number between 0 and {len(team.team) - 1}.")
        return False
    return True

def check_stat_to_increase(stat):
    if stat not in ["hp", "atk", "def", "spd"]:
        print("Invalid stat. Please enter a valid stat (HP/ATK/DEF/SPD).")
        return False
    return True

def main():
    teams = []

    while True:
        print("=== Menu ===")
        print("1. Create a New Team")
        print("2. Display Teams Stats")
        print("3. Add XP to a Player")
        print("4. Level up a Player")
        print("5. Assign Extra Points to a Player")
        print("6. Battle Simulator (Boss Battle)")
        print("7. Battle Simulator (Teams Battle)")
        print("8. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7): ")

        if choice == "1":
            team = create_team(len(teams))
            teams.append(team)
        elif choice == "2":
            if not teams:
                print("No teams created yet. Please create a team first.")
                continue
            for team in teams:
                team.display_team()
                print("\n")
        elif choice == "3":
            if not teams:
                print("No teams created yet. Please create a team first.")
                continue
        
            team_index = int(input("Enter team index (0 to {}): ".format(len(teams) - 1)))
            team = teams[team_index]
            team.display_team_indexes()
            player_index = int(input("Enter player index (0 to {}): ".format(len(team.team) - 1)))
            if not check_player_index(team, player_index):
                continue
            xp_amount = int(input("Enter the XP amount to add to the player: "))
            team[player_index].add_xp(xp_amount)
            print(f"{team[player_index].element} player gained {xp_amount} XP.")
        elif choice == "4":
            if not teams:
                print("No teams created yet. Please create a team first.")
                continue

            team_index = int(input("Enter team index (0 to {}): ".format(len(teams) - 1)))
            team = teams[team_index]
            team.display_team_indexes()
            player_index = int(input("Enter player index (0 to {}): ".format(len(team.team) - 1)))
            if not check_player_index(team, player_index):
                continue
            level_amount = int(input("Enter the level that the player should have: "))
            team[player_index].level_up_to_n_items(level_amount)
            print(f"{team[player_index].element} player leveled up.")

        elif choice == "5":
            if not teams:
                print("No teams created yet. Please create a team first.")
                continue

            team_index = int(input("Enter team index (0 to {}): ".format(len(teams) - 1)))
            team = teams[team_index]

            team.display_available_extra_points()
            player_index = int(input("Enter player index (0 to {}): ".format(len(team.team) - 1)))
            if not check_player_index(team, player_index):
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


        elif choice == "6":
            if not teams:
                print("No teams created yet. Please create a team first.")
                continue

            team_index = int(input("Enter team index (0 to {}): ".format(len(teams) - 1)))
            team = teams[team_index]

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
                    BossBattle.calculate_probability_of_winning(team, boss1),
                    BossBattle.calculate_probability_of_winning(team, boss2),
                    BossBattle.calculate_probability_of_winning(team, boss3),
                    BossBattle.calculate_probability_of_winning(team, boss4)
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
                battle = BossBattle(team, boss_to_fight)
                battle.run_battle()

        elif choice == "7":
            if len(teams) < 2:
                print("You need at least 2 teams to battle.")
                continue

            team1_index = int(input("Enter team 1 index (0 to {}): ".format(len(teams) - 1)))
            team2_index = int(input("Enter team 2 index (0 to {}): ".format(len(teams) - 1)))
            while team1_index == team2_index:
                print("Team indexes must be different.")
                team2_index = int(input("Enter team 2 index (0 to {}): ".format(len(teams) - 1)))

            if not check_player_index(teams[team1_index], 0) or not check_player_index(teams[team2_index], 0):
                continue

            battle = TeamBattle(teams[team1_index], teams[team2_index])
            battle.run_battle()

        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
