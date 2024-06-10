import random
from job_income import jobs
from names import names
from dataclasses import dataclass
import os
from Input_Handling import Security

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

class GameLogic:
    """
    Contains the game logic related to jobs, stealing money, and treasures.
    """
     
    def format_player_bank(self, player):
        """
        Formats the bank balances of all players in the game.
        
        Args:
            players (list): A list of Player instances.
        """
        player.bank = round(player.bank, 2)
        player.bank = self.format_currency(player.bank)

    @staticmethod
    def format_currency(amount):
        """
        Formats a currency amount to include underscores for thousands and millions.

        Args:
            amount (float or int): The currency amount to be formatted.

        Returns:
            str: The formatted currency amount.
        """
        if isinstance(amount, (float, int)):
            # Ensure the amount is formatted to two decimal places
            formatted_amount = f"{amount:,.2f}"
            
            # Replace commas with underscores
            formatted_amount = formatted_amount.replace(',', '_')
            
            return f"${formatted_amount}"
        elif isinstance(amount, str):
            return amount
        else:
            raise TypeError("Amount must be a number or a string")
        
    @staticmethod
    def deformat_currency(formatted_amount):
        """
        Deformats a currency string back to a numeric value.

        Args:
            formatted_amount (str): The formatted currency amount.

        Returns:
            float: The numeric value of the currency amount.
        """
        if isinstance(formatted_amount, str):
            # Remove the dollar sign and underscores
            cleaned_amount = formatted_amount.replace('$', '').replace('_', '')
            
            # Convert to float
            return float(cleaned_amount)
            
        elif isinstance( formatted_amount, (int, float)):
            return float(formatted_amount)
        
        else:
            raise TypeError("Formatted amount must be a string")
        
    def check_bank_modifications(self, players):
        """
        Checks for any bank modifications among players and formats their currency accordingly.
        
        Args:
            players (list): A list of Player instances.
        """
        for player in players:
            if isinstance(player.bank, float):
                self.format_player_bank(player)

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
        player.bank = self.deformat_currency(player.bank)  # Ensure bank balance is a float
        player.bank += player.job_income
        player.bank = round(player.bank, 2)
        log(f"{player.name} has worked and earned {self.format_currency(player.job_income)}. Bank balance updated to {self.format_currency(player.bank)}.")

    def view_other_player_profiles(self, players):
        """
        Allows the current player to view the profiles of other players.
        """
        while True:
            try:
                player_id = int(input("Enter the player ID you want to view (0 to cancel): "))
                if player_id == 0:
                    clear_terminal()
                    break
                player = self.get_player_by_id(players, player_id)
                if player:
                    self.player_description(player)
                    new_line()
                else:
                    log("Invalid player ID. Please try again.")
            except ValueError:
                log("Invalid input. Please enter a valid player ID.")

    def get_player_by_id(self, players, player_id):
        """
        Retrieves a player by their ID.
        
        Args:
            player_id (int): The ID of the player to retrieve.
        
        Returns:
            Player: The Player instance with the given ID, or None if not found.
        """
        for player in players:
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
        log(f"  Name: {player.name};")
        log(f"  Age: {player.age};")
        log(f"  Job Title: {player.job_title};")
        log(f"  Job Income: {self.format_currency(player.job_income)};")
        log(f"  Bank Balance: {self.format_currency(player.bank)}")

    def steal(self, player, players):
        """
        Allows the player to attempt to steal a percentage of another player's savings.

        Args:
            player (Player): The Player instance attempting the steal.
            players (list): The list of all players in the game.
        """
        while True:
            try:
                target_id = int(input("Enter the player ID you want to steal from (0 to cancel): "))
                if target_id == 0:
                    clear_terminal()
                    return False
                if target_id == player.id:
                    log("You cannot steal from yourself. Choose another player.")
                    continue
                target_player = self.get_player_by_id(players, target_id)
                if target_player:
                    success_rate = random.random()
                    if success_rate > 0.5:  # 50% chance of success
                        percentage = random.uniform(0.0, 1.0)  # Steal between 0% and 100%
                        player.bank = self.deformat_currency(player.bank)  # Ensure bank balance is a float
                        target_player.bank = self.deformat_currency(target_player.bank)
                        amount_stolen = target_player.bank * percentage
                        target_player.bank -= amount_stolen
                        player.bank += amount_stolen
                        target_player.bank = round(target_player.bank, 2)
                        player.bank = round(player.bank, 2)
                        log(f"Steal successful! {player.name} stole {self.format_currency(amount_stolen)} from {target_player.name}.")
                        log(f"{target_player.name}'s new bank balance is {self.format_currency(target_player.bank)}.")
                        log(f"{player.name}'s new bank balance is {self.format_currency(player.bank)}.")
                    else:
                        log(f"Steal attempt failed! {player.name} couldn't steal from {target_player.name}.")
                    return True
                else:
                    log("Invalid player ID. Please try again.")
            except ValueError:
                log("Invalid input. Please enter a valid player ID.")

    def search(self, player):
        """
        Allows the player to choose an item to search for and potentially gain a reward.

        This method presents the player with a menu of search options: treasure, lottery ticket, and stocks.
        Based on the player's choice, the player can earn a random amount of money, which is added to their bank balance.
        The player can also choose to go back to the player turn menu.

        Args:
            player (Player): The player who is performing the search.

        Returns:
            bool: True if the player completed a search action, False if they chose to go back to the player turn menu.
        """

        options = {
            "1": "treasure",
            "2": "lottery ticket",
            "3": "stocks",
            "0": "back"
        }
        
        while True:
            new_line()
            log("Search options:")
            for key, value in options.items():
                log(f"  {key}. {value.title()}")
            
            choice = input("Choose what to search for (0 to go back): ")
            
            if choice == "0":
                clear_terminal()
                return False
            
            search_item = options.get(choice)

            lottery_ticket_rewards = [0.5, 0, 1, 5, 10, 20, 25, 50, 100, 1_000, 
                                      5_000, 10_000, 15_000, 20_000, 25_000,
                                      50_000, 100_000, 250_000, 500_000, 
                                      1_000_000, 0.25, 0.10, 2, 15]

            if search_item:
                reward = 0
                
                if search_item in ["treasure", 't', '1']:
                    reward = random.uniform(-1_000, 10_000)
                    log(f"{player.name} found a treasure worth {self.format_currency(reward)}!")

                elif search_item in ["lottery ticket", 'l', '2', 'lottery', 'ticket']:
                    success_rate = random.random()
                    if success_rate > 0.9: # 10% of winning
                        reward = random.choice(lottery_ticket_rewards)
                        log(f"{player.name} bought a lottery ticket and won {self.format_currency(reward)}!")
                    else:
                        reward = -5
                        log(f"{player.name} bought a lottery ticket and didn't win anything. Lottery ticket cost {self.format_currency(reward)}")

                elif search_item in ["stocks", 's', '3']:
                    reward = random.uniform(-500_000, 1_500_000)
                    log(f"{player.name} invested in stocks and now has {self.format_currency(reward)}!")

                # print(f"Player Bank : ${player.bank} and type is {type(player.bank)}\nReward : ${reward:2f} and type is {type(reward)}")
                reward = self.deformat_currency(reward)
                player.bank = self.deformat_currency(player.bank)  # Ensure bank balance is a float
                player.bank += reward
                player.bank = round(player.bank, 2)
                new_line()
                log(f"{player.name}'s new bank balance is {self.format_currency(player.bank)}.")
                return True
            
            else:
                log("Invalid choice. Please choose a valid option.")

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

            players = self.getting_player_info(number_of_users)
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
            log(f"   Job Income: ${player.job_income};")
            log(f"   Bank: ${player.bank}")
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
        custom_name = input(f"Enter your custom name, Player #{player.id}: ")
        if custom_name:
            player.name = custom_name
            clear_terminal()

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
            name = full_name()
            age = random.randint(18, 65)
            job_title, job_income = self.gamelogic.get_job()
            bank = 400.0
            players.append(Player(id, name, age, job_title, job_income, bank))
        return players

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