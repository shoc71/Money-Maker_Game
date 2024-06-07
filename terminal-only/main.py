import random
from job_income import jobs
from names import names
from dataclasses import dataclass
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

# def to_continue():

class GameLogic:
    """
    Contains the game logic related to jobs, stealing money, and treasures.
    """
     
    def get_job(self):
        """
        Randomly selects a job title and job income from the jobs dictionary.
        
        Returns:
            tuple: A tuple containing the job title and job income.
        """
        jobs_list = jobs.popitem()
        job_title = jobs_list[0].title()
        job_income = jobs_list[1]
        return job_title.title(), job_income
    
    def work(self, player):
        """
        Performs work action for the player, increasing their bank balance based on their job income.
        
        Args:
            player (Player): The Player instance performing the work action.
        """
        player.bank += player.job_income
        player.bank = round(player.bank, 2)
        log(f"{player.name} worked and earned ${player.job_income}. Bank balance updated to ${player.bank}.")

    def steal_player_money(self):
        """
        Placeholder for logic to steal player money.
        """
        pass

    def treasure(self):
        """
        Placeholder for logic related to treasures.
        """
        pass

@dataclass
class Player:
    """
    Represents a player with a name, age, job title, job income, and bank balance.
    
    Attributes:
        name (str): The name of the player.
        age (int): The age of the player.
        job_title (str): The job title of the player.
        job_income (float): The job income of the player.
        bank (float): The bank balance of the player.
    """
    id : int
    name: str
    age: int
    job_title: str
    job_income: float
    bank: float

class Startup:
    """
    Handles the startup process for the game, including player setup.
    
    Attributes:
        gamelogic (GameLogic): An instance of the GameLogic class.
    """
    
    def __init__(self, gamelogic):
        """
        Initializes the Startup class with an instance of GameLogic.
        
        Args:
            gamelogic (GameLogic): An instance of the GameLogic class.
        """
        self.gamelogic = gamelogic

    def start_setup(self):
        """
        Handles user input to determine the number of players and rounds, and collects player information.
        
        Returns:
            tuple: A tuple containing the list of Player instances and the round limit.
        """
        try:
            number_of_users = int(input("\nHow many people are playing? : "))
            clear_terminal()
            if not (1 <= number_of_users <= 8):
                log("Invalid number of players. Please choose between 1 and 8.")
                return self.start_setup()

            players = self.getting_player_info(number_of_users)
            self.print_player_details(players)
            if self.ready_to_start():
                round_limit = self.get_round_limit()
                return players, round_limit
            else:
                return self.start_setup()

        except ValueError:
            log("Error. Invalid input. Please input an integer.")
            self.restart_start_setup()

    def ready_to_start(self):
        """
        Asks players if they are ready to start the game.
        
        Returns:
            bool: True if all players are ready, False otherwise.
        """
        ready = input("Are you ready to start the game? (yes/no): ").lower()
        if (ready == "yes") or (ready == "y") or (ready == "1"):
            clear_terminal()
            return True
        elif (ready == "no") or (ready == "n") or (ready == "0"):
            input("Press the [Enter key] when you are ready to start the game...")
            clear_terminal()
            return True
        else:
            print("Please input a valid response. ")
            self.ready_to_start()

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
            log(f"   Job Title: {player.job_title},")
            log(f"   Job Income: {player.job_income},")
            log(f"   Bank: {player.bank}")
            # log(f"")
            # log(f"")
            new_line()
            ready_to_start = input(f"{player.id}. Do you want to change your name? (yes/no): ").lower()
            if (ready_to_start == "yes") or (ready_to_start == "y") or (ready_to_start == "1"):
                self.enter_custom_names(player)
            # elif (ready_to_start == "no") or (ready_to_start == "n") or (ready_to_start == "0") or (ready_to_start == ""):
            #     input("Press the [Enter key] when you are ready to start the game...")
            #     clear_terminal()
            else:
                clear_terminal()

    def enter_custom_names(self, player):
        """
        Allows players to enter their own name.
        
        Args:
            players (list): A list of Player instances.
        """
        log("\nEnter your custom name player -> (first name, last name):")
        custom_name = input(f"Enter your custom name, Player #{player.id}: ")
        if custom_name:
            player.name = custom_name
            clear_terminal()

    # def change_specific_name(self, players):
    #     """
    #     Allows a specific player to change their name.
        
    #     Args:
    #         players (list): A list of Player instances.
    #     """
    #     player_index = int(input("Enter the player index to change their name (1 to n): ")) - 1
    #     if 0 <= player_index < len(players):
    #         self.enter_custom_name(players[player_index])
    #     else:
    #         log("Invalid player index.")

    def restart_start_setup(self):
        """
        Restarts the setup process if there is an error or invalid input.
        """
        log("Let's try this again.")
        self.start_setup()

    def getting_player_info(self, number_of_users):
        """
        Creates a list of Player instances with random information.
        
        Args:
            number_of_users (int): The number of players.
        
        Returns:
            list: A list of Player instances.
        """
        players = []
        for id in range(1, number_of_users + 1):  # Assign unique IDs starting from 1
            # id = 1 # how to set play ID here
            name = full_name()
            age = random.randint(18, 65)
            job_title, job_income = self.gamelogic.get_job()
            bank = 400
            players.append(Player(id, name, age, job_title, job_income, bank))
        return players

class GamePlay:
    """
    Handles the gameplay mechanics, including player turns and actions.
    
    Attributes:
        players (list): A list of Player instances representing the players in the game.
        round_limit (int): The maximum number of rounds in the game.
    """
    
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

    def start_game(self):
        """
        Starts the game with a turn-based system.
        """
        log("Starting the game!")
        
        for round_num in range(1, self.round_limit + 1):
            log(f"\nRound {round_num} begins!")
            for player in self.players:
                self.player_turn(player)
                if self.check_game_end():
                    return

    def print_player_options(self, player):
        """
        Prints the options available to a player during their turn.
        
        Args:
            player (Player): The Player instance whose turn it is.
        """
        log(f"It's Player #{player.id}'s turn.")
        log("Options:")
        log("0. Player Despriction")
        log("1. Work")
        log("2. Steal")
        log("3. Search")
        log("4. Use Item")
        log("5. End Turn")
    
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
                input("Press [Enter key] to continue...")
                clear_terminal()
                turn = 0
                break

            self.print_player_options(player)

            player_actions = input(f"Choose your action, Player #{player.id}: ").lower()
            if (player_actions == "0") or (player_actions == "despriction"):
                clear_terminal()
                self.view_other_player_profiles()
                new_line()

            elif (player_actions == "1") or (player_actions == "work"):
                new_line()
                self.gamelogic.work(player)
                turn += 4
                input("Press [Enter key] to continue...")
                clear_terminal()

            elif player_actions == "2":
                self.steal(player)
            elif player_actions == "3":
                self.search(player)
            elif player_actions == "4":
                self.use_item(player)
            elif player_actions == "5":
                new_line()
                log(f"Player #{player.id} turn has voted to end their turn.")
                input("Press [Enter key] to continue...")
                clear_terminal()
                break

            else:
                log("Invalid action. Choose between 0 and 5.")

    def view_other_player_profiles(self):
        """
        Allows the current player to view the profiles of other players.
        """
        while True:
            try:
                player_id = int(input("Enter the player ID you want to view (0 to cancel): "))
                if player_id == 0:
                    clear_terminal()
                    break
                player = self.get_player_by_id(player_id)
                if player:
                    self.player_description(player)
                    new_line()
                else:
                    log("Invalid player ID. Please try again.")
            except ValueError:
                log("Invalid input. Please enter a valid player ID.")

    def get_player_by_id(self, player_id):
        """
        Retrieves a player by their ID.
        
        Args:
            player_id (int): The ID of the player to retrieve.
        
        Returns:
            Player: The Player instance with the given ID, or None if not found.
        """
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def player_description(self, player):
        """
        Displays the player's description.
        
        Args:
            player (Player): The Player instance to describe.
        """
        log(f"Player #{player.id} Information:")
        log(f"Name: {player.name}")
        log(f"Age: {player.age}")
        log(f"Job Title: {player.job_title}")
        log(f"Job Income: ${player.job_income}")
        log(f"Bank Balance: ${player.bank}")
    
    def check_game_end(self):
        """
        Checks if the game has ended.
        
        Returns:
            bool: True if the game has ended, False otherwise.
        """
        # Placeholder for game end condition
        # Example: if self.game_over_condition_met():
        #              log("Game Over!")
        #              return True
        #          return False
        pass

# In the main block:
if __name__ == "__main__":
    gamelogic = GameLogic()
    startup = Startup(gamelogic)
    splash_screen()
    players, round_limit = startup.start_setup()
    gameplay = GamePlay(players, round_limit, gamelogic)
    gameplay.start_game()