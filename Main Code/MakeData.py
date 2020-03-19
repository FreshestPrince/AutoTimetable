import pandas as pd
from random import randrange, choice


def make_dict(workbook):
    return pd.read_excel(workbook, "Sheet1").to_dict("list")


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


def del_keys(Lecturer_Free, Lecturer_Expertise, Lecturer_Subjects, lecturer):
    lecturer_hours = zeros(Lecturer_Free, lecturer)
    if lecturer_hours > 18:
        del Lecturer_Free[lecturer]
        del Lecturer_Expertise[lecturer]
        del Lecturer_Subjects[lecturer]


def timetable(lectures, Lecturer_Subjects, Lecturer_Free, Classroom_Free, Classrooms, Lecture_Times,
              Lecturer_Expertise):
    lst = []
    for lecture in lectures:
        time = 0
        while time < 65:
            lecturers = check_free_lecturer(Lecturer_Subjects, time, Lecturer_Free, Lecturer_Expertise)
            classrooms = check_free_classroom(Classroom_Free, time, Classrooms)
            if len(classrooms) > 0 and len(lecturers) > 0:
                lecturer = choice(lecturers)
                classroom = choice(classrooms)
                lst.append([time, time_translate(time)[0], time_translate(time)[1], classroom, lecturer, lecture])
                make_zero(Lecture_Times, lecture, time)
                make_zero(Lecturer_Free, lecturer, time)
                make_zero(Classroom_Free, classroom, time)
                time += 1
                break
            time += 1
    df = pd.DataFrame.from_records(lst)
    df.columns = ["Number", "Day", "Time", "Classroom", "Lecturer", "Lecture"]
    df.to_excel("Timetable.xlsx")
    return df