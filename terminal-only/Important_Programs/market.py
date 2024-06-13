import random
from .item import Item
from .player import Player
from .Input_Handling import Security
from .ulits import log, clear_terminal, new_line

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
            Item("House", self.random_prices(500_000, 1_000_000), "A safe deposit to store a lot of their money."),
            Item("Safe Deposit Ticket", self.random_prices(1_000, 5_000), "A one-time-use ticket for a safe deposit.")
        ]

    # House, Safe_Deposit_Ticket (one-time-use-only), 
    def random_prices(num_1, num_2):
        return round(random.uniform(num_1, num_2), 2)

    def display_items(self):
        """
        Displays the iems available in the shop.
        """
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
        valid_choices = [str(i) for i in range (1, len(self.items) + 1)] + ["0", "cancel"]
        choice = Security.get_validated_choice("Enter the item number you want to buy (0 to cancel): ", 
                                               valid_choices)
        
        if choice in ["0", "cancel"]:
            clear_terminal()
            return False
        
        selected_item = self.items[int(choice) - 1]

        if player.bank >= selected_item.price:
            player.bank -= selected_item.price
            player.inventory.append(selected_item)
            log(f"{player.name} bought {selected_item.name} for {bank_manager.format_currency(selected_item.price)}.")
            log(f"New bank balance: {bank_manager.format_currency(player.bank)}")
        else:
            log(f"{player.name} does not have enough money to buy {selected_item.name}.")

        new_window()
        clear_terminal()
        return True