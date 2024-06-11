from dataclasses import dataclass

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