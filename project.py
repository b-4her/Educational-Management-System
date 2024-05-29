from main_menu import MainMenu
from student_portal import StudentPortal
from prof_portal import ProfPortal


def main():
    MainMenu.start_portal()  # starting app

    current_user = MainMenu.login_user_object
    go_to_portal(current_user)


def go_to_portal(current_user):
    if current_user.account_type.lower() == "student":
        StudentPortal.student_portal_menu()
    elif current_user.account_type.lower() == "professor":
        ProfPortal.prof_main_portal()


if __name__ == "__main__":
    main()
