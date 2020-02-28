from MakeData import *

Lecture_Hours = make_dict("Lecture Hours.xlsx")
Lecturer_Expertise = make_dict("Lecturer Expertise.xlsx")
Lecturer_Free = make_dict("Lecturer Free.xlsx")
Classroom_Free = make_dict("Classroom Occupancy.xlsx")
classroom = (find_classroom_and_lecturer(Lecture_Hours, Lecturer_Expertise, Lecturer_Free, Classroom_Free))
