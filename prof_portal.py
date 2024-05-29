"""
The Professor Portal allows professors to manage 
their profile, classes, assignments, and students grades. 
They can edit their profile, add or delete classes 
and assignments, and set grades for student submissions.
"""

# Please note that several errors raised in the
# file are randomly chosen to handle specific cases.

from main_menu import MainMenu  # Inheriting some methods
from courses import Course  # Creating classes
import Project_art  # Project-specific art elements
import pickle  # Save and load user object data
import random  # Generate random user IDs
from tabulate import tabulate  # Making nice looking tables of data
import os  # Removing files
import sys  # exit


COURSES_LIST_PATH = r"Courses_Data/courses_list.txt"
COURSE_OBJECTS_FOLDER = "Courses_Data"
USERNAMES_LIST_PATH = r"Users/usernames_list.txt"
USER_OBJECTS_FOLDER = "Users"


# Inherets MainMenu class.
class ProfPortal(MainMenu):
    """
    The Professor Portal allows professors to manage
    their profile, classes, assignments, and students grades.
    They can edit their profile, add or delete classes
    and assignments, and set grades for student submissions.
    """

    @classmethod
    def prof_main_portal(cls):
        """Provides choices such as logging out,
        viewing profile, creating a course,
        or listing created courses."""

        try:
            print(Project_art.professor_portal)
            print(
                "Please make a choice:",
                "   1 - List Courses",
                "   2 - Creat Course",
                "   3 - Profile",
                "   4 - Exit",
                sep="\n",
            )

            main_choice: int = super().get_choice(num_of_choices=4)
            match main_choice:
                case 1:
                    super().clear_screen()
                    cls.list_courses()
                case 2:
                    super().clear_screen()
                    cls.create_course()
                case 3:
                    super().clear_screen()
                    cls.prof_profile()
                case 4:
                    super().clear_screen()
                    sys.exit()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            cls.prof_main_portal()

    @classmethod
    def list_courses(cls):
        """Lists the professor's own courses and provides
        an option to view each course's details."""

        n = 1  # to prevent the loop from printing the table infinite times
        while True:
            try:
                if n == 1:
                    n += 1
                    print(Project_art.Courses_list)
                    current_prof_courses = cls.current_prof_courses()

                    if len(current_prof_courses) > 0:
                        print("To view a course details, please make a choice.")
                    print("To return to the main menu, press 'Ctrl + C'.\n")

                    table = []
                    headers = [
                        "",
                        "Title",
                        "Code",
                        "Students Number",
                        "Assignments Number",
                    ]

                    if len(current_prof_courses) == 0:
                        table.append(["", "None", "None", "None", "None"])
                    elif len(current_prof_courses) > 0:
                        index = 1
                        for course in current_prof_courses:
                            data = []
                            data.append(str(index).zfill(2))
                            index += 1  # 0th course in courses
                            data.append(course.course_title)
                            data.append(course.course_code)
                            data.append(str(len(course.enrolled_students)).zfill(2))
                            data.append(str(len(course.course_assignments)).zfill(2))
                            table.append(data)

                    print(tabulate(table, headers, tablefmt="simple"))
                    print()  # to add empty line
                    if len(current_prof_courses) == 0:
                        print("There are no courses to view.")
                    elif len(current_prof_courses) > 0:
                        choice: int = super().get_choice(len(table))
                        super().clear_screen()
                        cls.view_course(current_prof_courses[choice - 1])
                        break

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.prof_main_portal()
                break

    @classmethod
    def create_course(cls):
        """Allows the professor to create a course by
        providing the necessary information about it."""
        print(Project_art.create_course)
        while True:
            try:  
                print(
                    "Please Type the information requested.\nTo return to the main menu, press 'Ctrl + C'."
                )
                course_title = super().get_string(question="Course Title: ")
                if len(course_title) > 20:
                    raise FileNotFoundError
                course_descrioption = super().get_string(
                    question="Course Description: "
                )
                if len(course_descrioption) > 70:
                    raise IndentationError

                course_code = cls.get_course_code()
                course_prof_id = super().login_user_object.id
                course_prof = super().login_user_object.full_name
                course = Course(
                    course_title,
                    course_code,
                    course_prof_id,
                    course_descrioption,
                    course_prof,
                )
                cls.save_list_file(data=course.course_code, path=COURSES_LIST_PATH)
                cls.save_class_data(
                    data_object=course,
                    save_as=course.course_code,
                    folder_path=COURSE_OBJECTS_FOLDER,
                )

                super().clear_screen()
                print("Course created successfully.")
                cls.prof_main_portal()
                break

            except FileNotFoundError:
                print("The Title length should not exceed 20 characters.\n")
            except IndentationError:
                print("The description length should not exceed 70 characters.\n")
            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                print("No course has be created!")
                cls.prof_main_portal()
                break

    @classmethod
    def prof_profile(cls):
        """Shows the profile information such as ID,
        account, etc., and provides an option for
        editing the password and verification question."""

        try:
            print(Project_art.profile)
            print(
                "To return to the main menu, press 'Ctrl + C'.",
                "For any other operation please make a choice.",
                f"   -> University ID: {super().login_user_object.id}",
                f"   -> Full Name: {super().login_user_object.full_name}",
                f"   -> Number of Created Courses: {str(len(cls.current_prof_courses())).zfill(2)}",
                f"   -> Username: {super().login_user_object.username}",
                f"   -> Email Adress: {super().login_user_object.email}",
                f"   -> Password: {super().login_user_object.password}",
                f"   -> Verification Question & Answer:",
                f"          {super().login_user_object.question} - {super().login_user_object.answer}",
                "  1 - Change Password",
                "  2 - Change Verification Question & Answer",
                sep="\n",
            )
            profile_choice: int = super().get_choice(num_of_choices=2)
            match profile_choice:
                case 1:
                    super().clear_screen()
                    cls.edit_password()
                case 2:
                    super().clear_screen()
                    cls.edit_question()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            cls.prof_main_portal()

    @classmethod
    def create_assignment(cls, course: Course):
        """Allows the professor to create an assignment for the
        course by providing necessary information."""
        print(Project_art.create_assignment)
        while True:
            try:
                print(
                    "Please Type the information requested.\nTo return to the course overview, press 'Ctrl + C'."
                )
                assignment_name = super().get_string(question="Assignment Name: ")

                if len(assignment_name) > 20:
                    raise FileNotFoundError
                if len(course.course_assignments) > 0:
                    course_assignments = []
                    for assignment in course.course_assignments:
                        course_assignments.append(assignment["name"])
                    if assignment_name in course_assignments:
                        raise ValueError

                assignment_description = super().get_string(
                    question="Assignment Description: "
                )
                if len(assignment_description) > 70:
                    raise IndentationError

                # Adding the assignment to enrolled students
                students_in_course = []
                if len(course.enrolled_students) > 0:
                    for student in course.enrolled_students:
                        students_in_course.append(
                            {
                                "name": student["name"],
                                "id": student["id"],
                                "grade": "NA / 100",
                                "solution": "",
                            }
                        )
                course.course_assignments.append(
                    {
                        "description": assignment_description,
                        "name": assignment_name,
                        "students": students_in_course,
                    }
                )
                cls.save_class_data(
                    data_object=course,
                    save_as=course.course_code,
                    folder_path=COURSE_OBJECTS_FOLDER,
                )
                super().clear_screen()
                cls.view_course(course)
                break

            except FileNotFoundError:
                print("The Name length should not exceed 20 characters.\n")
            except IndentationError:
                print("The description length should not exceed 70 characters.\n")
            except ValueError:
                print("This name is already used")
            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.view_course(course)
                break

    @classmethod
    def list_assignments(cls, course: Course):
        """Lists the course assignments and
        provides an option to show each one's details."""

        n = 1
        while True:
            try:
                if n == 1:
                    n += 1
                    assignments = course.course_assignments
                    print(Project_art.list_assignments)
                    if len(assignments) > 0:
                        print("To view an assignment details, please make a choice.")
                    print("To return to the course overview, press 'Ctrl + C'.\n")

                    table = []
                    headers = ["", "Name", "Description"]
                    if len(assignments) == 0:
                        table.append(["", "None", "None"])
                    elif len(assignments) > 0:
                        index = 1
                        for assignment in assignments:
                            data = []
                            data.append(str(index).zfill(2))
                            index += 1
                            data.append(assignment["name"])
                            data.append(assignment["description"])
                            table.append(data)

                    print(tabulate(table, headers, tablefmt="simple"))
                    print()  # to add empty line
                    if len(assignments) == 0:
                        print("There are no assignments to view.")
                    elif len(assignments) > 0:
                        choice: int = super().get_choice(len(table)) - 1
                        super().clear_screen()
                        cls.view_assignment(assignments[choice], course)
                        break

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.view_course(course)
                break

    @classmethod
    def view_assignment(cls, assignment: dict, course: Course):
        """Shows the assignment details such as the students' solutions, etc.,
        and provides an option to delete the assignment."""

        while True:
            try:
                print(Project_art.view_assignment)
                print(
                    "To return to asignments list, press 'Ctrl + C'.",
                    "To review student solution and assign grade, please pick a student.\n",
                    sep="\n",
                )

                print(
                    tabulate(
                        [["", ""]],
                        headers=[assignment["name"], assignment["description"]],
                        tablefmt="simple",
                    )
                )

                if len(assignment["students"]) > 0:
                    header = ["", "Student ID", "Student Name", "Student Grade"]
                    students_table = []
                    index = 1

                    for student in assignment["students"]:
                        students_table.append(
                            [
                                str(index).zfill(2),
                                student["id"],
                                student["name"],
                                student["grade"],
                            ]
                        )
                        index += 1
                    print(tabulate(students_table, headers=header, tablefmt="simple"))
                    print()
                    print(
                        f"To delete the assignment, type {str(len(students_table) + 1).zfill(2)}.\n"
                    )
                    choice: int = super().get_choice(len(students_table) + 1)

                    if choice == len(students_table) + 1:  # delete assignment
                        super().clear_screen()
                        course.course_assignments.remove(assignment)
                        cls.save_class_data(
                            data_object=course,
                            save_as=course.course_code,
                            folder_path=COURSE_OBJECTS_FOLDER,
                        )
                        cls.load_courses_data()
                        cls.list_assignments(course)
                        break

                    else:
                        super().clear_screen()
                        cls.set_grade(
                            assignment["students"][choice - 1], assignment, course
                        )
                        break

                elif len(course.enrolled_students) == 0:
                    print("- There are no students enrolled in this course yet.\n")
                    print("To delete the assignment, type 1.\n")

                    choice: int = super().get_choice(1)  # delete assignment
                    super().clear_screen()
                    course.course_assignments.remove(assignment)
                    cls.save_class_data(
                        data_object=course,
                        save_as=course.course_code,
                        folder_path=COURSE_OBJECTS_FOLDER,
                    )
                    cls.load_courses_data()
                    cls.list_assignments(course)
                    break

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.list_assignments(course)
                break

    @classmethod
    def set_grade(cls, student: dict, assignment: dict, course: Course):
        """Allows the professor to set grades on the
        students' solutions if they were submitted."""

        n = 1
        while True:
            try:
                if n == 1:
                    n += 1
                    print(Project_art.set_grade)
                    print("To return to the assignment overview, press 'Ctrl + C'.\n")
                    print(
                        tabulate(
                            [["", "", ""]],
                            headers=[student["id"], student["name"], student["grade"]],
                            tablefmt="simple",
                        )
                    )

                    if len(student["solution"]) > 0:
                        print(f"-> Solution:\n          {student["solution"]}\n")
                        grade = cls.get_string(
                            question="Select a grade for the student from 0 to 100: "
                        )
                        if int(grade) > 100 or int(grade) < 0:
                            raise IndentationError
                        super().clear_screen()
                        student["grade"] = grade.strip().zfill(2) + " / 100"
                        cls.save_class_data(
                            data_object=course,
                            save_as=course.course_code,
                            folder_path=COURSE_OBJECTS_FOLDER,
                        )
                        print("Grade was assigned successfully.")
                        cls.view_assignment(assignment, course)
                        break
                    else:
                        print("No solution has been submitted yet.")

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                print("No grade was assigned.")
                cls.view_assignment(assignment, course)
                break
            except IndentationError:
                super().clear_screen()
                print("Please choose a value between 0 and 100.")
            except ValueError:
                super().clear_screen()
                print("Please type an integer.")

    @classmethod
    def edit_password(cls):
        """Asks the user for a new password and checks
        if it's valid according to the specified criteria."""

        try:
            print(Project_art.profile)
            print("To return to profile page, press 'Ctrl + C'.")
            print("Please enter the new password in the password field.")

            user = super().login_user_object
            new_password = super().get_password()
            user.password = new_password
            super().save_class_data(
                data_object=user, save_as=user.username, folder_path=USER_OBJECTS_FOLDER
            )

            super().clear_screen()
            print("Password has been changed succesfully.")
            cls.prof_profile()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            print("Password has not been changed!")
            cls.prof_profile()

    @classmethod
    def edit_question(cls):
        try:
            print(Project_art.profile)
            print("To return to profile page, press 'Ctrl + C'.")
            print("Please enter the question and answer in the specified fields below.")

            user = super().login_user_object
            new_question, new_answer = super().get_question()
            user.question = new_question
            user.answer = new_answer
            super().save_class_data(
                data_object=user, save_as=user.username, folder_path=USER_OBJECTS_FOLDER
            )

            super().clear_screen()
            print("Verification Question & Answer have been changed succesfully.")
            cls.prof_profile()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            print("Verification Question & Answer have not been changed!")
            cls.prof_profile()

    @classmethod
    def view_course(cls, course: Course):
        """Views the course details, such as the number
        of enrolled students, description, etc.,
        and provides an option to delete the course."""

        try:
            print(Project_art.course_overview)
            print(
                "To return to courses list, press 'Ctrl + C'.",
                "To view an assignment, create a new one, or delete the course, please make a choice.",
                f"   -> Course Title: {course.course_title}",
                f"   -> Course Code: {course.course_code}",
                f"   -> Assignments Number: {len(course.course_assignments)}",
                f"   -> Students Number: {len(course.enrolled_students)}\n",
                sep="\n",
            )

            print(
                tabulate(
                    [["", ""]],
                    headers=["- Course Description: ", course.course_description],
                    tablefmt="simple",
                )
            )

            if len(course.enrolled_students) > 0:
                header = ["", "Student ID", "Student Name"]
                students_table = []
                index = 1
                for student in course.enrolled_students:
                    students_table.append(
                        [str(index).zfill(2), student["id"], student["name"]]
                    )
                    index += 1
                print(tabulate(students_table, headers=header, tablefmt="simple"))
                print()
            elif len(course.enrolled_students) == 0:
                print("- There are no students enrolled in this course yet.")

            print(
                "  1 - List Assignments",
                "  2 - Create Assignment",
                "  3 - Delete Course\n",
                sep="\n",
            )
            choice: int = super().get_choice(3)
            match choice:
                case 1:
                    super().clear_screen()
                    cls.list_assignments(course)
                case 2:
                    super().clear_screen()
                    cls.create_assignment(course)
                case 3:
                    with open(COURSES_LIST_PATH, "r") as file:
                        codes_list = file.readlines()[1:]
                        for code in codes_list:
                            if (
                                code.strip().lower()
                                == course.course_code.strip().lower()
                            ):
                                codes_list.remove(code)

                    with open(COURSES_LIST_PATH, "w") as file:
                        for data in codes_list:
                            file.write(f"\n{data.strip()}")

                    if len(codes_list) == 0:
                        os.remove(COURSES_LIST_PATH)

                    os.remove(f"{COURSE_OBJECTS_FOLDER}/{course.course_code}_data.pkl")
                    super().clear_screen()
                    cls.list_courses()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            cls.list_courses()

    @classmethod
    def load_courses_data(cls):
        """Loads the courses data when opening the app."""

        # i refactored the load_user_data method to be this, due to the diffrent
        # data used in it so i couldn't take the danger and try to edit on it to use
        # it with super() like what i did with save_class_data and save_list_file

        cls.courses = []
        try:
            with open(COURSES_LIST_PATH, "r") as file:
                courses = [name.strip() for name in file.readlines()[1:]]
                for course in courses:
                    with open(
                        f"{COURSE_OBJECTS_FOLDER}/{course}_data.pkl", "rb"
                    ) as data:
                        cls.courses.append(pickle.load(data))

        except FileNotFoundError:
            pass
        except (KeyboardInterrupt, EOFError):
            pass

    @classmethod
    def get_course_code(cls) -> str:
        """Generates a course code using a specific algorithm."""

        # CS0-random00sort- 0random
        course_code = "CS"
        nums = [str(num) for num in range(10)]
        course_code += random.choice(nums)
        cls.load_courses_data()

        if len(cls.courses) == 0:
            course_code += "01"
        else:
            course_code += str(len(cls.courses) + 1).zfill(2)
        course_code += random.choice(nums)
        return course_code

    @classmethod
    def current_prof_courses(cls) -> list:
        """Returns the current professor's course objects in a list."""

        cls.load_courses_data()
        current_prof_id = super().login_user_object.id
        current_prof_courses = []
        for course in cls.courses:
            if course.course_prof_id == current_prof_id:
                current_prof_courses.append(course)
        return current_prof_courses
