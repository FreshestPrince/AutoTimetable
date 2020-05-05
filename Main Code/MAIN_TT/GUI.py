from tkinter import *
from tkinter.ttk import Button, Style
from random import choice, randint
import pandas as pd
from datetime import datetime, timedelta
from cal_setup import get_calendar_service
import datetime
from itertools import chain


# This class returns time for
class create_time():

    def __init__(self, number, hours_in_day):
        self.number = number
        self.hours_in_day = hours_in_day

    def time_normal(self):
        while 0 < self.number > self.hours_in_day - 1:
            self.number -= self.hours_in_day
        if self.number == 0:
            return 9
        elif self.number == 1:
            return 10
        elif self.number == 2:
            return 11
        elif self.number == 3:
            return 12
        elif self.number == 4:
            return 13
        elif self.number == 5:
            return 14
        elif self.number == 6:
            return 15
        elif self.number == 7:
            return 16
        elif self.number == 8:
            return 17
        elif self.number == 9:
            return 18
        elif self.number == 10:
            return 19
        elif self.number == 11:
            return 20
        elif self.number == 12:
            return 21

    def time_translate(self):
        if self.number < self.hours_in_day:
            return "Monday" + "-" + str(self.time_normal())
        elif self.hours_in_day * 2 > self.number:
            return "Tuesday" + "-" + str(self.time_normal())
        elif self.hours_in_day * 3 > self.number:
            return "Wednesday" + "-" + str(self.time_normal())
        elif self.hours_in_day * 4 > self.number:
            return "Thursday" + "-" + str(self.time_normal())
        elif self.hours_in_day * 5 > self.number:
            return "Friday" + "-" + str(self.time_normal())
        else:
            print("Value is not within proper range")
            return 0

    def make_date(self, start_day):
        day, time = self.time_translate().split("-")
        if day == "Monday":
            start_day += 0
            return start_day, int(time)
        elif day == "Tuesday":
            start_day += 1
            return start_day, int(time)
        elif day == "Wednesday":
            start_day += 2
            return start_day, int(time)
        elif day == "Thursday":
            start_day += 3
            return start_day, int(time)
        elif day == "Friday":
            start_day += 4
            return start_day, int(time)


class GUI():

    def __init__(self, classroom_free, lectures, lecturer_free, Course_Subjects, df, hours_in_day):
        self.classroom_free = classroom_free
        self.lectures = lectures
        self.lecturer_free = lecturer_free
        self.Course_Subjects = Course_Subjects
        self.df = df
        self.hours_in_day = hours_in_day
        self.course_times = {}
        self.lecturer_times = {}
        self.classroom_times = {}
        self.lecture_times = {}
        self.colours = []
        self.btn_list = []

    def make_times(self):
        classrooms = list(self.classroom_free.keys())
        for i in range(len(classrooms)):
            room = classrooms[i]
            new_df = df[df.values == room]
            self.classroom_times.update({room: new_df.to_dict("list")})

        for i in range(len(self.lectures)):
            lecture = self.lectures[i]
            new_df = df[df.values == lecture]
            self.lecture_times.update({lecture: new_df.to_dict("list")})

        for i in range(len(list(self.lecturer_free.keys()))):
            lecturer = list(self.lecturer_free.keys())[i]
            new_df = df[df.values == lecturer]
            self.lecturer_times.update({lecturer: new_df.to_dict("list")})
        lst = sorted(list(self.Course_Subjects.keys()))
        for i in range(len(lst)):
            course = lst[i]
            subjects = self.Course_Subjects[course]
            new_df = df[df.Lecture_ID.isin(subjects)]
            self.course_times.update({course: new_df.to_dict("list")})

    def make_timetable(self):
        root = Tk()
        self.colours = list(pd.read_csv("colours.csv").columns)
        values = ["Lecturer", "Rooms", "Courses", "Lecture"]
        root.config(bg="cornflowerblue")
        style = Style(root)
        style.theme_use("clam")
        style.configure(root, background="cornflowerblue", fieldbackground="cornflowerblue", foreground="white")
        for i in range(len(values)):
            item = values[i]
            b = Button(root, text=item, command=lambda idx=i: self.search(idx))
            b.pack(padx=10, pady=5, side=TOP)
            self.btn_list.append(b)  # Append the button to a list
        root.attributes('-transparent', True)
        root.mainloop()

    def search(self, idx):
        New_Window = Tk()
        button_pressed = (self.btn_list[idx].cget("text"))
        if button_pressed == "Lecturer":
            print("Lecturer")
            Label(New_Window, text="Search for a lecturer").grid(row=0)
            Lecturer = Entry(New_Window)
            Lecturer.grid(row=0, column=1)
            style = Style(New_Window)
            style.theme_use("clam")
            style.configure(New_Window, background="cornflowerblue", fieldbackground="cornflowerblue",
                            foreground="white")
            Button(New_Window, text='Search',
                   command=lambda value=Lecturer: self.timetable(value, self.lecturer_times)).grid(row=3, column=1,
                                                                                                   sticky=W,
                                                                                                   pady=4)
            New_Window.attributes('-transparent', True)
        elif button_pressed == "Rooms":
            print("Rooms")
            Label(New_Window, text="Search for a room").grid(row=0)
            Room = Entry(New_Window)
            Room.grid(row=0, column=1)
            New_Window.config(bg="cornflowerblue")
            style = Style(New_Window)
            style.theme_use("clam")
            style.configure(New_Window, background="cornflowerblue", fieldbackground="cornflowerblue",
                            foreground="white")
            Button(New_Window, text='Search',
                   command=lambda value=Room: self.timetable(value, self.classroom_times)).grid(
                row=3, column=1, sticky=W, pady=4)
            New_Window.attributes('-transparent', True)
        elif button_pressed == "Courses":
            print("Courses")
            Label(New_Window, text="Search for a course").grid(row=0)
            Course = Entry(New_Window)
            Course.grid(row=0, column=1)
            New_Window.config(bg="cornflowerblue")
            style = Style(New_Window)
            style.theme_use("clam")
            style.configure(New_Window, background="cornflowerblue", fieldbackground="cornflowerblue",
                            foreground="white")
            Button(New_Window, text='Search', command=lambda value=Course: self.course_timetable(value)).grid(
                row=3, column=1, sticky=W, pady=4)
            New_Window.attributes('-transparent', True)
        else:
            print("Lecture")
            Label(New_Window, text="Search for a lecture").grid(row=0)
            Lecture = Entry(New_Window)
            Lecture.grid(row=0, column=1)
            New_Window.config(bg="cornflowerblue")
            style = Style(New_Window)
            style.theme_use("clam")
            style.configure(New_Window, background="cornflowerblue", fieldbackground="cornflowerblue",
                            foreground="white")
            Button(New_Window, text='Search',
                   command=lambda value=Lecture: self.timetable(value, self.lecture_times)).grid(
                row=3, column=1, sticky=W, pady=4)
            New_Window.attributes('-transparent', True)
        New_Window.mainloop()

    def create_event(self, start_date, time, lecture, description, finish_date, location, color):
        service = get_calendar_service()
        tomorrow = datetime(start_date[0], start_date[1], start_date[2], time - 1)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=1)).isoformat()
        event_result = service.events().insert(calendarId='primary',
                                               body={
                                                   "summary": lecture,
                                                   'location': location,
                                                   "description": description,
                                                   "start": {"dateTime": start, "timeZone": 'Etc/GMT+0'},
                                                   "end": {"dateTime": end, "timeZone": 'Etc/GMT+0'},
                                                   'recurrence': [finish_date],
                                                   "colorId": color,
                                                   "reminders": {
                                                       "useDefault": "useDefault",
                                                       # Overrides can be set if and only if useDefault is false.
                                                       'overrides': [
                                                           {'method': 'email', 'minutes': 24 * 60},
                                                           {'method': 'popup', 'minutes': 10},
                                                       ]
                                                   },
                                               }
                                               ).execute()
        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    def create_window(self, Lecture):
        New_Window = Tk()
        Columns = ["Lecturer:", "Classroom:", "Lecture:", "Course:", ""]
        if type(Lecture) != list:
            lbl = Label(New_Window, text=Lecture, font=("Arial Bold", 30))
            lbl.grid(column=0, row=0)
        else:
            rows = 4
            columns = 2
            for x in range(columns):
                for y in range(rows):
                    if x == 0:
                        text = Columns[y]
                    else:
                        text = Lecture[y]
                    btn = Label(New_Window, text=text)
                    btn.grid(column=x, row=y, sticky="NSEW")
                    Grid.columnconfigure(New_Window, x, weight=1)
                    Grid.rowconfigure(New_Window, y, weight=1)
        New_Window.mainloop()

    def save_on_google(self, course):
        thecourse = course
        finish_date = 'RRULE:FREQ=WEEKLY;UNTIL=20200529'
        location = "TU Dublin Kevin Street, Kevin Street, Portobello, Dublin 2, D08 X622, Ireland"
        lecture_dict = {}
        course = thecourse
        for i in range(len(self.course_times[course]["Time"])):
            start_day = 20
            Lecture = self.course_times[course]["Lecture"][i]
            Classroom = self.course_times[course]["Room"][i]
            Lecturer = self.course_times[course]["Lecturer"][i]
            number = self.course_times[course]["Time"][i]
            color = randint(1, 11)
            description = "Classroom-" + str(Classroom) + "\n" + "Lecturer-" + str(Lecturer)
            times = create_time(0, self.hours_in_day)
            start_day, time = times.make_date(start_day)
            start_date = (2020, 4, start_day)
            lecture_dict.update({Lecture: number})
            self.create_event(start_date, time, Lecture, description, finish_date, location, color)

    def is_int(self, val):
        try:
            num = int(val)
        except ValueError:
            return False
        return True

    def timetable(self, value, dictionary):
        search_term = value.get()
        if self.is_int(search_term) == True:
            search_term = int(search_term)
        New_Window = Tk()

        time = 0
        index = 0
        rows = 13
        columns = 5
        grid = Frame(New_Window)
        Grid.rowconfigure(grid, rows, weight=1)
        Grid.columnconfigure(grid, columns, weight=1)
        grid.grid(row=0, column=0, sticky=N + S + E + W)
        subject_colours = {}
        for x in range(columns):
            for y in range(rows):
                if time in dictionary[search_term]["Time"]:
                    Lecture = dictionary[search_term]["Lecture"][index]
                    Lecturer = (dictionary[search_term]["Lecturer"][index])
                    Course = (dictionary[search_term]["Course(s)"][index])
                    Room_Size = (dictionary[search_term]["Room Size"][index])
                    info = [Lecturer, Lecture, Course, Room_Size]
                    lst = [Lecture]
                    text = ''.join(str(element) + ' ' for element in lst)
                    index += 1
                    fg_colour = "white"
                    if Lecture not in list(subject_colours.keys()):
                        bg_colour = choice(self.colours)
                        subject_colours.update({Lecture: bg_colour})
                    else:
                        bg_colour = subject_colours[Lecture]
                else:
                    text = "\n"
                    info = "There is no lecture at this time."
                    bg_colour = "white"
                    fg_colour = "black"
                style = Style(New_Window)
                style.theme_use("clam")
                style.configure(New_Window, background=bg_colour, fieldbackground=bg_colour, foreground=fg_colour)
                style.theme_use("clam")
                times = create_time(time, self.hours_in_day)
                text = (times.time_translate()) + "\n" + text
                btn = Button(New_Window, text=text, command=lambda idx=info: self.create_window(idx),
                             style='styling.TButton')
                btn.grid(column=x, row=y, sticky="NSEW")
                Grid.columnconfigure(New_Window, x, weight=1)
                Grid.rowconfigure(New_Window, y, weight=1)
                time += 1
        New_Window.mainloop()

    def course_timetable(self, course):
        course = course.get()
        New_Window = Tk()
        style = Style(New_Window)
        style.theme_use("clam")
        style.configure(New_Window, background="cornflowerblue", fieldbackground="cornflowerblue", foreground="white")
        style.theme_use("clam")
        time = 0
        index = 0
        rows = 13
        columns = 5
        grid = Frame(New_Window)
        Grid.rowconfigure(grid, rows, weight=1)
        Grid.columnconfigure(grid, columns, weight=1)
        grid.grid(row=0, column=0, sticky=N + S + E + W)
        subject_colours = {}
        for x in range(columns):
            for y in range(rows):
                if time in self.course_times[course]["Time"]:
                    Lecture = self.course_times[course]["Lecture"][index]
                    Classroom = self.course_times[course]["Room"][index]
                    Lecturer = (self.course_times[course]["Lecturer"][index])
                    Course = (self.course_times[course]["Course(s)"][index])
                    # Room_Size = (self.course_times[course]["Room Size"][index])
                    info = [Lecturer, Classroom, Lecture, Course]
                    lst = [Lecture, "\n", Classroom]
                    text = ''.join(str(element) + ' ' for element in lst)
                    index += 1
                    fg_colour = "white"
                    if Lecture not in list(subject_colours.keys()):
                        bg_colour = choice(self.colours)
                        subject_colours.update({Lecture: bg_colour})
                    else:
                        bg_colour = subject_colours[Lecture]
                else:
                    text = "\n"
                    info = "There is no lecture at this time."
                    bg_colour = "white"
                    fg_colour = "black"
                Style().configure('styling.TButton', foreground=fg_colour, background=bg_colour)
                times = create_time(time, self.hours_in_day)
                text = str(times.time_translate()) + "\n" + text
                btn = Button(New_Window, text=text, command=lambda idx=info: self.create_window(idx),
                             style='styling.TButton')
                btn.grid(column=x, row=y, sticky="NSEW")
                a = Button(New_Window, text="Save in Google Calendar",
                           command=lambda idx=course: self.save_on_google(idx),
                           style='styling.TButton')
                a.grid(column=columns + 1, row=6, sticky="NSEW")
                Grid.columnconfigure(New_Window, x, weight=1)
                Grid.rowconfigure(New_Window, y, weight=1)
                time += 1
        New_Window.mainloop()


class variables():
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.courses_list = []
        self.Subject_Courses = {}
        self.Course_Subjects = {}
        self.lectures = []
        self.lecturers = []
        self.lecturer_free = {}
        self.classroom_free = {}

    def get_keys(self, data, name):
        keys = [key for key, value in data.items() if name in value]
        return keys

    def make_dict(self, list, dictionary):
        d_dict = {}
        for item in list:
            d_dict.update({item: self.get_keys(dictionary, item)})
        return d_dict

    def get_var(self):
        self.lectures = list(dict.fromkeys(list(df["Lecture_ID"].values)))
        for course in self.data_dict["Course(s)"]:
            course = str(course)
            course = course.replace(" ", "")
            self.courses_list.append(course.split(","))
        for i in range(len(self.courses_list)):
            self.Subject_Courses.update({self.data_dict["Course(s)"][i]: self.courses_list[i]})
        courses = list(set(list(chain.from_iterable(self.courses_list))))
        self.Course_Subjects = self.make_dict(courses, self.Subject_Courses)
        lecturer_list = []
        for lecturer in list(df["Lecturer"]):
            lecturer_list.append(lecturer)
        self.lecturers = list(dict.fromkeys(lecturer_list))
        for lecturer in self.lecturers:
            self.lecturer_free.update({lecturer: list(range(0, 65))})
        rooms = list(dict.fromkeys(list(df["Room"].values)))
        for room in rooms:
            self.classroom_free.update({room: list(range(0, 65))})
        for lecturer in self.lecturers:
            times = list(df.loc[df['Lecturer'] == lecturer, 'Time'])
            for time in times:
                self.lecturer_free[lecturer].remove(time)
        for room in rooms:
            times = list(df.loc[df['Room'] == room, 'Time'])
            for time in times:
                self.classroom_free[room].remove(time)
        return self.Course_Subjects, self.lectures, self.classroom_free, self.lecturer_free


if __name__ == "__main__":
    df = pd.read_excel("timetable.xlsx")
    hours_in_day = 13
    var = variables(df)
    Course_Subjects, lectures, classroom_free, lecturer_free = var.get_var()
    gui = GUI(classroom_free, lectures, lecturer_free, Course_Subjects, df, hours_in_day)
    gui.make_times()
    gui.make_timetable()
