import os

def log(message):
    """
    Logs a message by printing it to the console.
    
    Args:
        message (str): The message to be logged.
    """
    return print(message)

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