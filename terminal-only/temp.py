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
    print(message)

def full_name():
    """
    Generates a full name by combining a first name and last name from the names list.
    
    Returns:
        str: A full name in the format "First Last".
    """
    first_name = random.choice(names).title()
    last_name = random.choice(names).title()
    return f"{first_name} {last_name}"

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
    print("\n")

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
    id: int
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
        Formats the bank balance of a player for display.
        
        Args:
            player (Player): A Player instance.
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
        job_title, job_income = random.choice(list(jobs.items()))
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
        log(f"{player.name} has worked and earned ${self.format_currency(player.job_income)}. Bank balance updated to {self.format_currency(player.bank)}.")

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
        log(f"  Job Income: ${self.format_currency(player.job_income)};")
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
                        percentage = random.uniform(0.1, 0.3)  # Steal between 10% and 30%
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
            "4": "back"
        }
        while True:
            log("Choose an item to search for:")
            for option, item in options.items():
                log(f"{option}. {item.capitalize()}")

            choice = input("Enter your choice (1-4): ").strip()
            if choice in options:
                if options[choice] == "back":
                    clear_terminal()
                    return False

                amount = random.uniform(100, 5000)  # Random reward amount between 100 and 5000
                player.bank = self.deformat_currency(player.bank)  # Ensure bank balance is a float
                player.bank += amount
                player.bank = round(player.bank, 2)
                log(f"{player.name} searched for {options[choice]} and found {self.format_currency(amount)}! Bank balance updated to {self.format_currency(player.bank)}.")
                return True
            else:
                log("Invalid choice. Please select a valid option.")

    def enter_ages(self, num_players):
        """
        Prompts each player to enter their age and returns the list of ages.

        Args:
            num_players (int): The number of players.

        Returns:
            list: A list of ages entered by the players.
        """
        ages = []
        for i in range(num_players):
            while True:
                try:
                    age = int(input(f"Player {i+1}, enter your age: "))
                    if age < 0:
                        raise ValueError("Age cannot be negative.")
                    ages.append(age)
                    break
                except ValueError as e:
                    log(f"Invalid input. Please enter a valid age. {e}")
        return ages

    def enter_players(self):
        """
        Prompts the user to enter the number of players and their details.

        This method prompts the user to enter the number of players and then collects
        details for each player, including their name, age, job title, job income, and initial bank balance.
        It then creates Player instances and returns them as a list.

        Returns:
            list: A list of Player instances created from the entered details.
        """
        clear_terminal()
        while True:
            try:
                num_players = int(input("Enter the number of players: "))
                if num_players <= 0:
                    raise ValueError("Number of players must be positive.")
                break
            except ValueError as e:
                log(f"Invalid input. Please enter a valid number of players. {e}")

        ages = self.enter_ages(num_players)
        players = []
        for i in range(num_players):
            name = full_name()
            age = ages[i]
            job_title, job_income = self.get_job()
            initial_bank_balance = 0.0
            player = Player(id=i+1, name=name, age=age, job_title=job_title, job_income=job_income, bank=initial_bank_balance)
            players.append(player)

        clear_terminal()
        log("Players entered:")
        for player in players:
            self.player_description(player)
            new_line()
        
        return players
