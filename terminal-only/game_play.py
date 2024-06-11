from game_logic import GameLogic
import random
from names import names
from Input_Handling import Security
import os

def log(message):
    """
    Logs a message by printing it to the console.
    
    Args:
        message (str): The message to be logged.
    """
    return print(message)

def full_name():
    """
    Generates a full name by combining a first name and last name from the names list.
    
    Returns:
        str: A full name in the format "First Last".
    """
    first_name = random.choice(names).title()
    last_name = random.choice(names).title()
    return f"{first_name}, {last_name}"

def splash_screen():
    """
    Displays the welcome message for the game.
    """
    clear_terminal()
    log("Welcome to the game. This is the Money-Game.")
    log("The one with the most amount of money by the end of this wins.")

def clear_terminal():
    """
    Clears the terminal screen.
    """
    # Clear command for Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Clear command for Unix/Linux/MacOS
    else:
        _ = os.system('clear')

def new_line():
    return print("\n")

def new_window():
    return Security.sanitize_input(input("Press the [Enter Key] to continue..."))

class GamePlay:
    """
    Handles the gameplay mechanics, including player turns and actions.
    
    Attributes:
        players (list): A list of Player instances representing the players in the game.
        round_limit (int): The maximum number of rounds in the game.
    """

    TEN_MILLION_BANK_BALANCE = 10_000_000.00
  
    def __init__(self, players, round_limit, gamelogic):
        """
        Initializes the GamePlay class with a list of Player instances and a round limit.
        
        Args:
            players (list): A list of Player instances.
            round_limit (int): The maximum number of rounds in the game.
        """
        self.players = players
        self.round_limit = round_limit
        self.gamelogic = gamelogic

    def format_player_banks(self):
        """
        Formats the bank balances of all players.
        """
        self.gamelogic.check_bank_modifications(self.players)

    def start_game(self):
        """
        Starts the game with a turn-based system.
        """
        log("Starting the game!")
        self.rounds = 0
        
        while self.rounds < self.round_limit:
            for player in self.players:
                self.player_turn(player)
            self.rounds += 1
            log(f"Round {self.rounds} completed.")
            if self.rounds == self.round_limit:
                self.check_game_end()
            else:
                log(f"Proceeding to Round {self.rounds + 1}.")

    def print_player_options(self, player):
        """
        Prints the options available to a player during their turn using a dictionary.
        
        Args:
            player (Player): The Player instance whose turn it is.
        """
        options = {
            0: "Player Description",
            1: "Work",
            2: "Steal",
            3: "Search",
            4: "Use Item",
            5: "End Turn"
        }

        new_line()
        log(f"It's Player #{player.id}'s turn.")
        log("Options:")
        for key, value in options.items():
            log(f"  {key}. {value}")
    
    def player_turn(self, player):
        """
        Manages a player's turn in the game.
        
        Args:
            player (Player): The Player instance whose turn it is.
        """
        turn = 0
        
        while True:
            
            if turn >= 5:
                log(f"Player #{player.id} turn has ended.")
                new_window()
                clear_terminal()
                turn = 0
                break

            self.print_player_options(player)

            player_actions = input(f"Choose your action, Player #{player.id}: ").lower()

            if player_actions in ["0", "despriction", "player despriction", "d"]:
                self.gamelogic.view_other_player_profiles(self.players)

            elif player_actions in ["1", "work", "w"]:
                new_line()
                self.gamelogic.work(player)
                turn += 4
                new_window()
                clear_terminal()

            elif player_actions == "2":
                self.gamelogic.steal(player, self.players)
                turn += 1
                new_window()
                clear_terminal()

            elif player_actions == "3":
                new_line()
                self.gamelogic.search(player)
                turn += 6
                new_window()
                clear_terminal()

            elif player_actions == "4":
                self.use_item(player)

            elif player_actions == "5":
                new_line()
                log(f"Player #{player.id} turn has voted to end their turn.")
                new_window()
                clear_terminal()
                break

            else:
                log("Invalid action. Choose between 0 and 5.")
    
    def check_game_end(self):
        """
        Checks if the game has reached the end of the rounds and determines the winner.
        """
        if self.rounds == self.round_limit:
            self.rank_players()
            self.check_achievements()
            self.announce_winner()
    
    def rank_players(self):
        """
        Ranks the players based on their bank balances.
        """
        self.players.sort(key=lambda p: self.gamelogic.deformat_currency(p.bank), reverse=True)

    def check_achievements(self):
        """
        Checks if any player has reached the target bank balance and logs this achievement.
        """
        for player in self.players:
            if self.gamelogic.deformat_currency(player.bank) >= self.TEN_MILLION_BANK_BALANCE:
                log(f"Achievement unlocked! {player.name} has reached a bank balance of {self.gamelogic.format_currency(player.bank)}.")

    def announce_winner(self):
        """
        Announces the winner and displays the final rankings.
        """
        log("Game Over!")
        log(f"In the {self.round_limit} rounds we had, this is the list of the winners.")
        new_line()
        log("Final Rankings:")
        for rank, player in enumerate(self.players, start=1):
            log(f"\t{rank}. {player.name} - Bank Balance: {self.gamelogic.format_currency(player.bank)}")
        new_line()
        log(f"The winner is {self.players[0].name} with a bank balance of {self.gamelogic.format_currency(self.players[0].bank)}!")
