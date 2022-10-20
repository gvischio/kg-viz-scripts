from csv import reader, writer
from datetime import datetime
import random

combinations = [[13, 24, 30, 40, 53, 77, 93, 107, 118, 126, 136, 155],
 [7, 21, 22, 48, 56, 66, 70, 86, 102, 104, 144, 151],
 [5, 41, 43, 55, 82, 117, 121, 122, 132, 133, 135, 148],
 [4, 14, 16, 20, 44, 61, 68, 74, 95, 109, 114, 115],
 [2, 6, 9, 23, 45, 52, 87, 106, 125, 141, 142, 153],
 [1, 18, 49, 78, 92, 99, 100, 119, 130, 139, 146, 156],
 [0, 19, 25, 33, 34, 37, 46, 60, 97, 120, 128, 149],
 [11, 15, 50, 62, 63, 101, 110, 111, 113, 127, 150, 157],
 [35, 57, 69, 73, 76, 84, 91, 98, 124, 129, 140, 152],
 [10, 26, 27, 39, 42, 47, 51, 67, 81, 85, 88, 112],
 [29, 31, 58, 59, 80, 94, 96, 105, 131, 137, 145, 154]]

def initializeFile(targetID):
    f = open("05 - Year-long datasets/dataset" + str(targetID) + ".csv", "w", newline='')
    with open("03 - Combined/user0.csv", "r") as rf:
        r = reader(rf)
        header = next(r)
        w = writer(f)
        w.writerow(header)
    return w

def concat(newUserID, fileNum, month, writerObj):
    with open("03 - Combined/user"+str(fileNum)+".csv", "r") as rf:
        readerObj = reader(rf)
        header = next(readerObj)

        currentDay = ""
        day = 0
        for row in readerObj:
            # start date
            rowDay = row[1]
            rowHour = rowDay[rowDay.index(' '):]
            rowDay = rowDay[:rowDay.index(' ')]
            if rowDay != currentDay:
                day += 1
                currentDay = rowDay
            row[1] = f"2018-{month:02d}-{day:02d}" + rowHour

            # end date
            rowDay = row[2]
            rowHour = rowDay[rowDay.index(' '):]
            rowDay = rowDay[:rowDay.index(' ')]
            if rowDay != currentDay:
                day += 1
                currentDay = rowDay
            try:
                datetime.strptime(f"2018-{month:02d}-{day:02d}", '%Y-%m-%d')
            except:
                month += 1
                day = 1
                row[2] = f"2018-{month:02d}-{day:02d}" + rowHour
                row[0] = "H" + str(newUserID)
                writerObj.writerow(row)
                break
            else:
                row[2] = f"2018-{month:02d}-{day:02d}" + rowHour
                row[0] = "H" + str(newUserID)
                writerObj.writerow(row)

currentUser = 1
for seq in combinations:
    random.shuffle(seq)

    writeObj = initializeFile(currentUser)
    month = 1
    for elem in seq:
        concat(currentUser, elem, month, writeObj)
        month += 1

    currentUser += 1
