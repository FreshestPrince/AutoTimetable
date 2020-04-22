import random
import time
from itertools import chain
import pandas as pd
import datetime

labs = "SEEE Labs 2019-20.xlsx"
main_data = "Timetabling EB03 Data Sample 201920.xlsx"
data = pd.read_excel(main_data, "Sheet1")
rooms = pd.read_excel(labs, "Sheet1")
columns = ['Event Id', 'Day', 'Time', 'Length', 'Module', 'Lecturer', 'Class', 'Grp', 'Weeks', 'Mod', 'Num weeks']
data_dict = data.to_dict("list")
Subjects_Lecturers = {}
lecturer_list = []
for lecturer in data_dict["Lecturer"]:
    lecturer = lecturer.replace(" ", "")
    lecturer_list.append(lecturer.split(","))
for i in range(len(data_dict["Event Id"])):
    Subjects_Lecturers.update({data_dict["Event Id"][i]: lecturer_list[i]})


def make_lecturers(lecturer_hours, Lecturer_Subjects):
    lecturers = []
    for item in list(Lecturer_Subjects.keys()):
        lecturers.append([item] * lecturer_hours)
    lecturers = list(chain.from_iterable(lecturers))
    return lecturers


def pick_lecturer(lecture, Lecturer_Subjects):
    choices = get_keys(Lecturer_Subjects, lecture)
    lecturer = random.choice(choices)
    return lecturer


def getInitialPopulation(lectures, Lecturer_Subjects, population, Subject_Courses, Subject_Size, Classroom_Size,
                         lecture_classrooms, lecturer_hours, ID_Subject):
    timetables = []
    fitness_list = {}
    fitness_dict = {}
    # lecturer_dict = {}
    for pop in range(population):
        classes = []
        for lecture in lectures:
            lecturers = make_lecturers(lecturer_hours, Lecturer_Subjects)
            classroom = random.choice(lecture_classrooms[lecture])
            courses = Subject_Courses[lecture]
            room_size = Classroom_Size[classroom]
            subject_sizes = subject_size[lecture]
            time = random.randrange(0, 64)
            classes.append(
                [time, classroom, pick_lecturer(lecture, Lecturer_Subjects),
                 lecture, courses, subject_sizes, room_size, ID_Subject[lecture]])
        print("Done population", pop)
        timetables.append(classes)
        fit = calc_fitness(classes)
        fitness_list.update({pop: classes})
        fitness_dict.update({pop: fit[0]})
        # lecturer_dict.update({pop: lecturers})
        fitness_dict = {k: v for k, v in sorted(fitness_dict.items(), key=lambda item: item[1], reverse=True)}
        fittest = list(fitness_dict.keys())[0]
        timetables = fitness_list[fittest]
    return timetables


def make_rooms(lst):
    room_size = {}
    for i in range(len(lst["Room"])):
        room_size.update({lst["Room"][i]: lst["Capacity"][i]})
    room_names = list(room_size.keys())
    return room_size, room_names


def make_dict(list, dictionary):
    data_dict = {}
    for item in list:
        data_dict.update({item: get_keys(dictionary, item)})
    return data_dict


def make_list(data, value1, value2):
    data_dict = {}
    for i in range(len(data[value1])):
        data_dict.update({data[value1][i]: data[value2][i]})
    return data_dict


def get_keys(data, name):
    keys = [key for key, value in data.items() if name in value]
    return keys


def classroom_sizes(Subject_Courses, Course_Size, Classroom_Size, Subject_Names):
    subject_size = {}
    for item in list(Subject_Courses.keys()):
        size = []
        for course in Subject_Courses[item]:
            size.append(Course_Size[course])
        subject_size.update({item: sum(size)})
    suitable_classrooms = {}
    for classroom in list(Classroom_Size.keys()):
        lectures = []
        for subject in list(subject_size.keys()):
            if Classroom_Size[classroom] > subject_size[subject]:
                lectures.append(subject)
            suitable_classrooms.update({classroom: lectures})
    suitable_classrooms = {k: v for k, v in suitable_classrooms.items() if v}
    lecture_classrooms = {}
    for subjects in Subject_Names:
        lecture_classrooms.update({subjects: get_keys(suitable_classrooms, subjects)})
    lecture_classrooms = {k: v for k, v in lecture_classrooms.items() if v}
    return subject_size, suitable_classrooms, lecture_classrooms


def rem_list(lst):
    new_lst = []
    res = []
    for values in lst:
        if values[0] != values[1]:
            new_lst.append(values)
    for i in new_lst:
        if sorted(i) not in res:
            res.append(i)
    return res


def calc_fitness(lst):
    fitness = len(lst)
    index1 = 0  # Index for time
    index2 = 1  # Index for room
    index3 = 2  # Index for Lecturer
    index4 = 4
    lecturer_clashes = []
    room_clashes = []
    course_clashes = []
    for items in lst:
        for pieces in lst:
            if [items[index1], items[index3]] == [pieces[index1], pieces[index3]]:
                lecturer_clashes.append([lst.index(items), lst.index(pieces)])
                fitness -= 1
            elif [items[index1], items[index2]] == [pieces[index1], pieces[index2]]:
                room_clashes.append([lst.index(items), lst.index(pieces)])
                fitness -= 1
            elif items[0] == pieces[0] and len(set(items[4]) & set(pieces[4])) > 0:
                course_clashes.append([lst.index(items), lst.index(pieces)])
                fitness -= 1
    room_clashes = rem_list(room_clashes)
    lecturer_clashes = rem_list(lecturer_clashes)
    fitness = -(len(lecturer_clashes) + len(room_clashes) + len(course_clashes))
    clashes = lecturer_clashes + room_clashes + course_clashes
    clashes = rem_list(clashes)
    fitness = -len(clashes)
    return fitness, clashes  # lecturer_clashes, room_clashes, course_clashes


def unique(arr):
    # Insert all array elements in hash
    n = len(arr)
    ls = []
    mp = {}
    for i in range(n):
        if arr[i] not in mp:
            mp[arr[i]] = 0
        mp[arr[i]] += 1
    # Traverse through map only and
    for x in mp:
        if (mp[x] == 1):
            ls.append(x)
    return ls


def lecturers_free(timetables):
    lecturer_free = {}
    lecturer_taken = {}
    for lecturer in lecturers:
        lecturer_taken.update({lecturer: []})
        lecturer_free.update({lecturer: list(range(0, 64))})
    for items in timetables:
        lecturer = items[2]
        time = items[0]
        lecturer_taken[lecturer].append(time)
    for lecturer in lecturers:
        times = lecturer_taken[lecturer]
        lecturer_taken[lecturer] = unique(times)
        a = [x for x in lecturer_free[lecturer] if x not in lecturer_taken[lecturer]]
        lecturer_free[lecturer] = a
    return lecturer_free, lecturer_taken


def classrooms_free(timetables):
    classroom_free = {}
    classroom_taken = {}
    for room in rooms:
        classroom_taken.update({room: []})
        classroom_free.update({room: list(range(0, 64))})
    for items in timetables:
        room = items[1]
        time = items[0]
        # print(classroom_taken)
        if type(room) == list:
            break
        classroom_taken[room].append(time)
    for room in rooms:
        times = classroom_taken[room]
        classroom_taken[room] = unique(times)
        a = [x for x in classroom_free[room] if x not in classroom_taken[room]]
        classroom_free[room] = a
    return classroom_free, classroom_taken


def pick_new_lecturer(lecturer_free, lecture, Lecturer_Subjects, lecturer_hours):
    choices = get_keys(Lecturer_Subjects, lecture)
    lecturer = random.choice(choices)
    if (65 - lecturer_free[lecturer]) > lecturer_hours:
        del lecturer_free[lecturer]
        del Lecturer_Subjects[lecturer]
        pick_new_lecturer(lecturer_free, lecture, Lecturer_Subjects, lecturer_hours)
    else:
        return lecturer


def pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours):
    lecturer_free = {k: v for k, v in lecturer_free.items() if v is not None}
    classroom_free = {k: v for k, v in classroom_free.items() if v is not None}
    room = random.choice((lecture_classrooms[lecture]))
    lecturer = pick_lecturer(lecture, Lecturer_Subjects)
    classroom_times = classroom_free[room]
    if lecturer == None:
        print(lecture)
        # print(lecturer_free)
        # print(Lecturer_Subjects)
    lecturer_times = lecturer_free[lecturer]
    if len(classroom_times) == 0:
        del lecturer_free[lecturer]
        pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours)
    times = list(set(classroom_times).intersection(lecturer_times))
    if len(times) == 0:
        pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours)
    else:
        time = random.choice(times)
        # print(classroom_free[room])
        classroom_free[room].remove(time)
        lecturer_free[lecturer].remove(time)
        return room, lecturer, time


def mutate(timetables, classroom_free, lecturer_free, lecturer_hours):
    fitness, clashes = calc_fitness(timetables)
    chromosome = timetables
    # lst = lecturer_clashes + room_clashes + course_clashes
    lst = clashes
    newFit = fitness
    print(newFit)
    start = time.time()
    while newFit <= fitness:
        for indices in lst:
            index = random.choice(indices)
            lecture = chromosome[index][3]
            room, lecturer, hour = pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects,
                                                           lecturer_hours)
            chromosome[index][0] = hour
            chromosome[index][1] = room
            chromosome[index][2] = lecturer
            newFit = calc_fitness(chromosome)[0]
            print(newFit)
            if newFit <= fitness:
                continue
        end = time.time()
        print(end - start)
        newFit = calc_fitness(timetables)[0]
        print(newFit)
        if newFit < 0:
            mutate(timetables, classroom_free, lecturer_free, lecturer_hours)
        return chromosome


def get_streams(courses):
    options = []
    for course in courses:
        a = course.split("/")
        options.append(a)
    new_c = {}
    for option in options:
        if len(option) == 1:
            new_c.update({option[0]: [option[0]]})
        else:
            course = option[0]
            stream = option[1]
            if course in list(new_c.keys()):
                new_c[course].append(stream)
            else:
                new_c.update({course: [stream]})
    return new_c


def split_halves(array):
    n = len(array)
    if n % 2 == 0:
        half = int(n / 2)
        first_half, second_half = array[:half], array[n - half:]
    else:
        half = int(n / 2)
        first_half, second_half = array[:half + 1], array[n - half:]
    return first_half, second_half


courses_list = []
for course in data_dict["Class"]:
    course = str(course)
    course = course.replace(" ", "")
    courses_list.append(course.split(","))
Subject_Courses = {}
for i in range(len(courses_list)):
    Subject_Courses.update({data_dict["Event Id"][i]: courses_list[i]})
courses = list(set(list(chain.from_iterable(courses_list))))
# print(courses)
Course_Size = {}
potential_courses = []
for course in courses:
    Course_Size.update({course: 1})
    potential_courses.append(course.split("/"))
lecturers = list(set(list(chain.from_iterable(lecturer_list))))
# print(lecturers)
ID_Subject = make_list(data_dict, "Event Id", "Mod")
Subject_Length = make_list(data_dict, "Event Id", "Length")
Lecturer_Subjects = make_dict(lecturers, Subjects_Lecturers)
Course_Subjects = make_dict(courses, Subject_Courses)
Subject_Hours = {}
for subject in Subject_Length:
    Subject_Hours.update({subject: 1})
    # Subject_Hours.update({subject:Subject_Length[subject]/12})
course_dict = {}
for course in courses:
    course_split = course.split("/")
    if len(course_split) == 1:
        course_dict.update({course: [course]})
    elif course_split[0] in list(course_dict.keys()):
        course_dict[course_split[0]].append(course_split[1])
    else:
        course_dict.update({course_split[0]: [course_split[1]]})
course_dict = {x: sorted(course_dict[x]) for x in course_dict.keys()}
labs = (rooms.loc[rooms['Type'] == "Flat"]).to_dict("list")
rooms = (rooms.loc[rooms['Type'] == "Classroom"]).to_dict("list")
Subject_Size = {}
for subject in list(Subject_Length.keys()):
    Subject_Size.update({subject: 1})

Lab_Size, lab_names = make_rooms(labs)
Classroom_Size, room_names = make_rooms(rooms)
rooms = lab_names + room_names
Course_Subjects_Sem1 = {}

for course in list(Course_Subjects.keys()):
    if len(Course_Subjects[course]) > 6:
        lectures_list = random.sample(Course_Subjects[course], 6)
        Course_Subjects_Sem1.update({course: lectures_list})
    else:
        lectures_list = Course_Subjects[course]
        Course_Subjects_Sem1.update({course: lectures_list})
lectures_sem_1 = list(chain.from_iterable((list(Course_Subjects_Sem1.values()))))
lectures = []
for keys in list(Subject_Hours.keys()):
    if keys in lectures_sem_1:
        word = str(keys)
        word = ((word,) * (Subject_Hours[keys]))
        lectures.append(word)
lectures = list(map(int, list(chain.from_iterable(lectures))))

subject_size, suitable_classrooms, lecture_classrooms = classroom_sizes(Subject_Courses, Course_Size, Classroom_Size,
                                                                        lectures)
random.shuffle(lectures)
time_list = []
generations = 1
population = 1

t0 = time.time()
lecturer_hours = 18

timetables = getInitialPopulation(lectures, Lecturer_Subjects, population, Subject_Courses, Subject_Size,
                                  Classroom_Size, lecture_classrooms, lecturer_hours, ID_Subject)
classroom_free, classroom_taken = classrooms_free(timetables)
lecturer_free, lecturer_taken = lecturers_free(timetables)
print(len(timetables))
first_half, second_half = split_halves(timetables)
print(len(first_half), len(second_half))
first_half = mutate(first_half, classroom_free, lecturer_free, lecturer_hours)
second_half = mutate(second_half, classroom_free, lecturer_free, lecturer_hours)
timetables = first_half + second_half
columns = ["Time", "Room", "Lecturer", "Lecture_ID", "Course(s)", "Class Size", "Room Size", "Lecture"]
a = mutate(timetables, classroom_free, lecturer_free, lecturer_hours)
t1 = time.time()
df = pd.DataFrame(a)
df.columns = columns
df.to_excel("tt.xlsx")
total = t1 - t0
time_list.append(total)
print(str(datetime.timedelta(seconds=total)))
