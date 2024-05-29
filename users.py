"""This class serves as a data structure designed 
to be used with the pickle library for saving 
users' data, replacing the need for a CSV file."""


class User:
    """This class serves as a data structure designed
    to be used with the pickle library for saving
    users' data, replacing the need for a CSV file."""

    def __init__(
        self,
        full_name: str,  # For profile and asnwers or courses viewing
        username: str,  # For login
        account_type: str,  # For login and management of data
        email: str,  # Can be used when the password had been forgoten
        password: str,  # For login
        question: str,  # In case the user has forgotten their password.
        answer: str,  # In case the user has forgotten their password.
        id: str,  # For courses management
    ):

        self.full_name: str = full_name
        self.username: str = username
        self.account_type: str = account_type
        self.email: str = email
        self.password: str = password
        self.question: str = question
        self.answer: str = answer
        self.id: str = id

    def __str__(self):
        return f"This is an object of a {self.account_type} called {self.full_name}."
