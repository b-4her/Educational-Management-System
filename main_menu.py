"""
The main menu provides options for logging in, 
signing up as a student or professor, 
and shutting down the app.
"""

# Please note that several errors raised in the
# file are randomly chosen to handle specific cases.

import sys  # System-specific parameters and functions
import re  # Regular expressions for email and password validation
import pickle  # Save and load user object data
import os  # ,subprocess  # Clear screen and interact with the OS
from users import User  # Creating users
import Project_art  # Project-specific art elements
import random  # Generate random user IDs


USERNAMES_LIST_PATH = r"Users/usernames_list.txt"
USER_OBJECTS_FOLDER = "Users"


class MainMenu:
    """
    The main menu provides options for logging in,
    signing up as a student or professor,
    and shutting down the app.
    """

    @classmethod
    def start_portal(cls):
        """Provides options to log in, sign up, or shut down."""

        try:
            print(Project_art.main_menu)
            print(
                "Please make a choice:",
                "   1 - Login",
                "   2 - Sign Up",
                "   3 - Shutdown System",
                sep="\n",
            )

            cls.user_choice: int = cls.get_choice(num_of_choices=3)
            match cls.user_choice:
                case 1:
                    cls.clear_screen()
                    cls.login_portal()
                case 2:
                    cls.clear_screen()
                    cls.signup_portal()
                case 3:
                    cls.clear_screen()
                    sys.exit()

        except (KeyboardInterrupt, EOFError):
            cls.clear_screen()
            cls.start_portal()

    @classmethod
    def login_portal(cls):
        """Prompts the user for their username and password, with an
        option available in case the user forgets their password."""

        print(Project_art.Login_portal)

        try:
            cls.load_user_data()
            if len(cls.users) == 0:
                cls.clear_screen()
                print("There are no users yet! Please sign up.")
                cls.start_portal()
                return None
            print(
                "Please Type the information requested.",
                "\nTo return to the main menu, press 'Ctrl + C'.",
                "\nIf you forgot your password, please type 'forgot' in the password field.",
                sep="",
            )
            cls.user_check()
            cls.password_check(cls.login_user_object.password)
            cls.clear_screen()

            # Note:
            # If you use a generator expression to print users, it will turn the objects into generator objects:
            # print(user for user in cls.users)
            # For more information: https://www.youtube.com/watch?v=u3T7hmLthUU
            # Use this method to iterate through objects and print them directly:
            # for user in cls.users:
            #     print(user)
            # This will print objects normally without converting them into generators.

        except (KeyboardInterrupt, EOFError):
            cls.clear_screen()
            cls.start_portal()
        except TypeError:
            cls.clear_screen()
            print("You have entered an incorrect answer or used Ctrl+C to go back.")
            cls.login_portal()

    @classmethod
    def signup_portal(cls):
        """Requests user information to create an account
        and verifies the validity of the provided information."""

        try:
            print(Project_art.signup_portal)
            print(
                "Please Type the information requested.\nTo return to the main menu, press 'Ctrl + C'."
            )
            full_name = cls.get_string(question="Full Name: ")
            username = cls.get_username()
            account_type = cls.get_account_type()
            email = cls.get_email(acc_type=account_type)
            password = cls.get_password()
            question, answer = cls.get_question()
            id = cls.get_id()

            user = User(
                full_name=full_name,
                username=username,
                account_type=account_type,
                email=email,
                password=password,
                question=question,
                answer=answer,
                id=id,
            )
            cls.save_list_file(data=user.username, path=USERNAMES_LIST_PATH)
            cls.save_class_data(
                data_object=user, save_as=user.username, folder_path=USER_OBJECTS_FOLDER
            )
            cls.clear_screen()
            print("Your'e all set!, head to the login page.")
            cls.start_portal()

        except (KeyboardInterrupt, EOFError):
            cls.clear_screen()
            print("No account has be created!")
            cls.start_portal()

    @classmethod
    def user_check(cls):
        """Validates the provided username
        and then verifies if an account exists for it."""

        while True:
            try:
                username = input("Username: ").strip()
                matches = re.search(r"^[a-z0-9_]{4,16}+$", username)

                if not matches:
                    raise ValueError
                username_is_used = False

                for user in cls.users:
                    if user.username == username:
                        cls.login_user_object = user
                        username_is_used = True

                if not username_is_used:
                    raise IndexError
                return username

            except ValueError:
                print(
                    "Invalid username,",
                    "\nUsername valid chars: a-z, 0-9, including _ (underscore).",
                    "\nType at least 4 chars and maximum of 16.",
                    sep="",
                )
            except IndexError:
                print("There is no account associated with this username.")
            except (KeyboardInterrupt, EOFError):
                cls.clear_screen()
                cls.start_portal()
                break

    @classmethod
    def password_check(cls, entered_password: str):
        """Validates the password and then verifies
        if it matches the password associated with the provided username.
        If the user selects 'forgot,' they will be directed
        to a verification question page."""

        while True:
            try:
                password = input("Password: ").strip()
                if password.lower() == "forgot":
                    user_email: str = cls.login_user_object.email
                    cls.verify_user(user_email)
                    break
                matches = re.search(r"^[^ ]{8,16}$", password)
                if not matches:
                    raise ValueError
                if entered_password.strip() != password:
                    raise IndexError
                return password

            except ValueError:
                print(
                    "Invalid password, type at least 8 chars and maximum of 16.",
                    "Please don't add any spaces.",
                )
            except IndexError:
                print("Incorrect password.")
            except (KeyboardInterrupt, EOFError):
                cls.clear_screen()
                cls.start_portal()
                break

    @classmethod
    def verify_user(cls, correct_email: str):
        """ "This page validates if the provided email is suitable
        for use and then verifies if it matches the email
        associated with the username provided during the
        login before selecting 'forgot password'"""

        cls.clear_screen()
        print(Project_art.Login_portal)
        print("To return to the login screen, press 'Ctrl + C'.")
        while True:
            try:
                email = input("Enter you email adress: ").strip().lower()
                matches = re.search(
                    r"^[\w]+@(?:stu|prof)\.harvard\.edu$", email, flags=re.IGNORECASE
                )
                if not matches:
                    raise ValueError
                used_emails = []
                for user in cls.users:
                    used_emails.append(user.email.lower())
                if email not in used_emails:
                    raise IndexError
                elif email != correct_email.lower():
                    raise IndentationError
                cls.answer_check(user_object=cls.login_user_object)
                break

            except ValueError:
                print(
                    "The email domain name should be:",
                    "\n'@stu.harvard.edu' for students and '@prof.harvard.edu' for proffesors.",
                    "\nUsername valid chars: a-z, A-Z, 0-9, including _ (underscore)",
                    sep="",
                )
            except IndexError:
                print("This email is not associated with any account.")
            except (KeyboardInterrupt, EOFError):
                cls.clear_screen()
                cls.login_portal()
                break
            except IndentationError:
                print(
                    "The email you entered is not associated with the username provided."
                )

    @classmethod
    def answer_check(cls, user_object: User):
        """Verifies if the answer to the verification
        question is correct. If not, it returns the user
        immediately to the login page with a prompt
        indicating an incorrect answer."""

        while True:
            try:
                print(f"Verification question: {user_object.question}")
                answer = input("Answer: ").strip()
                if answer == "":
                    raise ValueError
                elif answer.lower() != user_object.answer.lower():
                    raise IndexError
                cls.clear_screen()
                print(f"That's correct!, your password is: {user_object.password}")
                cls.login_portal()
                break

            except ValueError:
                print("Please type something!")
            except (KeyboardInterrupt, EOFError):
                cls.clear_screen()
                cls.login_portal()
                break
            except IndexError:
                print("Wrong answer!")

    @classmethod
    def save_class_data(cls, data_object, save_as: str, folder_path: str):
        """Saves the created user to the specified file path as a pickle file."""

        with open(f"{folder_path}/{save_as}_data.pkl", "wb") as users_data:
            pickle.dump(data_object, users_data)

    @classmethod
    def load_user_data(cls):
        """Loads the saved pickle files to retrieve the saved users on the system."""

        cls.users = []  # Iterating through a text file containing
        try:  # all the usernames and appending the data.
            with open(USERNAMES_LIST_PATH, "r") as file:
                usernames = [name.strip() for name in file.readlines()[1:]]
                for username in usernames:
                    with open(
                        f"{USER_OBJECTS_FOLDER}/{username}_data.pkl", "rb"
                    ) as data:
                        cls.users.append(pickle.load(data))
        except FileNotFoundError:
            # The user list will be empty, indicating that there are no users.
            pass

    @classmethod
    def save_list_file(cls, data: str, path: str):
        """Creates a usernames list in the specified path
        to facilitate user loading when the app is opened."""

        try:
            with open(path, "a") as file:
                file.write(f"\n{data}")

                # Note:
                # In file append mode, it can write a new line
                # and create a new file with only a new line.
                # However, when it comes to the text part,
                # it raises an error because it's in append mode.
                # That's why every time it creates a file, it starts from the next line,
                # as it has read the backslash part from here and then raised the error!

        except FileNotFoundError:
            with open(path, "w") as file:
                file.write(data)

    @classmethod
    def get_string(cls, question: str) -> str:
        """Requests a string input from the user
        with the provided question and validates
        that the user has entered at least one character."""

        while True:
            try:
                string = input(question).strip().title()
                if string == "":
                    raise ValueError
                return string

            except ValueError:
                print("Please type something!")
            except EOFError:
                pass

    @classmethod
    def get_choice(cls, num_of_choices: int) -> int:
        """Prompts the user to choose a number between 1
        and the provided number of choices."""

        while True:
            try:
                choice: int = int(input("Enter Choice (number): ").strip())
                if 1 > choice or choice > num_of_choices:
                    raise ValueError
                return choice

            except ValueError:
                print("Invalid choice")
            except EOFError:
                pass

    @classmethod
    def get_username(cls) -> str:
        """Prompts the user to enter a username and validates
        it against the specified criteria."""

        while True:
            try:
                username = input("Username: ").strip()
                matches = re.search(r"^[a-z0-9_]{4,16}+$", username)
                if not matches:
                    raise ValueError
                cls.load_user_data()
                if len(cls.users) != 0:
                    for user in cls.users:
                        # Checking if username is already taken
                        if user.username == username:
                            raise IndexError
                return username

            except ValueError:
                print(
                    "Invalid username,",
                    "\nUsername valid chars: a-z, 0-9, including _ (underscore).",
                    "\nType at least 4 chars and maximum of 16.",
                    sep="",
                )
            except IndexError:
                print("This username is already taken.")
            except EOFError:
                pass

    @classmethod
    def get_account_type(cls) -> str:
        """Prompts the user to choose between creating
        a student or professor account."""

        while True:
            try:
                acc_type = (
                    input("Account type (ex:Student, Professor): ").lower().strip()
                )
                if acc_type != "student" and acc_type != "professor":
                    raise ValueError
                return acc_type

            except ValueError:
                print("Invalid input,\nplease type 'Student' or 'Professor'")
            except EOFError:
                pass

    @classmethod
    def get_email(cls, acc_type: str) -> str:
        """Requests the user to input an email
        ending with a specific domain associated
        with the provided account type."""

        while True:
            try:
                email = input("Email adress: ").strip().lower()
                if acc_type == "student":
                    matches = re.search(
                        r"^[\w]+@stu\.harvard\.edu$", email, flags=re.IGNORECASE
                    )
                else:
                    matches = re.search(
                        r"^[\w]+@prof\.harvard\.edu$", email, flags=re.IGNORECASE
                    )
                if not matches:
                    raise ValueError
                cls.load_user_data()
                if len(cls.users) != 0:
                    for user in cls.users:
                        if email == user.email:
                            raise IndexError
                return email

            except ValueError:
                if acc_type == "student":
                    print(
                        "Student email domain name should be '@stu.harvard.edu'",
                        "\nUsername valid chars: a-z, A-Z, 0-9, including _ (underscore)",
                        sep="",
                    )
                elif acc_type == "professor":
                    print(
                        "Professor email domain name should be '@prof.harvard.edu'",
                        "\nUsername valid chars: a-z, A-Z, 0-9, including _ (underscore)",
                        sep="",
                    )
            except IndexError:
                print("This email is already in use.")
            except EOFError:
                pass

    @classmethod
    def get_password(cls) -> str:
        """Prompts the user to type a password and checks
        if it meets the specified criteria."""

        while True:
            try:
                password = input("Password = ").strip()
                matches = re.search(r"^[^ ]{8,16}$", password)
                if not matches:
                    raise ValueError
                return password

            except ValueError:
                print(
                    "Invalid password, type at least 8 chars and maximum of 16.",
                    "Please don't add any spaces.",
                )
            except EOFError:
                pass

    @classmethod
    def get_question(cls) -> tuple:
        """Prompts the user to provide a verification question
        and answer to use in case of a forgotten password,
          ensuring that the user types at least one character."""

        while True:
            try:
                question = input("Verification question: ").strip().capitalize()
                if question.strip() == "":
                    raise ValueError
                break

            except ValueError:
                print("Please type something!")
            except EOFError:
                pass

        while True:
            try:
                answer = input("Answer: ").strip()
                if answer == "":
                    raise ValueError
                break

            except ValueError:
                print("Please type something!")
            except EOFError:
                pass

        return question, answer

    @classmethod
    def get_id(cls) -> str:
        """Generates a random ID in a specific format."""

        id = "0"
        cls.load_user_data()
        nums = [str(num) for num in range(10)]
        for _ in range(5):
            id += random.choice(nums)
        if len(cls.users) == 0:
            id += "01"
        else:
            id += str((len(cls.users) + 1)).zfill(2)
        return id

    @classmethod
    def clear_screen(cls):
        """Clears the terminal screen."""

        ## method 1: (Avoid making user type comands if you want to use this)
        # operating_system = sys.platform
        # match operating_system:
        #     case "win32" | "darwin":
        #         subprocess.run("clear", shell=True)
        #     case "linux":
        #         subprocess.run("cls", shell=True)
        #     case _:
        #         pass
        ## more info about this method:
        ## https://www.youtube.com/watch?v=Kmu6rmPQt4c&list=PL69OGRm1iAMV8DlHi4AzMkKemT_Sb3mLg&index=34

        # method 2:
        os.system("cls||clear")  # alot easier :)
