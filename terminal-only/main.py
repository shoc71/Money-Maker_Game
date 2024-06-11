import sys
from Important_Programs.game_logic import GameLogic
from Important_Programs.player_setup import Startup
from Important_Programs.game_play import GamePlay
from Important_Programs.Input_Handling import Security
from Important_Programs.ulits import splash_screen

def main():
    sys.path.append("Important_Programs")
    gamelogic = GameLogic()
    security = Security()
    startup = Startup(gamelogic, security)
    splash_screen()
    players, round_limit = startup.start_setup()
    gameplay = GamePlay(players, round_limit, gamelogic)
    gameplay.start_game()
    gameplay.format_player_banks()  # Format player banks after the game ends

def restart_game():
    while True:
        main()
        restart = Security.sanitize_input(input("Do you want to restart the game? (yes/no): ").lower())
        if restart not in ['yes', 'y', '1']:
            break

# In the main block:
if __name__ == "__main__":
    restart_game()