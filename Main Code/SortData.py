from MakeData import *

Lecturer_Expertise = make_dict("Lecturer Expertise.xlsx")
Lecturer_Free = make_dict("Lecturer Free.xlsx")
Classroom_Free = make_dict("Classroom Occupancy.xlsx")
Lecture_Hours = make_dict("Lecture Hours.xlsx")
Lecture_Times = make_dict("Lecture_Times.xlsx")
Course_Lectures = make_dict("Course_Lecturers.xlsx")
Lecturer_Free = lunchtime(Lecturer_Free)
Lecture_Times = lunchtime(Lecture_Times)
Classroom_Free = lunchtime(Classroom_Free)


Lecturer_Names = list(Lecturer_Expertise.keys())[1:]
Subject_Names = Lecturer_Expertise['Subjects']
Classrooms = list(Classroom_Free.keys())[1:]

Lecturer_Subjects = one(Lecturer_Expertise, Lecturer_Names, Subject_Names)
lectures = []
for subject in Subject_Names:
    for i in range((Lecture_Hours[subject][0])):
        lectures.append(subject)



"""
Courses = list(Course_Lectures.keys())[1:]
Time = Lecture_Times['Time']

Lecturer_Free_Times = one(Lecturer_Free, Lecturer_Names, Time)
Classroom_Times = one(Classroom_Free, Classrooms, Time)
Lecture_Free_Times = one(Lecture_Times, Subject_Names, Time)
Course_Subjects = one(Course_Lectures, Courses, Subject_Names)

Subject_Lecturers = {}
for subject in lectures:
    lecturers_list = get_keys(Lecturer_Subjects, subject)
    Subject_Lecturers.update({subject: lecturers_list})
"""
