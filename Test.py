from datetime import datetime
from xlwt import Workbook
def ExcelTime(Array, DayLimit, TimeLimitA, TimeLimitB, Name):
    DayDict = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    wb = Workbook()
    sheet1 = wb.add_sheet('Timetable 1')
    sheet1.write(0,0, "Time")
    NewTimeLimitA = TimeLimitA
    x = 1
    while NewTimeLimitA < TimeLimitB:
        d = datetime.strptime(str(NewTimeLimitA) + ":00", "%H:%M")
        d = d.strftime("%I:%M %p")
        sheet1.write(x, 0, d)
        NewTimeLimitA += 1
        x += 1
    x = 0
    while x < DayLimit:
        sheet1.write(0, x+1, DayDict[x+1])
        x += 1
    Number = 1
    day = 1
    while day < DayLimit:
        time = TimeLimitA+1
        while time < TimeLimitB:
            if time == TimeLimitB:
                day += 1
                time = TimeLimitA
                sheet1.write(time - TimeLimitA, day, Array[Number])
            elif Number == len(Array):
                time == TimeLimitB
                break
            else:
                sheet1.write(time - TimeLimitA, day, Array[Number])
                Number += 1
                time += 1
        day += 1

    wb.save(Name + ".xls")
def GetArray():

    SubjectsNo = int(input("Please enter the number of subjects: "))
    DayLimit = 5
    AllSubjects = dict(input("Please insert subjects followed by their number of hours \n").split() for _ in range(SubjectsNo))
    AllSubjects = {str(k): int(v) for k, v in AllSubjects.items()}  # Convert hours from strings to ints
    OnlySubs = list(AllSubjects.keys())  # Getting list of just subjects
    TimeLimitA = int(input("Please input the opening time in 24 hrs: ")) + 1
    TimeLimitB = int(input("Please input the closing time in 24 hrs: ")) + 1
    Name = input("What would you like to name the Excel file: ")
    day = 0
    Number = 0
    Array = []
    while day < DayLimit:
        time = TimeLimitA
        while SubjectsNo > 0:
            while AllSubjects[OnlySubs[Number]] > 0:
                Array.append(OnlySubs[Number])
                AllSubjects[OnlySubs[Number]] -= 1
                time += 1
            Number += 1
            SubjectsNo -= 1
        day += 1
    ExcelTime(Array, DayLimit, TimeLimitA, TimeLimitB, Name)

GetArray()