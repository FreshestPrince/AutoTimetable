import random
import time
from itertools import chain
import itertools


def courses(data_dict):
    courses_list = []
    for course in data_dict["Class"]:
        course = str(course)
        course = course.replace(" ", "")
        courses_list.append(course.split(","))
    Subject_Courses = {}
    for i in range(len(courses_list)):
        Subject_Courses.update({data_dict["Event Id"][i]: courses_list[i]})
    courses = list(set(list(chain.from_iterable(courses_list))))
    Course_Size = {}
    potential_courses = []
    for course in courses:
        Course_Size.update({course: 1})
        potential_courses.append(course.split("/"))
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
    return Course_Size, courses, courses_list, Subject_Courses, course_dict


def lecturers(data_dict):
    Subjects_Lecturers = {}
    lecturer_list = []
    for lecturer in data_dict["Lecturer"]:
        lecturer = lecturer.replace(" ", "")
        lecturer_list.append(lecturer.split(","))
    for i in range(len(data_dict["Event Id"])):
        Subjects_Lecturers.update({data_dict["Event Id"][i]: lecturer_list[i]})
    lecturers = list(set(list(chain.from_iterable(lecturer_list))))
    return Subjects_Lecturers, lecturer_list, lecturers


def make_all_rooms(rooms):
    labs = (rooms.loc[rooms['Type'] == "Flat"]).to_dict("list")
    rooms = (rooms.loc[rooms['Type'] == "Classroom"]).to_dict("list")
    Lab_Size, lab_names = make_rooms(labs)
    Classroom_Size, room_names = make_rooms(rooms)
    all_rooms = lab_names + room_names
    return all_rooms, Classroom_Size

def Course_Subject(Course_Subjects):
    Course_Subjects_Sem1 = {}
    for course in list(Course_Subjects.keys()):
        if len(Course_Subjects[course]) > 6:
            lectures_list = random.sample(Course_Subjects[course], 6)
            Course_Subjects_Sem1.update({course: lectures_list})
        else:
            lectures_list = Course_Subjects[course]
            Course_Subjects_Sem1.update({course: lectures_list})
    lectures_sem_1 = list(chain.from_iterable((list(Course_Subjects_Sem1.values()))))
    return lectures_sem_1


def make_data(data_dict, rooms):
    ID_Subject = make_list(data_dict, "Event Id", "Mod")
    Subject_Length = make_list(data_dict, "Event Id", "Length")
    Subject_Size = {}
    for subject in list(Subject_Length.keys()):
        Subject_Size.update({subject: 1})
    all_rooms, Classroom_Size = make_all_rooms(rooms)
    return Subject_Length, ID_Subject, all_rooms, Classroom_Size


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


def getInitialPopulation(lectures, Lecturer_Subjects, population, Subject_Courses, subject_size, Classroom_Size,
                         lecture_classrooms, ID_Subject):
    timetables = []
    fitness_list = {}
    fitness_dict = {}
    # lecturer_dict = {}
    for pop in range(population):
        classes = []
        for lecture in lectures:
            classroom = random.choice(lecture_classrooms[lecture])
            courses = Subject_Courses[lecture]
            room_size = Classroom_Size[classroom]
            subject_sizes = subject_size[lecture]
            time = random.randrange(0, 64)
            classes.append(
                [time, classroom, pick_lecturer(lecture, Lecturer_Subjects),
                 lecture, courses, subject_sizes, room_size, ID_Subject[lecture]])
        # print("Done population", pop)
        timetables.append(classes)
        fit = calc_fitness(classes)
        fitness_list.update({pop: classes})
        fitness_dict.update({pop: fit[0]})
        # lecturer_dict.update({pop: lecturers})
        fitness_dict = {k: v for k, v in sorted(fitness_dict.items(), key=lambda item: item[1], reverse=True)}
        fittest = list(fitness_dict.keys())[0]
        timetable = fitness_list[fittest]
    return timetable


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
        get_keys(suitable_classrooms, subjects)
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
            if [items[index1], items[index3]] == [pieces[index1], pieces[index3]] or \
                    items[0] == pieces[0] and len(set(items[4]) & set(pieces[4])) > 0 or \
                    [items[index1], items[index2]] == [pieces[index1], pieces[index2]]:
                lecturer_clashes.append([lst.index(items), lst.index(pieces)])
                fitness -= 1
                """
            elif :
                room_clashes.append([lst.index(items), lst.index(pieces)])
                fitness -= 1
            elif :
                course_clashes.append([lst.index(items), lst.index(pieces)])
                fitness -= 1
                """
    room_clashes = rem_list(room_clashes)
    lecturer_clashes = rem_list(lecturer_clashes)
    """
    fitness = -(len(lecturer_clashes) + len(room_clashes) + len(course_clashes))
    clashes = lecturer_clashes + room_clashes + course_clashes
    clashes = rem_list(clashes)
    """
    clashes = lecturer_clashes
    fitness = -len(lecturer_clashes)
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


def lecturers_free(timetables, lecturers):
    lecturer_free = {}
    lecturer_taken = {}
    for lecturer in lecturers:
        lecturer_taken.update({lecturer: []})
        lecturer_free.update({lecturer: list(range(0, 64))})
    for items in timetables:
        lecturer = items[2]
        time = items[0]
        if type(lecturer) == list:
            break
        lecturer_taken[lecturer].append(time)
    for lecturer in lecturers:
        times = lecturer_taken[lecturer]
        lecturer_taken[lecturer] = unique(times)
        a = [x for x in lecturer_free[lecturer] if x not in lecturer_taken[lecturer]]
        lecturer_free[lecturer] = a
    return lecturer_free, lecturer_taken


def classrooms_free(timetables, rooms):
    classroom_free = {}
    classroom_taken = {}
    for room in rooms:
        classroom_taken.update({room: []})
        classroom_free.update({room: list(range(0, 64))})
    for items in timetables:
        room = items[1]
        time = items[0]
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
    if len(choices) > 1:
        lecturer_lengths = {}
        for lecturers in choices:
            lecturer_lengths.update({lecturers: 65 - len(lecturer_free[lecturers])})
        myList = {k: v for k, v in sorted(lecturer_lengths.items(), key=lambda item: item[1])}
        lecturer = list(myList.keys())[0]
    else:
        lecturer = choices[0]
    if (65 - len(lecturer_free[lecturer])) > lecturer_hours:
        del lecturer_free[lecturer]
        del Lecturer_Subjects[lecturer]
        pick_new_lecturer(lecturer_free, lecture, Lecturer_Subjects, lecturer_hours)
    else:
        return lecturer


def pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours,
                            lecture_classrooms):
    lecturer_free = {k: v for k, v in lecturer_free.items() if v is not None}
    classroom_free = {k: v for k, v in classroom_free.items() if v is not None}
    room = random.choice((lecture_classrooms[lecture]))
    lecturer = pick_lecturer(lecture, Lecturer_Subjects)
    classroom_times = classroom_free[room]
    if lecturer == None:
        print(lecture)
    lecturer_times = lecturer_free[lecturer]
    if len(classroom_times) == 0:
        del lecturer_free[lecturer]
        pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours,
                                lecture_classrooms)
    times = list(set(classroom_times).intersection(lecturer_times))
    if len(times) == 0:
        pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours,
                                lecture_classrooms)
    else:
        time = random.choice(times)
        classroom_free[room].remove(time)
        lecturer_free[lecturer].remove(time)
        return room, lecturer, time


def mutate(timetables, classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects, lecture_classrooms):
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
                                                           lecturer_hours, lecture_classrooms)
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
            mutate(timetables, classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects, lecture_classrooms)
        return chromosome, classroom_free, lecturer_free


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


def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


def return_timetables(timetables, classroom_free, lecturer_free, lecturer_hours, group, Lecturer_Subjects,
                      lecture_classrooms):
    groups = list(mygrouper(group, timetables))
    mutate_dicts = {}
    for i in range(len(groups)):
        mutate_dicts.update({i: mutate(groups[i], classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects,
                                       lecture_classrooms)})
    output = list(mutate_dicts.values())
    return list(itertools.chain(*output))


def create_lectures(hours, Subject_Length, lectures_sem_1):
    Subject_Hours = {}
    for subject in Subject_Length:
        Subject_Hours.update({subject: hours})
        # Subject_Hours.update({subject:Subject_Length[subject]/12})
    lectures = []
    for keys in list(Subject_Hours.keys()):
        if keys in lectures_sem_1:
            word = str(keys)
            word = ((word,) * (Subject_Hours[keys]))
            lectures.append(word)
    lectures = list(map(int, list(chain.from_iterable(lectures))))
    return lectures, Subject_Hours
