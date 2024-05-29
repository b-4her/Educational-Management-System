"""
Students portal allows students to
easily access their courses, enroll or unenroll as 
needed, and submit assignments directly 
through the portal. Additionally, 
they have the ability to view their grades and 
track their academic progress over time. 
The portal also provides students with access to their
profile information, allowing them to update password
and verification question. 
"""

# Please note that several errors raised in the
# file are randomly chosen to handle specific cases.

from prof_portal import ProfPortal  # Inheriting some methods
import Project_art  # Project-specific art elements
from tabulate import tabulate  # Making nice looking tables of data
from courses import Course  # Used in type hints
import sys # exit

COURSES_LIST_PATH = r"Courses_Data/courses_list.txt"
COURSE_OBJECTS_FOLDER = "Courses_Data"
USERNAMES_LIST_PATH = r"Users/usernames_list.txt"
USER_OBJECTS_FOLDER = "Users"


# Inherets ProfPortal and MainMenu classes.
class StudentPortal(ProfPortal):
    """
    Students portal allows students to
    easily access their courses, enroll or unenroll as
    needed, and submit assignments directly
    through the portal. Additionally,
    they have the ability to view their grades and
    track their academic progress over time.
    The portal also provides students with access to their
    profile information, allowing them to update password
    and verification question.
    """

    @classmethod
    def student_portal_menu(cls):
        """This method enables students to select from specified choices
        such as accessing their profile, logging out, and more."""

        try:
            print(Project_art.student_portal)
            print(
                "Please make a choice:",
                "   1 - List My Courses",
                "   2 - Register in a Course",
                "   3 - Profile",
                "   4 - Exit",
                sep="\n",
            )
            main_choice: int = super().get_choice(num_of_choices=4)

            match main_choice:
                case 1:
                    super().clear_screen()
                    cls.list_my_courses()
                case 2:
                    super().clear_screen()
                    cls.course_register()
                case 3:
                    super().clear_screen()
                    cls.student_profile()
                case 4:
                    super().clear_screen()
                    sys.exit()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            cls.student_portal_menu()

    @classmethod
    def course_register(cls):
        """This functionality enables students to register for
        a course by selecting it from a list of available options."""

        n = 1  # to prevent the loop from printing the table infinite times
        while True:
            try:
                if n == 1:
                    n += 1
                    print(Project_art.register_course)

                    current_student_courses = cls.student_registered_courses()
                    courses_can_be_registered = []
                    for course in cls.courses:
                        if course not in current_student_courses:
                            courses_can_be_registered.append(course)

                    if len(courses_can_be_registered) > 0:
                        print("Please pick a course to register for.")
                    print("To return to the main menu, press 'Ctrl + C'.\n")

                    table = []
                    headers = [
                        "",
                        "Title",
                        "Code",
                        "Professor Name",
                        "Assignments Number",
                        "Regestered Students Number",
                    ]

                    if len(courses_can_be_registered) == 0:
                        table.append(["", "None", "None", "None", "None", "None"])
                    elif len(courses_can_be_registered) > 0:
                        index = 1
                        for course in courses_can_be_registered:
                            data = []
                            data.append(str(index).zfill(2))
                            index += 1  # 0th course in courses
                            data.append(course.course_title)
                            data.append(course.course_code)
                            data.append(course.course_prof)
                            data.append(str(len(course.course_assignments)).zfill(2))
                            data.append(str(len(course.enrolled_students)).zfill(2))
                            table.append(data)

                    print(tabulate(table, headers, tablefmt="simple"))
                    print()  # to add empty line

                    if len(courses_can_be_registered) == 0:
                        print("There are no courses you can register.")
                    elif (
                        len(courses_can_be_registered) > 0
                    ):  # add student to enrolled students
                        choice: int = super().get_choice(len(table))
                        registered_course = courses_can_be_registered[choice - 1]
                        current_student = super().login_user_object
                        registered_course.enrolled_students.append(
                            {
                                "name": current_student.full_name,
                                "id": current_student.id,
                            }
                        )

                        if len(registered_course.course_assignments) > 0:
                            for assignment in registered_course.course_assignments:
                                assignment["students"].append(
                                    {
                                        "name": current_student.full_name,
                                        "id": current_student.id,
                                        "grade": "NA / 100",
                                        "solution": "",
                                    }
                                )

                        cls.save_class_data(
                            data_object=registered_course,
                            save_as=registered_course.course_code,
                            folder_path=COURSE_OBJECTS_FOLDER,
                        )
                        super().clear_screen()
                        print("Course has been succefully regestered.")
                        cls.course_register()
                        break

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                print("No courses have been registered.")
                cls.student_portal_menu()
                break

    @classmethod
    def list_my_courses(cls):
        """This method allows students to view the courses
        they have enrolled in and provides an option
        to see the details of each course."""

        n = 1
        while True:
            try:
                if n == 1:
                    n += 1
                    print(Project_art.my_courses)

                    current_student_courses = cls.student_registered_courses()
                    if len(current_student_courses) > 0:
                        print("To view a course assignmetns, please make a choice")
                    print("To return to the main menu, press 'Ctrl + C'.\n")
                    table = []
                    headers = [
                        "",
                        "Title",
                        "Code",
                        "Professor Name",
                        "Assignments Number",
                        "Regestered Students Number",
                    ]

                    if len(current_student_courses) == 0:
                        table.append(["", "None", "None", "None", "None", "None"])
                    elif len(current_student_courses) > 0:
                        index = 1

                        for course in current_student_courses:
                            data = []
                            data.append(str(index).zfill(2))
                            index += 1  # 0th course in courses
                            data.append(course.course_title)
                            data.append(course.course_code)
                            data.append(course.course_prof)
                            data.append(str(len(course.course_assignments)).zfill(2))
                            data.append(str(len(course.enrolled_students)).zfill(2))
                            table.append(data)

                    print(tabulate(table, headers, tablefmt="simple"))
                    print()  # to add empty line

                    if len(current_student_courses) == 0:
                        print(
                            "There are no courses available to view. Please register for courses first."
                        )
                    elif (
                        len(current_student_courses) > 0
                    ):  # add student to enrolled students
                        choice: int = super().get_choice(len(table))
                        course_to_view = current_student_courses[choice - 1]
                        super().clear_screen()
                        cls.view_my_course(course_to_view)
                        break

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.student_portal_menu()
                break

    @classmethod
    def view_my_course(cls, course: Course):
        """This method displays specific details of a course
        to the student, such as the professor's name,
        a list of assignments, and more. It also provides
        options to view the details of an assignment
        and to delete the course."""

        while True:
            try:
                assignments = course.course_assignments
                print(Project_art.course_overview)
                if len(assignments) > 0:
                    print("To view an assignment details, please make a choice.")

                print(
                    "To return to courses list, press 'Ctrl + C'.",
                    f"   -> Course Title: {course.course_title}",
                    f"   -> Course Code: {course.course_code}",
                    f"   -> Course Code: {course.course_prof}",
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

                _student = None  # this one has the solution info and grade
                student = None  # this one does not have the solution info
                for student in course.enrolled_students:
                    if student["id"] == cls.login_user_object.id:
                        student = student

                table = []
                headers = ["", "Assignment", "Description", "Grade"]
                if len(assignments) == 0:
                    table.append(["", "None", "None"])
                elif len(assignments) > 0:
                    index = 1
                    for assignment in assignments:
                        data = []

                        student_grade = ""  # checking the student grade
                        current_student_id = super().login_user_object.id
                        for student_info in assignment["students"]:
                            if student_info["id"] == current_student_id:
                                student_grade = student_info["grade"]

                        data.append(str(index).zfill(2))
                        index += 1
                        data.append(assignment["name"])
                        data.append(assignment["description"])
                        data.append(student_grade)
                        table.append(data)

                print(tabulate(table, headers, tablefmt="simple"))
                print()

                if len(assignments) == 0:
                    print("There are no assignments to view.\n")
                    print("To unregister from the course, please type '1'.\n")
                    choice: int = super().get_choice(1)
                    super().clear_screen()
                    course.enrolled_students.remove(student)
                    cls.save_class_data(
                        data_object=course,
                        save_as=course.course_code,
                        folder_path=COURSE_OBJECTS_FOLDER,
                    )
                    super().clear_screen()
                    cls.list_my_courses()
                elif len(assignments) > 0:
                    print(
                        f"To unregister from the course, please type '{str(len(table) + 1).zfill(2)}'.\n"
                    )
                    choice: int = super().get_choice(len(table) + 1)
                    super().clear_screen()



                    if choice == len(table) + 1:
                        course.enrolled_students.remove(student) 
                        # deleting student from enrolled students list

                        # deleting the student solution and grade from the assignments
                        for assignment in assignments:
                            for assignment_student in assignment["students"]:
                                if assignment_student["id"] == super().login_user_object.id:
                                    assignment["students"].remove(assignment_student)                                    

                        cls.save_class_data(
                            data_object=course,
                            save_as=course.course_code,
                            folder_path=COURSE_OBJECTS_FOLDER,
                        )
                        super().clear_screen()
                        cls.list_my_courses()
                    else:
                        current_assignment = assignments[choice - 1]
                        for assignment_student in current_assignment["students"]:
                            if assignment_student["id"] == super().login_user_object.id:
                                _student = assignment_student

                        cls.view_my_assignment(assignments[choice - 1], course, _student) # type: ignore

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.list_my_courses()

    @classmethod
    def student_profile(cls):
        """This feature enables students to view their account
        information, including the number of courses enrolled in,
        password, username, etc. It also provides options
        to change the password or the verification question."""

        try:
            print(Project_art.profile)
            print(
                "To return to the main menu, press 'Ctrl + C'.",
                "For any other operation please make a choice.",
                f"   -> Student ID: {super().login_user_object.id}",
                f"   -> Full Name: {super().login_user_object.full_name}",
                f"   -> Courses regiestered in number: {str(len(cls.student_registered_courses())).zfill(2)}",
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
            cls.student_portal_menu()

    @classmethod
    def edit_password(cls):
        """This function prompts the student to enter
        a new password and verifies if it meets specific criteria."""

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
            cls.student_profile()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            print("Password has not been changed!")
            cls.student_profile()

    @classmethod
    def view_my_assignment(cls, assignment: dict, course: Course, student: dict):
        """This function displays the details of an assignment, offering
        an option for the student to submit a solution."""

        while True:
            try:
                print(Project_art.view_assignment)
                print("To return to course overview, press 'Ctrl + C'.")

                if len(student["solution"]) == 0:
                    print("To submit a solution, please type '1'.\n")
                else:
                    print("To submit a new solution, please type '1'.\n")

                print(
                    tabulate(
                        [
                            [
                                assignment["name"],
                                assignment["description"],
                                student["grade"],
                            ]
                        ],
                        headers=["Assignment Name", "Description", "Grade"],
                        tablefmt="simple",
                    )
                )

                if len(student["solution"]) > 0:
                    print(f"\n-> Solution:\n          {student["solution"]}\n")
                else:
                    print("\nNo solution has been submitted yet.\n")

                super().get_choice(1)
                super().clear_screen()
                cls.submit_solution(assignment, course, student)
                break

            except (KeyboardInterrupt, EOFError):
                super().clear_screen()
                cls.view_my_course(course)
                break

    @classmethod
    def edit_question(cls):
        """This function prompts the student to type a
        new question and answer, ensuring that they
        type at least one character for each."""

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
            cls.student_profile()

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            print("Verification Question & Answer have not been changed!")
            cls.student_profile()

    @classmethod
    def submit_solution(cls, assignment: dict, course: Course, student: dict):
        """This function prompts the student to submit a solution,
        ensuring that they type at least one character
        in it before proceeding."""

        try:
            print(Project_art.solution_submission)
            solution = super().get_string("-> Solution: ")
            student["solution"] = solution

            cls.save_class_data(
                data_object=course,
                save_as=course.course_code,
                folder_path=COURSE_OBJECTS_FOLDER,
            )
            super().clear_screen()
            print("Solution was submitted succesfully.")
            cls.view_my_assignment(assignment, course, student)

        except (KeyboardInterrupt, EOFError):
            super().clear_screen()
            cls.view_my_assignment(assignment, course, student)

    @classmethod
    def student_registered_courses(cls):
        """This function returns a list containing the objects
        of the courses that the student has enrolled in."""

        cls.load_courses_data()
        current_student_id = super().login_user_object.id
        current_student_courses = []

        for course in cls.courses:
            for student in course.enrolled_students:
                if student["id"] == current_student_id:
                    current_student_courses.append(course)

        return current_student_courses
