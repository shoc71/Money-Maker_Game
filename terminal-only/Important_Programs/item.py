from dataclasses import dataclass

@dataclass
class Item:
    """
    Represents an item in the shop.
    
    Attributes:
        name (str): The name of the item.
        price (float): The price of the item.
        description (str): A brief description of the item.
    """
    name : str
    price : float
    despriction : str