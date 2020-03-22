from MakeData import *

Lecturer_Expertise = make_dict("Lecturer Expertise.xlsx")
Lecturer_Free = make_dict("Lecturer Free.xlsx")
Classroom_Free = make_dict("Classroom Occupancy.xlsx")
Lecture_Hours = make_dict("Lecture Hours.xlsx")
Lecture_Times = make_dict("Lecture_Times.xlsx")
Course_Lectures = make_dict("Course_Lectures.xlsx")
Course_Free = make_dict("Course Free.xlsx")
Lab_Free = make_dict("Labs Occupancy.xlsx")
Labs = make_dict("Labs.xlsx")
Lecturer_Free = lunchtime(Lecturer_Free)
Courses = list(Course_Lectures.keys())[1:]

Lecturer_Names = list(Lecturer_Expertise.keys())[1:]
Subject_Names = Lecturer_Expertise['Subjects']
Course_Subjects = one(Course_Lectures, Courses, Subject_Names)
Classrooms = list(Classroom_Free.keys())[1:]
Lecturer_Subjects = one(Lecturer_Expertise, Lecturer_Names, Subject_Names)
lectures = []
for subject in Subject_Names:
    for i in range((Lecture_Hours[subject][0])):
        lectures.append(subject)
Lab_Hours, Lab_Subjects, Subject_Lab = make_lab(Lab_Free, Labs, Subject_Names)
Lab_Names = list(Lab_Hours.keys())
Labs_list = list(Lab_Free.keys())[1:]
Subjects_Labs = {k: v for k, v in (one(Labs, Subject_Names, Labs_list)).items() if v}

Subject_Courses = {}
for subject in Subject_Names:
    Subject_Courses.update({subject: get_keys(Course_Subjects, subject)})
lectures.extend(list(Subject_Lab.keys()))
df = timetable(lectures, Lecturer_Subjects, Lecturer_Free, Classroom_Free, Classrooms, Lecture_Times, Subject_Courses,
               Lecturer_Expertise, Course_Free, Subject_Names, Subject_Lab, Lab_Free, Subjects_Labs)

"""

Time = Lecture_Times['Time']

Lecturer_Free_Times = one(Lecturer_Free, Lecturer_Names, Time)
Classroom_Times = one(Classroom_Free, Classrooms, Time)
Lecture_Free_Times = one(Lecture_Times, Subject_Names, Time)



"""
