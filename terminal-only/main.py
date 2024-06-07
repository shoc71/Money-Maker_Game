import random
from job_income import jobs
from names import names
from dataclasses import dataclass

def log(message):
    """
    Logs a message by printing it to the console.
    
    Args:
        message (str): The message to be logged.
    """
    return print(message)

def full_name():
    first_name = random.choice(names).title()
    last_name = random.choice(names).title()
    return f"{first_name}, {last_name}"

def splash_screen():
    log("Welcome to the game. This is the Money-Game.")
    log("The one with the most amount of money by the end of this wins.")

class GameLogic:
    """
    Contains the game logic related to jobs, stealing money, and treasures.
    """
     
    def job(self):
        """
        Randomly selects a job title and job income from the jobs dictionary.
        
        Returns:
            tuple: A tuple containing the job title and job income.
        """
        jobs_list = jobs.popitem()
        job_title = jobs_list[0].title()
        job_income = jobs_list[1]
        return job_title.title(), job_income

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
        Handles user input to determine the number of players and collects player information.
        """
        try:
            number_of_users = int(input("\nHow many people are playing? : "))

            if 1 <= number_of_users <= 8:
                players = self.getting_player_info(number_of_users)
                log(players)

            elif number_of_users <= 0:
                log("Cannot play with negative players.")
                self.restart_start_setup()
                
            elif number_of_users > 8:
                log("Too many players for the program to handle.")
                self.restart_start_setup()

        except ValueError:
            log("Error. Invalid input. Please input an integer.")
            self.restart_start_setup()

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
        for _ in range(number_of_users):
            name = full_name()
            age = random.randint(18, 65)
            job_title, job_income = self.gamelogic.job()
            bank = 400
            players.append(Player(name, age, job_title, job_income, bank))
        return players

if __name__ == "__main__":
    gamelogic = GameLogic()
    startup = Startup(gamelogic)
    splash_screen()
    startup.start_setup()