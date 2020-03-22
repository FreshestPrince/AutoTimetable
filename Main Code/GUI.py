from tkinter import *
from SortData import *

root = Tk()

frame = Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N + S + E + W)
grid = Frame(frame)
grid.grid(sticky=N + S + E + W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)

df = timetable(lectures, Lecturer_Subjects, Lecturer_Free, Classroom_Free, Classrooms, Lecture_Times,
               Lecturer_Expertise)
data = (df.loc[df['Lecturer'] == 'Cathryn Bendel  '])
data_dict = (data.to_dict('list'))
root.title('Cathryn Bendel')
time = 0
index = 0
# example values
for x in range(5):
    for y in range(13):
        if time in data_dict["Number"]:
            text = [(data_dict["Classroom"][index])]
            index += 1
        else:
            text = ["Free"]
        btn = Label(frame, text=((time_translate(time)[0], str(time_translate(time)[1])), "\n", text[0]))
        btn.config(font=("Courier", 15))
        btn.grid(column=x, row=y, sticky=N + S + E + W)
        time += 1

for x in range(13):
    Grid.columnconfigure(frame, x, weight=1)

for y in range(5):
    Grid.rowconfigure(frame, y, weight=1)

root.mainloop()
