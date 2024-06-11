import os
from Input_Handling import Security
from game_logic import GameLogic
from player_setup import Startup
from game_play import GamePlay

def splash_screen():
    """
    Displays the welcome message for the game.
    """
    # Clear command for Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Clear command for Unix/Linux/MacOS
    else:
        _ = os.system('clear')
    print("Welcome to the game. This is the Money-Game.")
    print("The one with the most amount of money by the end of this wins.")

def main():
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
        restart = input("Do you want to restart the game? (yes/no): ").lower()
        if restart not in ['yes', 'y', '1']:
            break

# In the main block:
if __name__ == "__main__":
    restart_game()