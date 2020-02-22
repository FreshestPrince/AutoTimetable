from Scripts.MakeData import *

Lecture_Hours = make_dict("Lecture Hours.xlsx")
Lecturer_Expertise = make_dict("Lecturer Expertise.xlsx")
Lecturer_Free = make_dict("Lecturer Free.xlsx")
Classroom = make_dict("Classroom.xlsx")

free_lecturer = lecturer_available_time(Lecture_Hours, Lecturer_Expertise, Lecturer_Free, "Analogue Electronics", 9)
print(free_lecturer[0])

