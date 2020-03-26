from tkinter import *
import pandas as pd
from MakeData import *
from random import choice, shuffle

Lecturer_Expertise = make_dict("Lecturer Expertise.xlsx")
Lecturer_Free = make_dict("Lecturer Free.xlsx")
Classroom_Free = make_dict("Classroom Occupancy.xlsx")
Lecture_Hours = make_dict("Lecture Hours.xlsx")
Lecture_Times = make_dict("Lecture_Times.xlsx")
Course_Lectures = make_dict("Course_Lectures.xlsx")
Course_Free = make_dict("Course Free.xlsx")
Lab_Free = make_dict("Labs Occupancy.xlsx")
Labs = make_dict("Labs.xlsx")
Classroom_Size = make_dict("Classroom Size.xlsx")
Course_Size = make_dict("Course Size.xlsx")
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
subject_size, suitable_classrooms, lecture_classrooms = classroom_sizes(Subject_Courses, Course_Size, Classroom_Size,
                                                                        Subject_Names)
data = Course_Subjects
for lecture in lectures:
    if (lecture[-4:]) == "-Lab":
        courses = get_keys(data, lecture[0:-4])
        for course in courses:
            Course_Subjects[course].append(lecture)
        new_lecture = lecture
        lecture = lecture[0:-4]
        for lecturer in get_keys(Lecturer_Subjects, lecture):
            Lecturer_Subjects[lecturer].append(new_lecture)


shuffle(lectures)

df = timetable(lectures, Lecturer_Subjects, Lecturer_Free, Classroom_Free, Classrooms, Lecture_Times, Subject_Courses,
               Lecturer_Expertise, Course_Free, Subject_Names, Subject_Lab, Lab_Free, Subjects_Labs, lecture_classrooms,
               subject_size, Classroom_Size)
root = Tk()
root.minsize(200, 200)


def onClick(idx):
    New_Window = Tk()
    course = (btn_list[idx].cget("text"))  # Print the text for the selected button
    time = 0
    index = 0
    for x in range(6):
        for y in range(13):
            if time in new_data[course]["Number"]:
                Lecture = new_data[course]["Lecture"][index]
                Classroom = new_data[course]["Classroom"][index]
                Lecturer = (new_data[course]["Lecturer"][index])
                lst = [Lecture, "\n", Lecturer, "\n", Classroom]
                text = ''.join(str(element) + ' ' for element in lst)[:-1]
                index += 1
                bg_colour = subject_colours[Lecture]
                fg_colour = "White"
            else:
                text = ""
                bg_colour = "White"
                fg_colour = "Black"
            text = time_translate(time)[0] + " - " + str(time_translate(time)[1]) + ".00" + "\n" + text
            btn = Label(New_Window, text=text, bg=bg_colour, fg=fg_colour, borderwidth=1, relief="solid",
                        highlightcolor="white")
            btn.config(font=("Courier", 10))
            btn.grid(column=x, row=y, ipadx=5, ipady=5, sticky="NSEW")
            btn.columnconfigure(1, weight=1)
            time += 1
    New_Window.mainloop()


btn_list = []  # List to hold the button objects
new_data = {}
number_name = {}
lst = list(Course_Subjects.keys())
i = 0
colours = list(pd.read_csv("colours.csv").columns)
subjects_list = list(dict.fromkeys(lectures))
subject_colours = {}
for subject in subjects_list:
    subject_colours.update({subject: choice(colours)})
for i in range(len(lst)):
    course = lst[i]
    subjects = Course_Subjects[course]
    new_df = df[df.Lecture.isin(subjects)]
    new_data.update({course: new_df.to_dict("list")})
    b = Button(root, text=course, command=lambda idx=i: onClick(idx))
    b.grid(column=0, row=i, ipadx=7, ipady=7, sticky="NSEW")
    b.config(font=("Courier", 15))
    btn_list.append(b)  # Append the button to a list
root.mainloop()
