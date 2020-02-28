from openpyxl import load_workbook
import pandas as pd


def make_dict(workbook):
    rows = 1
    columns = 1
    wb = load_workbook(workbook, read_only=True)
    sheet = wb.worksheets[0]
    row_count = sheet.max_row
    column_count = sheet.max_column - 1
    listfolders = []
    while rows <= row_count:
        while columns <= column_count:
            name = sheet.cell(row=rows, column=columns).value
            df = pd.read_excel(workbook)  # can also index sheet by name or fetch all sheets
            mylist = df[name].tolist()
            listfolders.append(mylist)
            columns += 1
        rows += 1
    num = 0
    new_list = []
    while num < len(listfolders):
        data = listfolders[num]
        new_list.append({data[0]: data[1:]})
        num += 1
    return new_list


def duplicates(lst, item):
    lst = (list(lst.values())[0])
    return [i for i, x in enumerate(lst) if x == item]


def lecturer_subject(data, subject):
    lst = (list(data[0].values())[0].index(subject))
    lecturer = []
    for info in data:
        for name in info:
            if (list(info.values())[0][lst]) == 1:
                lecturer.append(name)
    return lecturer


def lecturer_free(data, name, time):
    lst = []
    for item in data:
        for key in item.keys():
            lst.append(key)
    no = lst.index(name)

    free = list(data[no].values())[0][time]
    if free == 1:
        return True
    else:
        return False


def class_free(data, time):
    if list(data[1].values())[0][time] == 1:
        return True
    else:
        return False


def time_normal(number):
    while 0 < number > 13:
        number -= 13
    if number == 1:
        return 9
    elif number == 2:
        return 10
    elif number == 3:
        return 11
    elif number == 4:
        return 12
    elif number == 5:
        return 13
    elif number == 6:
        return 14
    elif number == 7:
        return 15
    elif number == 8:
        return 16
    elif number == 9:
        return 17
    elif number == 10:
        return 18
    elif number == 11:
        return 19
    elif number == 12:
        return 20
    elif number == 13:
        return 21


def time_translate(number):
    if number < 14:
        return ("Monday", time_normal(number))
    elif 27 > number > 14:
        return ("Tuesday", time_normal(number))
    elif 40 > number > 27:
        return ("Wednesday", time_normal(number))
    elif 53 > number > 40:
        return ("Thursday", time_normal(number))
    elif 66 > number > 53:
        return ("Friday", time_normal(number))
    else:
        print("Value is not within proper range")
        return 0


def lecturer_available_time(Lecture_Hours, Lecturer_Expertise, Lecturer_Free, subject, time):
    subject_list = []
    for item in Lecture_Hours:
        list_of_lists = (list(item.keys()))
        for x in list_of_lists:
            subject_list.append(x)
    subject_index = subject_list.index(subject)
    hours = list(Lecture_Hours[subject_index].values())[0][0]
    lst = []
    if hours > 0:
        for names in (lecturer_subject(Lecturer_Expertise, subject)):
            if lecturer_free(Lecturer_Free, names, time) == True:
                lst.append(names)
    if len(lst) == 0:
        return []
    return lst

def check_free_classroom(data, time):
    lst = []
    free_lst = []
    number = 1
    for item in data:
        for key in item.keys():
            lst.append(key)
    while number < len(lst):
        classroom = lst[number]
        classroom_index = lst.index(classroom)
        if list(data[classroom_index].values())[0][time-1] == 1:
            free_lst.append(classroom)
        number += 1
    if len(free_lst) > 0:
        return free_lst
    else:
        return free_lst

def find_classroom_and_lecturer(Lecture_Hours, Lecturer_Expertise, Lecturer_Free, Classroom_Free):
    lecture = []
    for value in Lecture_Hours:
        time = list(value.values())[0][0]
        subject = list(value.keys())[0]
        while time > 0:
            timeOfDay = 0
            number_of_hours = list(Classroom_Free[0].values())[0]
            while timeOfDay < len(number_of_hours):
                free_classroom = check_free_classroom(Classroom_Free, timeOfDay)
                free_lecturer = lecturer_available_time(Lecture_Hours, Lecturer_Expertise, Lecturer_Free, subject,
                                                        timeOfDay)
                if len(free_classroom) > 0 and len(free_lecturer) > 0:
                    lecture.append({subject: [timeOfDay, free_lecturer, free_classroom]})
                    timeOfDay += 1
                    time -= 1
                    if time == 0:
                        break
                else:
                    timeOfDay += 1
    return lecture