from dataclasses import dataclass, field
from .item import Item

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
    safe : float
    inventory : list['Item'] = field(default_factory=list)
    # safe : float

    def redacted_profile(self):
        """
        Returns a redacted version of the player's profile.
        
        Returns:
            dict: A dictionary with the redacted profile information.
        """
        return {
                "ID": self.id,
                "Name": "Redacted",
                "Age": "Redacted",
                "Job Title": "Redacted",
                "Job Income": "Redacted",
                "Bank": "Redacted",
                "Inventory": "Redacted",
                "Safe": "Redacted"
            }
    
    def normal_profile(self):
        """
        Returns a normal version of the player's profile.
        
        Returns:
            dict: A dictionary with the redacted profile information.
        """
        return {
                "ID": self.id,
                "Name": self.name,
                "Age": self.age,
                "Job Title": self.job_title,
                "Job Income": "Redacted",
                "Bank": "Redacted",
                "Inventory": "Redacted",
                "Safe": "Redacted"
            }
    
    def bank_detailed__profile(self):
        """
        Returns a normal version of the player's profile.
        
        Returns:
            dict: A dictionary with the player profile information. 
            Id, Name, Age, Job_Title
        """
        return {
                "ID": self.id,
                "Name": self.name,
                "Age": self.age,
                "Job Title": self.job_title,
                "Job Income": self.job_income,
                "Bank": self.bank,
                "Inventory": "Redacted",
                "Safe": "Redacted"
            }
    
    def leaked_profile(self):
        """
        Returns a normal version of the player's profile.
        
        Returns:
            dict: A dictionary with the player profile information. 
            Id, Name, Age, Job_Title
        """
        return {
                "ID": self.id,
                "Name": self.name,
                "Age": self.age,
                "Job Title": self.job_title,
                "Job Income": self.job_income,
                "Bank": self.bank,
                "Inventory": [item.__dict__ for item in self.inventory],
                "Safe": self.safe
            }