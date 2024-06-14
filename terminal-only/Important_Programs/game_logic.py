import random
from .job_income import jobs
from .Input_Handling import Security
from .item import Item
from .ulits import log, clear_terminal, new_line
import sys

def new_window():
    return Security.sanitize_input(input("Press the [Enter Key] to continue..."))

class BankManagement:
    @staticmethod
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
            # Ensure the amount is formatted to two decimal places & comma replace with underscores
            formatted_amount = f"{amount:,.2f}".replace(',', '_') 
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
        
    @staticmethod
    def check_bank_modifications(self, players):
        """
        Checks for any bank modifications among players and formats their currency accordingly.
        
        Args:
            players (list): A list of Player instances.
        """
        for player in players:
            if isinstance(player.bank, float):
                self.format_player_bank(player)

class Employment:
    @staticmethod
    def get_job():
        """
        Randomly selects a job title and job income from the jobs dictionary.
        
        Returns:
            tuple: A tuple containing the job title and job income.
        """
        jobs_list = jobs.popitem()
        job_title = jobs_list[0].title()
        job_income = jobs_list[1]
        return job_title.title(), job_income
    
    @staticmethod
    def work(player):
        """
        Performs work action for the player, increasing their bank balance based on their job income.
        
        Args:
            player (Player): The Player instance performing the work action.
        """
        player.bank = BankManagement.deformat_currency(player.bank)  # Ensure bank balance is a float
        player.bank += player.job_income
        player.bank = round(player.bank, 2)
        log(f"{player.name} has worked and earned {BankManagement.format_currency(player.job_income)}."
            f"Bank balance updated to {BankManagement.format_currency(player.bank)}.")

class PlayerManagement:
    
    def __init__(self):
        self.current_player = None

    # @staticmethod
    # def current_player_index_id(current_player, players):
    #     # player_id = PlayerManagement.get_player_by_id(current_player, players)
    #     return player_id

    def set_current_player(self, player):
        self.current_player = player

    def view_other_player_profiles(self, players):
        """
        Allows the current player to view the players of other players.
        """
        # if not self.current_player:
        #     log("Error: Current player is not set.")
        #     return

        while True:
            try:
                player_id = Security.get_validated_int(
                    "Enter the player ID you want to view (0 to cancel): ", 
                    range(0, (len(players) + 1)))
                
                if player_id == 0:
                    clear_terminal()
                    break

                player = self.get_player_by_id(player_id, players)

                # PlayerManagement.set_current_player(self, player)

                # log(f"Player Id: #{player_id} - Current_Player_ID : #{self.current_player.id}")

                # if player_id == self.current_player.id:
                #     log("You cannot view your own profile.")
                #     continue

                if player:
                    # if player_id == self.current_player.id:
                    profile = player.leaked_profile()
                    # else:
                    #     profile = player.redacted_profile()

                    self.player_description(profile)
                    new_line()

                else:
                    log("Invalid player ID. Please try again.")
            except ValueError:
                log("Invalid input. Please enter a valid player ID.")

    def get_player_by_id(self, player_id, players):
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
    
    def player_description(self, profile):
        """
        Displays the player's description.
        
        Args:
            player (Player): The Player instance to describe.
        """
        log(f"Player #{profile['ID']} Information:")
        log(f"  Name: {profile['Name']}")
        log(f"  Age: {profile['Age']}")
        log(f"  Job Title: {profile['Job Title']}")
        log(f"  Job Income: {BankManagement.format_currency(profile['Job Income'])}")
        log(f"  Bank: {BankManagement.format_currency(profile['Bank'])}")
        log(f"  Inventory: {profile['Inventory']}")
        log(f"  Safe: {BankManagement.format_currency(profile['Safe'])}")

class CriminalActivity:

    def steal(self, player, players):
        """
        Allows the player to attempt to steal a percentage of another player's savings.

        Args:
            player (Player): The Player instance attempting the steal.
            players (list): The list of all players in the game.
        """
        while True:
            try:
                target_id = Security.get_validated_int("Enter the player ID you want to steal from (0 to cancel): ", 
                                                       range(1, (len(players) + 1)))
                if target_id == 0:
                    clear_terminal()
                    return False
                if target_id == player.id:
                    log("You cannot steal from yourself. Choose another player.")
                    continue
                target_player = PlayerManagement.get_player_by_id(target_id)
                if target_player:
                    success_rate = random.random()
                    if success_rate > 0.5:  # 50% chance of success
                        percentage = random.uniform(0.0, 1.0)  # Steal between 0% and 100%
                        player.bank = BankManagement.deformat_currency(player.bank)  # Ensure bank balance is a float
                        target_player.bank = BankManagement.deformat_currency(target_player.bank)
                        amount_stolen = target_player.bank * percentage
                        target_player.bank -= amount_stolen
                        player.bank += amount_stolen
                        target_player.bank = round(target_player.bank, 2)
                        player.bank = round(player.bank, 2)
                        log(f"Steal successful! {player.name} stole {BankManagement.format_currency(amount_stolen)},"
                            f"roughly ({(percentage*100):.2f})% from {target_player.name}.")
                        log(f"\t\t{target_player.name}'s new bank balance is {BankManagement.format_currency(target_player.bank)}.")
                        log(f"\t\t{player.name}'s new bank balance is {BankManagement.format_currency(player.bank)}.")
                    else:
                        log(f"Steal attempt failed! {player.name} couldn't steal from {target_player.name}.")
                    return True
                else:
                    log("Invalid player ID. Please try again.")
            except ValueError:
                log("Invalid input. Please enter a valid player ID.")

class Exploration:
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

            choice = Security.get_validated_choice(
                "Choose what to search for (0 to go back): ", [
                    "0", "cancel",
                    "1", "t", "treasure", "chest",
                    "2", "lottery ticket", 'l', 'lottery', 'ticket',
                    "3", "stocks", 's', 'stock'
                ]
            )
            
            if choice in ["0", "cancel"]:
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
                    log(f"{player.name} found a treasure worth {BankManagement.format_currency(reward)}!")

                elif search_item in ["lottery ticket", 'l', '2', 'lottery', 'ticket']:
                    success_rate = random.random()
                    if success_rate > 0.9: # 10% of winning
                        reward = random.choice(lottery_ticket_rewards)
                        log(f"{player.name} bought a lottery ticket and won {BankManagement.format_currency(reward)}!")
                    else:
                        reward = -5
                        log(f"{player.name} bought a lottery ticket and didn't win anything."
                            f"Lottery ticket cost {BankManagement.format_currency(reward)}")

                elif search_item in ["stocks", 's', '3', 'stock']:
                    reward = random.uniform(-500_000, 1_500_000)
                    log(f"{player.name} invested in stocks and now has {BankManagement.format_currency(reward)}!")

                # print(f"Player Bank : ${player.bank} and type is {type(player.bank)}\nReward : ${reward:2f} and type is {type(reward)}")
                reward = BankManagement.deformat_currency(reward)
                player.bank = BankManagement.deformat_currency(player.bank)  # Ensure bank balance is a float
                player.bank += reward
                player.bank = round(player.bank, 2)
                new_line()
                log(f"{player.name}'s new bank balance is {BankManagement.format_currency(player.bank)}.")
                return True
            
            else:
                log("Invalid choice. Please choose a valid option.")

class Market:
    """
    Manages the shop inventory and pricing.
    """
    def __init__(self):
        self.items = self.setup_items()

    def setup_items(self):
        """
        Sets up the initial items available in the shop.

        Returns:
            list: A list of Item instance.
        """
        return [
            Item("House", BankManagement.format_currency(self.random_prices(100_000, 1_000_000)), 
                 "A safe deposit to store a lot of 'your' money."),
            Item("Safe Deposit Ticket", BankManagement.format_currency(self.random_prices(1_000, 5_000)), 
                 "A one-time-use ticket for a safe deposit."),
            Item("Bank Note", BankManagement.format_currency(self.random_prices(10, 100)), 
                 "A bank note worth a specific amount of money.")     
        ]

    def random_prices(self, num_1, num_2):
        """
        Generates a random price within the specified range.
        
        Args:
            num_1 (float): The lower bound of the price range.
            num_2 (float): The upper bound of the price range.
        
        Returns:
            float: The generated random price.
        """
        return round(random.uniform(num_1, num_2), 2)

    def display_items(self):
        """
        Displays the iems available in the shop.
        """
        new_line()
        log("Items available  in the shop:")
        for idx, item in enumerate(self.items, start=1):
            log(f"{idx}. {item.name} - {item.price} - {item.despriction}")

    def purchase_item(self, player):
        """
        Handles the purchasing of an item from the shop by the player.
        
        Args:
            player (Player): The Player instance making the purchase.
        """
        self.display_items()
        valid_choices = [str(i) for i in range (1, len(self.items) + 1)] + ["0", "cancel"] + ["h", "house", "1"]
        valid_choices = valid_choices + ["s", "safe", "2", 'ticket', 'Safe Deposit Ticket', "deposit"]
        choice = Security.get_validated_choice("Enter the item number you want to buy (0 to cancel): ", 
                                               valid_choices)
        
        if choice in ["0", "cancel"]:
            clear_terminal()
            return False
        
        elif choice in ["h", "house", "1"]:
            choice = 1

        elif choice in ["s", "safe", "2", 'ticket', 'Safe Deposit Ticket', "deposit"]:
            choice = 1

        item_index = int(choice) - 1
        selected_item = self.items[item_index]
        selected_item.price = float(BankManagement.deformat_currency(selected_item.price))

        if player.bank >= selected_item.price:
            player.bank -= selected_item.price
            player.inventory.append(selected_item)
            new_line()
            log(f"{player.name} bought {selected_item.name} for {BankManagement.format_currency(selected_item.price)}.")
            log(f"New bank balance: {BankManagement.format_currency(player.bank)}")
        else:
            selected_item.price = (BankManagement.format_currency(selected_item.price))
            log(f"{player.name} does not have enough money to buy {selected_item.name}.")

        new_window()
        clear_terminal()
        return True

class ItemsUsage:

    @staticmethod
    def safe_deposit(player):
        """
        Put all available cash in the bank into the safe.

        Args:
            player (Player): The player who is depositing the cash into the safe.
        """
        if isinstance(player.bank, float):
            player.safe += player.bank
            player.bank = 0
            log(f"All available cash in bank has been deposited into the safe for {player.name}.")
        else:
            log("Bank balance must be a valid number.")

    @staticmethod
    def use_bank_note(player, bank_note):
        """
        Use a bank note item.

        Args:
            player (Player): The player using the bank note.
            bank_note (Item): The bank note item being used.
        """
        amount = BankManagement.deformat_currency(bank_note.price)
        player.bank += amount
        log(f"You used a bank note worth {BankManagement.format_currency(amount)}."
            f"Your bank balance has been increased by {BankManagement.format_currency(amount)}.")

    @staticmethod
    def choose_item(player, item_index):
        """
        Use an item from the player's inventory.

        Args:
            player (Player): The player using the item.
            item_index (int): The index of the item to use in the player's inventory.
        """
        if item_index < 0 or item_index >= len(player.inventory):
            log("Invalid item index.")
            return
        
        selected_item = player.inventory[item_index]
        if selected_item.name == "Safe Deposit Ticket":
            ItemsUsage.safe_deposit(player)
        elif selected_item.name == "Bank Note":
            ItemsUsage.use_bank_note(player, selected_item)
        else:
            log("This item cannot be used.")

    def use_item(player):
        """
        Allows the player to use an item from their inventory.
        """
        if player.inventory:
            log("Inventory:")
            for idx, item in enumerate(player.inventory, start=1):
                log(f"{idx}. {item.name}")
            choice = Security.get_validated_int("Enter the item number you want to use (0 to cancel): ", 
                                                 range(0, len(player.inventory) + 1))
            if choice == 0:
                clear_terminal()
                return
            item_index = int(choice) - 1
            ItemsUsage.choose_item(player, item_index)
        else:
            log("You have no items in your inventory.")


class QuitGame:
    @staticmethod
    def quit_game():
        """
        Terminate the program immediately.
        """
        sys.exit()

class GameLogic:
    """
    Contains the game logic related to jobs, stealing money, and treasures.
    """
    def __init__(self):
        self.market = Market()
        self.bank_manager = BankManagement()
        self.employment = Employment()
        self.player_manger = PlayerManagement()
        self.crime = CriminalActivity()
        self.exploration = Exploration()
        self.quit_game = QuitGame()
        self.item_usage = ItemsUsage

    def format_player_bank(self, player):
        return self.bank_manager.format_player_bank(self, player)

    def format_currency(self, amount):
        return self.bank_manager.format_currency(amount)

    def deformat_currency(self, formatted_amount):
        return self.bank_manager.deformat_currency(formatted_amount)

    def check_bank_modifications(self, players):
        return self.bank_manager.check_bank_modifications(self, players)

    def get_job(self):
        return self.employment.get_job()

    def work(self, player):
        return self.employment.work(player)

    def data_redacted(self, player):
        return self.player_manger.data_redacted(player)

    def view_other_player_players(self, players):
        return self.player_manger.view_other_player_profiles(players)

    def get_player_by_id(self, players, player_id):
        return self.player_manger.get_player_by_id(player_id)

    def player_description(self, player):
        return self.player_manger.player_description(player)

    def steal(self, player, players):
        return self.crime.steal(player, players)

    def search(self, player):
        return self.exploration.search(player)
    
    def use_item(self, player):
        return self.item_usage.use_item(player)
    
    def visit_market(self, player):
        self.market.purchase_item(player)

    def quit_game(self):
        return self.quit_game()