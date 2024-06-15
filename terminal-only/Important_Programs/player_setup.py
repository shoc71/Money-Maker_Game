import random
from .player import Player
from .ulits import log, clear_terminal, new_line
from .names import names
from .game_logic import BankManagement

def full_name():
    """
    Generates a full name by combining a first name and last name from the names list.
    
    Returns:
        str: A full name in the format "First Last".
    """
    first_name = random.choice(names).title()
    last_name = random.choice(names).title()
    return f"{first_name}, {last_name}"

class Startup:
    """
    Handles the startup process for the game, including player setup.
    
    Attributes:
        gamelogic (GameLogic): An instance of the GameLogic class.
    """
    
    def __init__(self, gamelogic, security):
        """
        Initializes the Startup class with an instance of GameLogic.
        
        Args:
            gamelogic (GameLogic): An instance of the GameLogic class.
        """
        self.gamelogic = gamelogic
        self.security = security

    def start_setup(self):
        """
        Handles user input to determine the number of players and rounds, and collects player information.
        
        Returns:
            tuple: A tuple containing the list of Player instances and the round limit.
        """
        try:
            number_of_users = self.security.get_validated_int("Enter the number of players (1-8): ", range(1, 9))
            clear_terminal()
            if not (1 <= number_of_users <= 8):
                log("Invalid number of players. Please choose between 1 and 8.")
                return self.start_setup()

            players = self.adding_players_info(number_of_users)
            self.print_player_details(players)
            if self.ready_to_start():
                round_limit = self.get_round_limit()
                return players, round_limit
            else:
                self.ready_to_start()

        except ValueError:
            log("Error. Invalid input. Please input an integer.")
            self.restart_start_setup()

    def ready_to_start(self):
        """
        Asks players if they are ready to start the game.
        
        Returns:
            bool: True if all players are ready, False otherwise.
        """
        while True:
            ready = input("Are you ready to start the game? (yes/no): ").lower()
            if (ready in ["yes", "y", "1"]):
                clear_terminal()
                return True
            elif (ready == "no") or (ready == "n") or (ready == "0"):
                str(input("Press the [Enter key] when you are ready to start the game..."))
                clear_terminal()
                return True
            else:
                print("Please input a valid response. ")
            

    def get_round_limit(self):
        """
        Asks the user for the round limit.
        
        Returns:
            int: The chosen round limit.
        """
        while True:
            try:
                round_limit = int(input("How many rounds do you want to play? (5/10/15): "))
                clear_terminal()
                if round_limit in [5, 10, 15]:
                    return round_limit
                else:
                    log("Invalid round limit. Please choose 5, 10, or 15.")
            except ValueError:
                log("Error. Invalid input. Please input an integer.")
    
    def print_player_details(self, players):
        """
        Prints the details of each player.
        
        Args:
            players (list): A list of Player instances.
        """
        for player in players:
            log(f"Player Details:")
            log(f"   Player #{player.id};")
            log(f"   Name: {player.name};")
            log(f"   Age: {player.age};")
            log(f"   Job Title: {player.job_title};")
            log(f"   Job Income: {BankManagement.format_currency(player.job_income)};")
            log(f"   Bank: {BankManagement.format_currency(player.bank)}")
            log(f"   Inventory: {player.inventory}")
            log(f"   Safe: {BankManagement.format_currency(player.safe)}")
            new_line()
            ready_to_start = input(f"{player.id}. Do you want to change your name? (yes/no): ").lower()
            if (ready_to_start == "yes") or (ready_to_start == "y") or (ready_to_start == "1"):
                self.enter_custom_names(player)
            else:
                clear_terminal()

    def enter_custom_names(self, player):
        """
        Allows players to enter their own name.
        
        Args:
            players (list): A list of Player instances.
        """
        log("\nEnter your custom name player -> (first name, last name):")
        custom_name = self.security.sanitize_input(input(f"Enter your custom name, Player #{player.id}: "))
        if custom_name:
            player.name = custom_name
            clear_terminal()

    def restart_start_setup(self):
        """
        Restarts the setup process if there is an error or invalid input.
        """
        log("Let's try this again.")
        self.start_setup()

    def adding_players_info(self, number_of_users):
        """
        Creates a list of Player instances with random information.
        
        Args:
            number_of_users (int): The number of players.
        
        Returns:
            list: A list of Player instances.
        """
        players = []
        for id in range(1, number_of_users + 1):  # Assign unique IDs starting from 1
            name = full_name()
            age = random.randint(18, 65)
            job_title, job_income = self.gamelogic.get_job()
            bank = 40000.0
            inventory = []
            safe = 0
            players.append(Player(id, name, age, job_title, job_income, bank, safe, inventory))
        return players
