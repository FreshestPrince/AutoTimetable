import random
import time
import pandas as pd
import datetime
from functions import *

labs = "SEEE Labs 2019-20.xlsx"
main_data = "Timetabling EB03 Data Sample 201920.xlsx"
data = pd.read_excel(main_data, "Sheet1")
rooms = pd.read_excel(labs, "Sheet1")
data_dict = data.to_dict("list")

Subjects_Lecturers, lecturer_list, lecturers = lecturers(data_dict)
Course_Size, courses, courses_list, Subject_Courses, course_dict = courses(data_dict)
Subject_Length, ID_Subject, all_rooms, Classroom_Size = make_data(data_dict, rooms)

Course_Subjects = make_dict(courses, Subject_Courses)
lectures_sem_1 = Course_Subject(Course_Subjects)
Lecturer_Subjects = make_dict(lecturers, Subjects_Lecturers)
generations = 2
population = 1
clashes_dict = {}
len_dict = {}
t0 = time.time()
lectures, Subject_Hours = create_lectures(1, Subject_Length, lectures_sem_1)
subject_size, suitable_classrooms, lecture_classrooms = classroom_sizes(Subject_Courses, Course_Size, Classroom_Size,
                                                                        lectures)

random.shuffle(lectures)
time_list = []
lecturer_hours = 18
timetables = getInitialPopulation(lectures, Lecturer_Subjects, population, Subject_Courses, subject_size,
                                  Classroom_Size, lecture_classrooms, ID_Subject)

classroom_free, classroom_taken = classrooms_free(timetables, all_rooms)
lecturer_free, lecturer_taken = lecturers_free(timetables, lecturers)
first_half, second_half = split_halves(timetables)
first_half = mutate(first_half, classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects, lecture_classrooms)[0]
second_half = mutate(second_half, classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects, lecture_classrooms)[
    0]
timetables = first_half + second_half

chromosome, classroom_free, lecturer_free = mutate(timetables, classroom_free, lecturer_free, lecturer_hours,
                                                   Lecturer_Subjects, lecture_classrooms)
t1 = time.time()
df = pd.DataFrame(chromosome)
columns = ['Time', 'Room', 'Lecturer', 'Lecture_ID', 'Course(s)', 'StudentsNo', 'Room Size', 'Lecture']
df.columns = columns
df.to_excel("test.xlsx")
total = t1 - t0
print(str(datetime.timedelta(seconds=total)))
