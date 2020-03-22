import pandas as pd
from random import randrange, choice


def make_dict(workbook):
    return pd.read_excel(workbook, "Sheet1").to_dict("list")


def make_lab(Lab_Free, Labs, Subject_Names):
    Lab_Hours = {}
    Subject_Lab = {}
    Lab_Subjects = []
    Labs_list = list(Lab_Free.keys())[1:]
    subjects_labs = {k: v for k, v in (one(Labs, Subject_Names, Labs_list)).items() if v}
    for subject in Subject_Names:
        if subject in subjects_labs:
            lab = subject + "-Lab"
            Lab_Subjects.append(subject)
            Lab_Hours.update({lab: 2})
            Subject_Lab.update({lab: subject})
    return Lab_Hours, Lab_Subjects, Subject_Lab


def lunchtime(Lecturer_Free):
    names = list(Lecturer_Free.keys())[1:]
    n = 3
    for name in names:
        while n < 65:
            Lecturer_Free[name][n] = 0
            n += 13 + randrange(0, 3)
    return Lecturer_Free


def time_normal(number):
    while 0 < number > 12:
        number -= 13
    if number == 0:
        return 9
    elif number == 1:
        return 10
    elif number == 2:
        return 11
    elif number == 3:
        return 12
    elif number == 4:
        return 13
    elif number == 5:
        return 14
    elif number == 6:
        return 15
    elif number == 7:
        return 16
    elif number == 8:
        return 17
    elif number == 9:
        return 18
    elif number == 10:
        return 19
    elif number == 11:
        return 20
    elif number == 12:
        return 21


def time_translate(number):
    if number < 13:
        return ("Monday", time_normal(number))
    elif 26 > number:
        return ("Tuesday", time_normal(number))
    elif 39 > number:
        return ("Wednesday", time_normal(number))
    elif 52 > number:
        return ("Thursday", time_normal(number))
    elif 65 > number:
        return ("Friday", time_normal(number))
    else:
        print("Value is not within proper range")
        return 0


def one(data, names1, names2):
    data_dict = {}
    for name in names1:
        lst = []
        numbers = data[name]
        index = 0
        while index < len(numbers):
            if numbers[index] == 1:
                lst.append(names2[index])
                index += 1
            else:
                index += 1
        data_dict.update({name: lst})
    return data_dict


def zeros(Lecturer_Free, name):
    zeros = len([i for i, x in enumerate(Lecturer_Free[name]) if x == 0])
    return zeros


def get_keys(data, name):
    keys = [key for key, value in data.items() if name in value]
    return keys


def make_zero(data, name, time):
    data[name][time] = 0


def make_zero_courses(data, courses, time):
    for course in courses:
        data[course][time] = 0


"""
def check_free_lab(Lab_Subjects, Subjects_Labs, Lab_Free, time):
    for subject in Lab_Subjects:
        lab = choice(Subjects_Labs[subject])
        if Lab_Free[lab][time] == 1:
            return True
        else:
            return False
"""


def check_free(data, name, time):
    if data[name][time] == 1:
        return True
    else:
        return False


def check_free_classroom(data, time, Classrooms):
    free = []
    for name in Classrooms:
        if data[name][time] == 1:
            free.append(name)
    return free


def check_free_lecturer(Lecturer_Subjects, time, Lecturer_Free, Lecturer_Expertise):
    free = []
    lst = list(Lecturer_Free.keys())[1:]
    for lecturer in lst:
        lecturer_hours = zeros(Lecturer_Free, lecturer)
        if lecturer_hours > 18:
            del_keys(Lecturer_Free, Lecturer_Expertise, Lecturer_Subjects, lecturer)
            lst.remove(lecturer)
            continue
        if Lecturer_Free[lecturer][time] == 1:
            free.append(lecturer)
    return free


def check_expertise(lecture, lecturers, Subject_Names, Lecturer_Subjects):
    Subject_Lecturers = {}
    free_lecturers = []
    for subject in Subject_Names:
        lecturers_list = get_keys(Lecturer_Subjects, subject)
        Subject_Lecturers.update({subject: lecturers_list})
    for lecturer in lecturers:
        if lecturer in Subject_Lecturers[lecture]:
            free_lecturers.append(lecturer)
    return free_lecturers


def del_keys(Lecturer_Free, Lecturer_Expertise, Lecturer_Subjects, lecturer):
    lecturer_hours = zeros(Lecturer_Free, lecturer)
    if lecturer_hours > 18:
        del Lecturer_Free[lecturer]
        del Lecturer_Expertise[lecturer]
        del Lecturer_Subjects[lecturer]


def check_dicts(Course_Free, items, time):
    free = []
    for item in items:
        free.append(Course_Free[item][time])
    if all(x == 1 for x in free):
        return True
    else:
        return False


def check_free_lab(lab, time, Subject_Lab, Lab_Free, Subjects_Labs):
    free_labs = []
    lab_name = Subject_Lab[lab]
    for labs in Subjects_Labs[lab_name]:
        if Lab_Free[labs][time] == 1:
            free_labs.append(labs)
    return free_labs


def check_free_lab_lecturer(lab, time, Subject_Lab, Lecturer_Free, Lecturer_Subjects):
    free = []
    free_lecturers = []
    lab_name = Subject_Lab[lab]
    lecturers_list = get_keys(Lecturer_Subjects, lab_name)
    for labs in lecturers_list:
        if Lecturer_Free[labs][time] == 1:
            free.append(labs)
    if len(free) > 0:
        for lecturer in free:
            if lab_name in Lecturer_Subjects[lecturer]:
                free_lecturers.append(lecturer)
    return free_lecturers


def timetable(lectures, Lecturer_Subjects, Lecturer_Free, Classroom_Free, Classrooms, Lecture_Times, Subject_Courses,
              Lecturer_Expertise, Course_Free, Subject_Names, Subject_Lab, Lab_Free, Subjects_Labs):
    lst = []
    for lecture in lectures:
        time = 0
        if (lecture[-4:]) == "-Lab":
            while time < 65:
                lab = check_free_lab(lecture, time, Subject_Lab, Lab_Free, Subjects_Labs)
                lecturer = check_free_lab_lecturer(lecture, time, Subject_Lab, Lecturer_Free, Lecturer_Subjects)
                courses = Subject_Courses[lecture[0:-4]]
                if len(lecturer) > 0 and len(lab) > 0 and len(courses) > 0:
                    lecturer = choice(lecturer)
                    lab = choice(lab)
                    make_zero(Lab_Free, lab, time)
                    make_zero(Lab_Free, lab, time+1)
                    make_zero(Lecturer_Free, lecturer, time)
                    make_zero(Lecturer_Free, lecturer, time+1)
                    make_zero_courses(Course_Free, courses, time)
                    lst.append(
                        [time, time_translate(time)[0], time_translate(time)[1], lab, lecturer, lecture, "Lab",
                         courses])
                    lst.append(
                        [time+1, time_translate(time)[0], time_translate(time)[1], lab, lecturer, lecture, "Lab",
                         courses])
                    time += 2
                    break
                time += 1
        else:
            while time < 65:
                lecturers = check_free_lecturer(Lecturer_Subjects, time, Lecturer_Free, Lecturer_Expertise)
                free_lecturers = check_expertise(lecture, lecturers, Subject_Names, Lecturer_Subjects)
                classrooms = check_free_classroom(Classroom_Free, time, Classrooms)
                courses = Subject_Courses[lecture]
                if len(classrooms) > 0 and len(free_lecturers) > 0 and (
                        check_dicts(Course_Free, courses, time)) == True and len(
                    courses) > 0:
                    lecturer = choice(free_lecturers)
                    classroom = choice(classrooms)
                    lst.append(
                        [time, time_translate(time)[0], time_translate(time)[1], classroom, lecturer, lecture,
                         "Lecture", courses])
                    make_zero(Lecture_Times, lecture, time)
                    make_zero(Lecturer_Free, lecturer, time)
                    make_zero(Classroom_Free, classroom, time)
                    make_zero_courses(Course_Free, courses, time)
                    time += 1
                    break
                time += 1
    df = pd.DataFrame.from_records(lst)
    df.columns = ["Number", "Day", "Time", "Classroom", "Lecturer", "Lecture", "Type", "Courses"]
    df.to_excel("Timetable.xlsx")
    return df
