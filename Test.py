from datetime import datetime
from xlwt import Workbook
def Timetable():
    SubjectsNo = int(input("Please enter the number of subjects: "))
    DayLimit = 6 # For weekdays
    AllSubjects = dict(input("Please insert subjects followed by their number of hours \n").split()
                       for _ in range(SubjectsNo)) # Create a dict of subject followed by the number of hours
    AllSubjects = {str(k): int(v) for k, v in AllSubjects.items()}  # Convert hours from strings to ints
    OnlySubs = list(AllSubjects.keys())  # Getting list of just subjects
    TimeLimitA = int(input("Please input the opening time in 24 hrs: ")) + 1  # Starting time for the day
    TimeLimitB = int(input("Please input the closing time in 24 hrs: ")) + 2  # Closing time for the day
    Name = input("What would you like to name the Excel file: ")


    # Below makes an array for the subjects in order
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

    DayDict = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    wb = Workbook()
    sheet1 = wb.add_sheet('Timetable 1')
    sheet1.write(0,0, "Time")
    NewTimeLimitA = TimeLimitA
    x = 1

    #  Below makes the first column for the time
    while NewTimeLimitA < TimeLimitB-1:
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

    #  Writing subjects into excel sheets into times
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

    wb.save(Name + ".xls") # Save file as an excel sheet
Timetable()