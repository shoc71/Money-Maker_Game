import re

def log(message):
    """
    Logs a message by printing it to the console.
    
    Args:
        message (str): The message to be logged.
    """
    return print(message)

class Security:

    @staticmethod
    def sanitize_input(user_input):
        """
        Sanitizes the user input by removing potentially harmful characters.

        Args:
            user_input (str): The input string to sanitize.

        Returns:
            str: The sanitized input string.
        """
        # Remove potentially harmful characters or patterns
        sanitized = re.sub(r'[^\w\s]', '', user_input)
        return sanitized
    
    @staticmethod
    def get_validated_int(prompt, valid_range):
        """
        Prompts the user for an integer input and validates it.

        Args:
            prompt (str): The prompt to display to the user.
            valid_range (range): A range object defining the valid integer range.

        Returns:
            int: The validated integer input.
        """
        while True:
            try:
                value = int(Security.sanitize_input(input(prompt)))
                if value in valid_range:
                    return value
                else:
                    log(f"Invalid input. Please enter a number between {valid_range.start} and {valid_range.stop - 1}.")
            except ValueError:
                log("Invalid input. Please enter a valid integer.")

    @staticmethod
    def get_validated_choice(prompt, valid_choices):
        """
        Prompts the user for a choice input and validates it.

        Args:
            prompt (str): The prompt to display to the user.
            valid_choices (list): A list of valid choice strings.

        Returns:
            str: The validated choice input.
        """
        while True:
            choice = Security.sanitize_input(input(prompt).lower())
            if choice in valid_choices:
                return choice
            else:
                log(f"Invalid choice. Please choose from {', '.join(valid_choices)}.")