from .Input_Handling import Security
from .ulits import log, clear_terminal, new_line

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
            5: "Visit Shop",
            6: "End Turn"
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

            player_actions = Security.get_validated_choice(
                f"Choose your action, Player #{player.id}: ",
                ["0", "description", "player description", "d", 
                 "1", "work", "w", 
                 "2", "steal", 
                 "3", "search"
                 "4", "use_item", "u", "i", "item"
                 "5", "market", "m"
                 "6", "end turn", "end", "e",
                 "quit"]
            ).lower()

            if player_actions in ["0", "despriction", "player despriction", "d"]:
                self.gamelogic.view_other_player_profiles(self.players)

            elif player_actions in ["1", "work", "w"]:
                new_line()
                self.gamelogic.work(player)
                turn += 4
                new_window()
                clear_terminal()

            elif player_actions in ["2", "steal"]:
                self.gamelogic.steal(player, self.players)
                turn += 1
                new_window()
                clear_terminal()

            elif player_actions in ["3", "search"]:
                new_line()
                self.gamelogic.search(player)
                turn += 6
                new_window()
                clear_terminal()

            elif player_actions in ["4", "use_item", "item", "u", "i"]:
                self.use_item(player)

            elif player_actions in ["5", "market", "m"]:
                self.gamelogic.purchase_item(player)

            elif player_actions in ["6", "end turn", "end", "e"]:
                new_line()
                log(f"Player #{player.id} turn has voted to end their turn.")
                new_window()
                clear_terminal()
                break

            elif player_actions == "quit":
                log(f"{player.name} has been forcefully terminated this program early.")

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
