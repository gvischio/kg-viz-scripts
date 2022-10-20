import pandas as pd
from csv import reader, writer

# Splitting diaries
diaries = pd.read_csv("01 - Pre-processed/TimeDiariesPP.csv")
for i in range(158):
    diary = diaries[diaries['userid'] == i]
    diary.to_csv("02 - Individuals/Diaries/diary"+str(i)+".csv", index=False)
del diaries

print("Diaries done")

# Splitting POIs
with open("00 - Input from SU2/LocationEvent.csv", "r") as file:
    csv_reader = reader(file)
    header = next(csv_reader)

    # initialize files
    for ID in range(158):
        with open("02 - Individuals/POIs/Poi"+str(ID) + ".csv", "w", newline='') as out:
            csv_writer = writer(out)
            csv_writer.writerow(header)

    lastID = 0
    file = open("02 - Individuals/POIs/Poi0.csv", "a", newline='')
    csv_writer = writer(file)
    for row in csv_reader:
        id = row[9]
        if(id != lastID):
            file.close()
            file = open("02 - Individuals/POIs/Poi"+str(id) + ".csv", "a", newline='')
            csv_writer = writer(file)
            lastID = id
        csv_writer.writerow(row)

print("POIs done")

# Splitting GPS
with open("00 - Input from SU2/LocationEventCoordinates.csv", "r") as file:
    csv_reader = reader(file)
    header = next(csv_reader)

    # initialize files
    for ID in range(158):
        with open("02 - Individuals/GPS/Gps"+str(ID) + ".csv", "w", newline='') as out:
            csv_writer = writer(out)
            csv_writer.writerow(header)

    lastID = 0
    file = open("02 - Individuals/GPS/Gps0.csv", "a", newline='')
    csv_writer = writer(file)
    for row in csv_reader:
        id = row[10]
        if(id != lastID):
            file.close()
            file = open("02 - Individuals/GPS/Gps"+str(id) + ".csv", "a", newline='')
            csv_writer = writer(file)
            lastID = id
        csv_writer.writerow(row)

print("GPS done")
