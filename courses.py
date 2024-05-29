"""This class serves as a data structure designed 
to be used with the pickle library for saving 
courses' data, replacing the need for a CSV file."""


class Course:
    """This class serves as a data structure designed
    to be used with the pickle library for saving
    users' data, replacing the need for a CSV file."""

    def __init__(
        self,
        course_title: str, 
        course_code: str,
        course_prof_id: str,
        course_description: str,
        course_prof: str,
    ):

        self.course_title: str = course_title
        self.course_description: str = course_description
        self.course_code: str = course_code
        self.course_prof: str = course_prof
        self.course_prof_id: str = course_prof_id
        self.enrolled_students: list = []
        self.course_assignments: list = []

    def __str__(self):
        return f"'{self.course_title}', is a course object created by professor {self.course_prof}."


#* The Structures of enrolled_students and course_assignments 
#* viewing two student enrolled in a course
#* while there is only one assignment :

# enrolled_students = [
#     {"name" : "David", "id" : "09876542"},
#     {"name" : "Joseph", "id" : "76540987"},
# ]

# course_assignments = [{     #* this is only one assignment 
#     "name" : "assignment1", 
#     "description" : "This a test assignment", 
#     "students" : [
#         {"name" : "David", "id" : "09876542", "grade": "NA / 100", "solution" : "..."},
#         {"name" : "Joseph", "id" : "76540987", "grade": "NA / 100", "solution" : "..."},
#     ]
# }]
