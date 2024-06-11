import random
from job_income import jobs
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
            
        elif isinstance(formatted_amount, (int, float)):
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
                player_id = Security.get_validated_int("Enter the player ID you want to view (0 to cancel): ", range(0, (len(players) + 1)))
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
                target_id = Security.get_validated_int("Enter the player ID you want to steal from (0 to cancel): ", range(1, (len(players) + 1)))
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
                        log(f"Steal successful! {player.name} stole {self.format_currency(amount_stolen)}, roughly ({(percentage*100):.2f})% from {target_player.name}.")
                        log(f"\t\t{target_player.name}'s new bank balance is {self.format_currency(target_player.bank)}.")
                        log(f"\t\t{player.name}'s new bank balance is {self.format_currency(player.bank)}.")
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
                
                if search_item in ["treasure", 't', '1','chest']:
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

                elif search_item in ["stocks", 's', '3', 'stock']:
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