from itertools import chain
import random
import time
import pandas as pd
import datetime


# This class generates the initial timetable as well as the data that is need for the mutation
class timetable():

    def __init__(self, lecturer_hours, population, data_dict, rooms, no_of_subjects):
        self.lecturer_hours = lecturer_hours
        self.population = population
        self.data_dict = data_dict
        self.rooms = rooms
        self.Subject_Courses = {}
        self.Course_Size = {}
        self.courses = []
        self.Subject_Length = {}
        self.ID_Subject = {}
        self.Subject_Size = {}
        self.lectures = []
        self.subject_size = {}
        self.lecture_classrooms = {}
        self.lectures_sem_1 = []
        self.lecturers = []
        self.lecturer_free = {}
        self.lecturer_taken = {}
        self.all_rooms = []
        self.Classroom_Size = {}
        self.Lecturer_Subjects = {}
        self.timetable_result = []
        self.classes = []
        self.Course_Subjects_Sem1 = {}
        self.result = []
        self.no_of_subjects = no_of_subjects

    # This function returns a dict of the size of each program/course,
    # a dict of the modules each course takes, and a list of the courses
    def courses_func(self):
        courses_list = []
        for course in self.data_dict["Class"]:
            course = str(course)
            course = course.replace(" ", "")
            courses_list.append(course.split(","))
        self.Subject_Courses = {}
        for i in range(len(courses_list)):
            self.Subject_Courses.update({self.data_dict["Event Id"][i]: courses_list[i]})
        self.courses = list(set(list(chain.from_iterable(courses_list))))
        potential_courses = []
        for course in self.courses:
            self.Course_Size.update({course: 1})
            potential_courses.append(course.split("/"))
        return self.Course_Size, self.Subject_Courses, self.courses

    # This function returns a dict of the lectures that are going to be taken by each module,
    # and an updated dict of the modules taken by courses
    def Course_Subject(self, cfSubject_Courses):
        Course_Subjects_Sem1 = {}
        Course_Subjects = self.make_dict(self.courses, cfSubject_Courses)
        for course in list(Course_Subjects.keys()):
            if (len(Course_Subjects[course]) // 2) > self.no_of_subjects:
                lectures_list = random.sample(Course_Subjects[course], self.no_of_subjects)
                Course_Subjects_Sem1.update({course: lectures_list})
            else:
                lectures_list = random.sample(Course_Subjects[course], len(Course_Subjects[course]) // 2)
                Course_Subjects_Sem1.update({course: lectures_list})
        self.lectures_sem_1 = list(chain.from_iterable((list(Course_Subjects_Sem1.values()))))
        return self.lectures_sem_1, Course_Subjects

    # This returns the finalised list of lectures to be taken in the first semester
    def create_lectures(self, cslectures_sem_1, cfSubject_Courses):
        Subject_Hours = {}
        self.Subject_Length = self.make_list(self.data_dict, "Event Id", "Length")
        for subject in list(cfSubject_Courses.keys()):
            # Subject_Hours.update({subject: 1})
            Subject_Hours.update({subject: self.Subject_Length[subject] // 24})
        for keys in list(cfSubject_Courses.keys()):
            if keys in cslectures_sem_1:
                word = str(keys)
                word = ((word,) * (Subject_Hours[keys]))
                self.lectures.append(word)
        self.lectures = list(map(int, list(chain.from_iterable(self.lectures))))
        return self.lectures

    # This function returns a list of the the rooms, and a dict of the room sizes
    def make_rooms(self, lst):
        room_size = {}
        for i in range(len(lst["Room"])):
            room_size.update({lst["Room"][i]: lst["Capacity"][i]})
        room_names = list(room_size.keys())
        return room_size, room_names

    # This function returns a dict of the modules that fit in list of classrooms/labs
    def make_all_rooms(self):
        # labs = (self.rooms.loc[self.rooms['Type'] == "Flat"]).to_dict("list")

        # Lab_Size, lab_names = self.make_rooms(labs)
        rooms = (self.rooms.loc[self.rooms['Type'] == "Classroom"]).to_dict("list")
        self.Classroom_Size, room_names_result = self.make_rooms(rooms)
        # self.all_rooms = lab_names + room_names_result
        return self.Classroom_Size  # , self.all_rooms

    # This function returns the rooms which each lecture can use and the size of each module
    def classroom_sizes(self, cfCourse_Size, cfSubject_Courses, marClassroom_Size, cllectures):
        self.subject_size = {}
        for item in list(cfSubject_Courses.keys()):
            size = []
            for course in cfSubject_Courses[item]:
                size.append(cfCourse_Size[course])
            self.subject_size.update({item: sum(size)})
        suitable_classrooms = {}
        for classroom in list(marClassroom_Size.keys()):
            lectures_lst = []
            for subject in list(self.subject_size.keys()):
                if marClassroom_Size[classroom] > self.subject_size[subject]:
                    lectures_lst.append(subject)
                suitable_classrooms.update({classroom: lectures_lst})
        suitable_classrooms = {k: v for k, v in suitable_classrooms.items() if v}
        for subjects in cllectures:
            self.lecture_classrooms.update({subjects: self.get_keys(suitable_classrooms, subjects)})
        self.lecture_classrooms = {k: v for k, v in self.lecture_classrooms.items() if v}
        return self.lecture_classrooms, self.subject_size

    # This function translates the ID of a subject to its name as a string
    def make_data(self):
        self.ID_Subject = self.make_list(self.data_dict, "Event Id", "Mod")
        """
        for subject in list(self.Subject_Length.keys()):
            self.Subject_Size.update({subject: 1})
        """
        return self.ID_Subject

    # This function returns a dict of the modules which each lecturer takes
    def lecturers_function(self):
        lecturer_list = []
        Subjects_Lecturers = {}
        for lecturer in self.data_dict["Lecturer"]:
            lecturer = lecturer.replace(" ", "")
            lecturer_list.append(lecturer.split(","))
        for i in range(len(self.data_dict["Event Id"])):
            Subjects_Lecturers.update({self.data_dict["Event Id"][i]: lecturer_list[i]})
        self.lecturers = list(set(list(chain.from_iterable(lecturer_list))))
        self.Lecturer_Subjects = self.make_dict(self.lecturers, Subjects_Lecturers)
        return self.Lecturer_Subjects

    # This function returns a dict made out of two lists
    def make_list(self, data, value1, value2):
        data_dict = {}
        for i in range(len(data[value1])):
            data_dict.update({data[value1][i]: data[value2][i]})
        return data_dict

    # This function returns a dict from the common elements between a given list and given dict
    def make_dict(self, list, dictionary):
        data_dict = {}
        for item in list:
            data_dict.update({item: self.get_keys(dictionary, item)})
        return data_dict

    # This function returns a list of unique values in a list
    def unique(self, arr):
        n = len(arr)
        ls = []
        mp = {}
        for i in range(n):
            if arr[i] not in mp:
                mp[arr[i]] = 0
            mp[arr[i]] += 1
        for x in mp:
            if (mp[x] == 1):
                ls.append(x)
        return ls

    # This function selects a lecturer randomly based on the modules they teach
    def pick_lecturer(self, lecture, lfLecturer_Subjects):
        choices = self.get_keys(lfLecturer_Subjects, lecture)
        lecturer = random.choice(choices)
        return lecturer

    # This function returns the keys of a dictionary that contain a certain value
    def get_keys(self, data, name):
        keys = [key for key, value in data.items() if name in value]
        return keys

    # This function removes duplicates
    def rem_list(self, lst):
        new_lst = []
        res = []
        for values in lst:
            if values[0] != values[1]:
                new_lst.append(values)
        for i in new_lst:
            if sorted(i) not in res:
                res.append(i)
        return res

    # This function generates the timetable that will be mutated
    def getInitialPopulation(self, cslectures_sem_1, marClassroom_Size, cslecture_classrooms, cssubject_size,
                             mdID_Subject, cfSubject_Courses, lfLecturer_Subjects):
        for pop in range(self.population):
            for lecture in cslectures_sem_1:
                classroom = random.choice(cslecture_classrooms[lecture])
                courses = cfSubject_Courses[lecture]
                room_size = marClassroom_Size[classroom]
                subject_sizes = cssubject_size[lecture]
                time = random.randrange(0, 64)
                self.classes.append(
                    [time, classroom, self.pick_lecturer(lecture, lfLecturer_Subjects), lecture, courses, subject_sizes,
                     room_size, mdID_Subject[lecture]])
        return self.classes

    # This function calls all the
    def call_all(self):
        marClassroom_Size = self.make_all_rooms()
        cfCourse_Size, cfSubject_Courses, cfcourses = self.courses_func()
        cslectures_sem_1, Course_Subjects = self.Course_Subject(cfSubject_Courses)
        cllectures = self.create_lectures(cslectures_sem_1, cfSubject_Courses)
        mdID_Subject = self.make_data()
        lfLecturer_Subjects = self.lecturers_function()
        cslecture_classrooms, cssubject_size = self.classroom_sizes(cfCourse_Size, cfSubject_Courses, marClassroom_Size,
                                                                    cllectures)
        self.result = self.getInitialPopulation(cllectures, marClassroom_Size, cslecture_classrooms,
                                                cssubject_size, mdID_Subject, cfSubject_Courses, lfLecturer_Subjects)
        return self.result, lfLecturer_Subjects, cslecture_classrooms, list(lfLecturer_Subjects.keys()), list(
            marClassroom_Size.keys()), cllectures, Course_Subjects

    # This function generates an excel file from a dictionary
    def excel_function(self, data_dict, xlsx):
        new_lst = []
        for lecture in list(data_dict.keys()):
            lst = []
            lst.append(lecture)
            for item in data_dict[lecture]:
                lst.append(item)
            new_lst.append(lst)
        df = pd.DataFrame(new_lst).T
        df.to_excel(xlsx)


# This class mutates the timetable to create a solution
class algorithm():

    def __init__(self, timetable):
        self.timetable = timetable

    # This function returns a list of unique values
    def rem_list(self, lst):
        new_lst = []
        res = []
        for values in lst:
            if values[0] != values[1]:
                new_lst.append(values)
        for i in new_lst:
            if sorted(i) not in res:
                res.append(i)
        return res

    # This function calculates the fitness of a given timetable.
    # The fitness is measured for the amount of clashes in the timetable
    # There is always duplicates due to the list counting itself and the clash as two separate events
    def calc_fitness(self, lst):
        fitness = len(lst)
        index1 = 0  # Index for time
        index2 = 1  # Index for room
        index3 = 2  # Index for Lecturer
        clashes = []
        for items in lst:
            for pieces in lst:
                if [items[index1], items[index3]] == [pieces[index1], pieces[index3]] or \
                        items[0] == pieces[0] and len(set(items[4]) & set(pieces[4])) > 0 or \
                        [items[index1], items[index2]] == [pieces[index1], pieces[index2]]:
                    clashes.append([lst.index(items), lst.index(pieces)])
                    fitness -= 1
        clashes = self.rem_list(clashes)
        fitness = -len(clashes)
        return fitness, clashes

    # This function returns a dict of the lecturers and their times
    def lecturers_free(self, lecturers):
        lecturer_free = {}
        lecturer_taken = {}
        for lecturer in lecturers:
            lecturer_taken.update({lecturer: []})
            lecturer_free.update({lecturer: list(range(0, 64))})
        for items in self.timetable:
            lecturer = items[2]
            time = items[0]
            if type(lecturer) == list:
                break
            lecturer_taken[lecturer].append(time)
        for lecturer in lecturers:
            times = lecturer_taken[lecturer]
            lecturer_taken[lecturer] = self.unique(times)
            a = [x for x in lecturer_free[lecturer] if x not in lecturer_taken[lecturer]]
            lecturer_free[lecturer] = a
        return lecturer_free

    # This function mutates the timetable to mutate it to a value of 0 which is the fittest possible value.
    # The function will parse through a list of indices and change each one which should slowly bring it to a value of 0.
    def mutate(self, timetable, classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects, lecture_classrooms):
        fitness, clashes = self.calc_fitness(timetable)
        chromosome = timetable
        lst = clashes
        newFit = fitness
        print(newFit)
        # start = time.time()
        while newFit <= fitness:
            for indices in lst:
                index = random.choice(indices)
                hour_original = chromosome[index][0]
                room_original = chromosome[index][1]
                lecturer_original = chromosome[index][2]
                lecture = chromosome[index][3]
                room, lecturer, hour = self.pick_classroom_lecturer(lecture, classroom_free, lecturer_free,
                                                                    Lecturer_Subjects, lecturer_hours,
                                                                    lecture_classrooms)
                lecturer_free[lecturer_original].append(hour_original)
                classroom_free[room_original].append(hour_original)
                chromosome[index][0] = hour
                chromosome[index][1] = room
                chromosome[index][2] = lecturer
                newFit = self.calc_fitness(chromosome)[0]
                print(newFit)
                if newFit <= fitness:
                    continue
            # end = time.time()
            newFit = self.calc_fitness(chromosome)[0]
            print(newFit)
            if newFit < 0:
                self.mutate(chromosome, classroom_free, lecturer_free, lecturer_hours, Lecturer_Subjects,
                            lecture_classrooms)
            return chromosome, classroom_free, lecturer_free

    # This function returns the keys of a dictionary that contain a certain value
    def get_keys(self, data, name):
        keys = [key for key, value in data.items() if name in value]
        return keys

    # Picks a lecturer based off of the modules that they teach
    def pick_lecturer(self, lecture, Lecturer_Subjects):
        choices = self.get_keys(Lecturer_Subjects, lecture)
        lecturer = random.choice(choices)
        return lecturer

    # This function returns a list of unique values in a list
    def unique(self, arr):
        n = len(arr)
        ls = []
        mp = {}
        for i in range(n):
            if arr[i] not in mp:
                mp[arr[i]] = 0
            mp[arr[i]] += 1
        for x in mp:
            if (mp[x] == 1):
                ls.append(x)
        return ls

    # This function creates a dict of the times a classroom is free at
    def classrooms_free(self, rooms):
        classroom_free = {}
        classroom_taken = {}
        for room in rooms:
            classroom_taken.update({room: []})
            classroom_free.update({room: list(range(0, 64))})
        for items in self.timetable:
            room = items[1]
            time = items[0]
            if type(room) == list:
                break
            classroom_taken[room].append(time)
        for room in rooms:
            times = classroom_taken[room]
            classroom_taken[room] = self.unique(times)
            a = [x for x in classroom_free[room] if x not in classroom_taken[room]]
            classroom_free[room] = a
        return classroom_free

    # This function will compare the times that a lecturer and a classroom is free and return any lecturer
    # and classroom that have overlapping times
    def pick_classroom_lecturer(self, lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours,
                                lecture_classrooms):
        lecturer_free = {k: v for k, v in lecturer_free.items() if v is not None}
        classroom_free = {k: v for k, v in classroom_free.items() if v is not None}
        room = random.choice((lecture_classrooms[lecture]))
        lecturer = self.pick_lecturer(lecture, Lecturer_Subjects)
        classroom_times = classroom_free[room]
        if lecturer == None:
            print(lecture)
        lecturer_times = lecturer_free[lecturer]
        if len(classroom_times) == 0:
            del lecturer_free[lecturer]
            self.pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours,
                                         lecture_classrooms)
        times = list(set(classroom_times).intersection(lecturer_times))
        if len(times) == 0:
            self.pick_classroom_lecturer(lecture, classroom_free, lecturer_free, Lecturer_Subjects, lecturer_hours,
                                         lecture_classrooms)
        else:
            time = random.choice(times)
            classroom_free[room].remove(time)
            lecturer_free[lecturer].remove(time)
            return room, lecturer, time

    # This function splits a list in half
    def split_halves(self):
        n = len(self.timetable)
        if n % 2 == 0:
            half = int(n / 2)
            first_half, second_half = self.timetable[:half], self.timetable[n - half:]
        else:
            half = int(n / 2)
            first_half, second_half = self.timetable[:half + 1], self.timetable[n - half:]
        return first_half, second_half

    # This function mutates each half from the split_halves function
    def halves(self, classroom_free, lecturer_free, lecturer_hours, lfLecturer_Subjects, cslecture_classrooms):
        first_half, second_half = self.split_halves()
        first_half, classroom_free, lecturer_free = self.mutate(first_half, classroom_free, lecturer_free,
                                                                lecturer_hours, lfLecturer_Subjects,
                                                                cslecture_classrooms)
        second_half, classroom_free, lecturer_free = self.mutate(second_half, classroom_free, lecturer_free,
                                                                 lecturer_hours, lfLecturer_Subjects,
                                                                 cslecture_classrooms)
        timetable = first_half + second_half
        return timetable, classroom_free, lecturer_free


if __name__ == "__main__":
    no_of_subjects = 4
    lecturer_hours = 16
    population = 1
    hours_in_day = 13
    times = []
    for i in range(7):
        t0 = time.time()
        # The rooms and data used to create the timetable is generated and formatted into a usable dataframe
        labs = "SEEE Labs 2019-20.xlsx"
        main_data = "Timetabling EB03 Data Sample 201920.xlsx"
        data = pd.read_excel(main_data, "Sheet1")
        rooms = pd.read_excel(labs, "Sheet1")
        data_dict = data.to_dict("list")

        # An instance of a timetable is generated and populated with the max. amount of hours a lecturer can work,
        # the size of the population, the data in the form of a dictionary, the rooms in a dataframe,
        # and the max. no. of subjects per module
        timetables = timetable(lecturer_hours, population, data_dict, rooms, no_of_subjects)

        # The timetable is all generated within the class, as is the dictionary that holds the lecturers subjects,
        # the dictionary that holds each classrooms, a list of the lecturers, a list of the rooms, all the lectures,
        # and all the subjects that each modules takes
        results, lfLecturer_Subjects, cslecture_classrooms, lecturers, rooms, cllectures, Course_Subjects = timetables.call_all()
        data = algorithm(results)
        # Generating the times classrooms and lecturers are free
        classroom_free = data.classrooms_free(rooms)
        lecturer_free = data.lecturers_free(lecturers)

        # Splitting the timetable in half speeds the mutation up considerably
        list_timetable, classroom_free, lecturer_free = data.halves(classroom_free, lecturer_free, lecturer_hours,
                                                                    lfLecturer_Subjects, cslecture_classrooms)

        # The mutation that creates teh solution
        result = data.mutate(list_timetable, classroom_free, lecturer_free,
                             lecturer_hours, lfLecturer_Subjects, cslecture_classrooms)[0]
        t1 = time.time()
        total = t1 - t0
        times.append(len(cllectures))
        times.append(total)
    with open('data.txt', 'w') as filehandle:
        for listitem in times:
            filehandle.write('%s\n' % listitem)
