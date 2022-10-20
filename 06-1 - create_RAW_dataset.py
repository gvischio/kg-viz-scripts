import pandas as pd
from csv import reader, writer
import random

# pick a subset of the available people
people = pd.read_csv("04 - Generated data\humans.csv")
user = (people[:11]).sample(1)
people = people[11:]
people = people.sample(n=random.randint(100,300))
people = pd.concat([user, people], axis=0, ignore_index=True)
people.to_csv("06 - Parsed datasets/1 - raw dataset/humans.csv", index=False)

# preprocess contexts to add ids for context, event and mood for ME
data = pd.read_csv("05 - Year-long datasets/dataset1.csv")
data['contextID'] = data.index + 1
data['locationID'] = data['contextID'].apply(lambda x: "L" + str(x))
data['eventID'] = data['contextID'].apply(lambda x: "E" + str(x))
data['moodID'] = data['contextID'].apply(lambda x: "M1" + str(x))
data['contextID'] = data['contextID'].apply(lambda x: "C" + str(x))

# random creation of the participants to the events
def createParticipants(who, contextID, file):
    who = str(who)
    if((who != "") & (who != "Alone")):
        # choose up to 10 people as participants in the event
        for Hid in people.sample(n=random.randint(1, 10))['id']:
            # define new participant as contextID, personID, role, mood
            file.writerow([contextID, Hid, who[:-1], random.randint(1, 5)])

with open("06 - Parsed datasets/1 - raw dataset/participants.csv", 'w', newline='') as f:
    participants = writer(f)
    participants.writerow(["context","person","role","mood"])

    data.apply(lambda row: createParticipants(row['who'], row['contextID'], participants), axis=1)

# create function and mood IDs for participants
p = pd.read_csv("06 - Parsed datasets/1 - raw dataset/participants.csv")
p['fID'] = p.index
p['fID'] = p['fID'].apply(lambda x: "F1" + str(x))
p['mID'] = p.index
p['mID'] = p['mID'].apply(lambda x: "M2" + str(x))
p.to_csv("06 - Parsed datasets/1 - raw dataset/participants.csv", index=False)

context_counter = len(data.index) + 1

# picture generation [people]
pi_people = pd.read_csv("04 - Generated data\pictures_of_people.csv")
pi_people['of_person'] = pi_people.apply(lambda x: (people['id'].sample(1)).iloc[0], axis=1)
pi_people['of_event'] = pi_people.apply(lambda x: ("E"+str(random.randint(1, context_counter)) if (random.randint(0, 100) > 50) else None), axis=1)
pi_people['of_location'] = pi_people.apply(lambda x: ("L"+str(random.randint(1, context_counter)) if (random.randint(0, 100) > 80) else ""), axis=1)

# picture generation [locations]
pi_location = pd.read_csv("04 - Generated data\pictures_of_places.csv")
pi_location['of_person'] = pi_location.apply(lambda x: (people['id'].sample(1)).iloc[0] if (random.randint(0, 100) > 70) else "", axis=1)
pi_location['of_event'] = pi_location.apply(lambda x: ("E"+str(random.randint(1, context_counter)) if (random.randint(0, 100) > 60) else ""), axis=1)
pi_location['of_location'] = pi_location.apply(lambda x: ("L"+str(random.randint(1, context_counter))), axis=1)

# picture generation [events]
pi_events = pd.read_csv("04 - Generated data\pictures_of_events.csv")
pi_events['of_person'] = pi_events.apply(lambda x: (people['id'].sample(1)).iloc[0] if (random.randint(0, 100) > 60) else "", axis=1)
pi_events['of_event'] = pi_events.apply(lambda x: ("E"+str(random.randint(1, context_counter))), axis=1)
pi_events['of_location'] = pi_events.apply(lambda x: ("L"+str(random.randint(1, context_counter)) if (random.randint(0, 100) > 70) else ""), axis=1)

# add profile pictures of selected humans
photos = pd.read_csv("04 - Generated data\profile_pics.csv")
photos = photos[photos['of_person'].isin(people['id'])]
photos = pd.concat([photos, pi_people], axis=0, ignore_index=True)
photos = pd.concat([photos, pi_location], axis=0, ignore_index=True)
photos = pd.concat([photos, pi_events], axis=0, ignore_index=True)
photos.to_csv("06 - Parsed datasets/1 - raw dataset/pictures.csv", index=False)


