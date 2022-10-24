import pandas as pd
from csv import writer
import random
import numpy as np
np.seterr(all="ignore")

# preprocess contexts to add id
data = pd.read_csv("05 - Year-long datasets/dataset1.csv")
data['contextID'] = data.index + 1
data['eventID'] = data['contextID'].apply(lambda x: "E" + str(x))
data['moodID'] = data['contextID'].apply(lambda x: "M1" + str(x))
data['contextID'] = data['contextID'].apply(lambda x: "C" + str(x))

# LOCATIONS

# combining info about the location into a column
cols = ['suburb', 'city', 'region']
data['combined'] = data[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
data['combined'] = data['combined'].apply(lambda x: None if x == "nan_nan_nan" else x)

# split the dataset into groups
others, home = [x for _, x in data.groupby(data['where'] == "Home")]
others, relatives = [x for _, x in others.groupby(others['where'] == "Relatives home")]
others, work = [x for _, x in others.groupby(others['where'] == "Work place")]
others, friends = [x for _, x in others.groupby(others['where'] == "Others home")]
others, labelled = [x for _, x in others.groupby(others['where_categ'].fillna('') != "")]
others = pd.concat([others, friends])

def defineUniqueLocation(dataset, Locations, writerObj, chooseOne=False):
    newID = str("L" + str(len(Locations)+1))
    if(dataset.size > 0):
        if(chooseOne):
            choosen = dataset['combined'].mode()[0]
            subset = dataset[dataset['combined'] == choosen]
        else:
            subset = dataset
        new_location = [newID, 
            subset['where'].fillna("").mode()[0], 
            subset['where_categ'].fillna("").mode()[0], 
            subset['suburb'].fillna("").mode()[0],
            subset['city'].fillna("").mode()[0],
            subset['region'].fillna("").mode()[0],
            str(np.round(np.nanmean((subset[subset['latitude'] > 0])['latitude'].value_counts().index.tolist()[:3]), decimals=6)).replace('nan', ''),
            str(np.round(np.nanmean((subset[subset['longitude'] > 0])['longitude'].value_counts().index.tolist()[:3]), decimals=6)).replace('nan', ''),
            str(np.round(np.nanmean((subset[subset['altitude'] > 0])['altitude'].value_counts().index.tolist()[:3]), decimals=6)).replace('nan', ''),
        ]
        Locations.add(newID)
        writerObj.writerow(new_location)
        dataset['locationID'] = newID
    return dataset

# define the format of the output
output_cols = ['contextID', 'userid', 'date', 'date_end', 'eventID', 'what', 'how', 'moodID', 'mood', 'who', 'locationID' ]

with open("06 - Parsed datasets/02 - Parsed locations/locations.csv", 'w', newline='', encoding='utf-8') as f:
    writerObj = writer(f)
    writerObj.writerow(['locationID', 'label', 'category', 'suburb', 'city', 'region', 'latitude', 'longitude', 'altitude'])

    # Set memorizing the locations (for ID)
    Locations = set()

    # creating static locations like home
    home = defineUniqueLocation(home, Locations, writerObj, chooseOne=True)[output_cols]
    relatives = defineUniqueLocation(relatives, Locations, writerObj, chooseOne=True)[output_cols]
    work = defineUniqueLocation(work, Locations, writerObj, chooseOne=True)[output_cols]
    data2 = pd.concat([home, relatives, work])

    # locations that were labelled
    ldfs = list()
    groups = labelled.groupby('where')
    for name, group in groups:
        ldfs.append(defineUniqueLocation(group, Locations, writerObj)[output_cols])
    labelled = pd.concat(ldfs)
    data2 = pd.concat([data2, labelled])

    # All the others
    ldfs = list()
    groups = others.groupby(['where', 'where_categ', 'suburb', 'city', 'latitude', 'longitude'], dropna=False)
    for name, group in groups:
        ldfs.append(defineUniqueLocation(group, Locations, writerObj)[output_cols])

    # last group contains the empty location. Since I don't know how to intercept that,
    # I replace the locationID of the group with null. Later I will delete such location from the location dataset
    group['locationID'] = None
    ldfs = ldfs[:-1]
    ldfs.append(group[output_cols])
    others = pd.concat(ldfs)
    data2 = pd.concat([data2, others])

    data = data2.sort_index()

# PARTICIPANTS

# pick a subset of the available people
people = pd.read_csv("04 - Generated data\humans.csv")
user = (people[:11]).sample(1)
data['userid'] = user.iloc[0]['id']
people = people[11:]
people = people.sample(n=random.randint(100,300))
people = pd.concat([user, people], axis=0, ignore_index=True)
people.to_csv("06 - Parsed datasets/02 - Parsed locations/humans.csv", index=False)

# assign persons to custom roles
relatives = people[1:3]
partner = people[3:4]
roommates = people[4:9]
classmates = people[9:37]
friends = people[37:83]
colleagues = people[83:96]
others = people[96:]

def writeParticipants(file, contextID, set, label, n):
    for Hid in set.sample(n)['id']:
        # define new participant as contextID, eventID, personID, role, mood
        file.writerow([contextID, contextID.replace('C', 'E'), Hid, label, random.randint(1,5)])

def createParticipants(file, contextID, who):
    who = str(who)
    if(who == 'Classmates'):
        global classmates
        writeParticipants(file, contextID, classmates, who[:-1], random.randint(2, 7))
    elif(who == 'Friends'):
        global friends
        writeParticipants(file, contextID, friends, who[:-1], random.randint(2, 10))
    elif(who == 'Roommates'):
        global roommates
        writeParticipants(file, contextID, classmates, who[:-1], random.randint(1, 4))
    elif(who == 'Relatives'):
        global relatives
        which = random.randint(1,3)
        if (which < 3): file.writerow([contextID, contextID.replace('C', 'E'), relatives.iloc[0]['id'], "Mother", random.randint(1,5)])
        if (which > 1): file.writerow([contextID, contextID.replace('C', 'E'), relatives.iloc[1]['id'], "Father", random.randint(1,5)])
    elif(who == 'Partner'):
        global partner
        file.writerow([contextID, contextID.replace('C', 'E'), partner.iloc[0]['id'], "Partner", random.randint(1,5)])
    if(who == 'Colleagues'):
        global colleagues
        writeParticipants(file, contextID, classmates, who[:-1], random.randint(2, 6))
    elif(who == 'Others'):
        global others
        writeParticipants(file, contextID, others, who[:-1], random.randint(2, 8))

with open("06 - Parsed datasets/02 - Parsed locations/participants.csv", 'w', newline='') as f:
    file = writer(f)
    file.writerow(["context","event", "person","role","mood"])

    data.apply(lambda row: createParticipants(file, row['contextID'], row['who']), axis=1)

# create function and mood IDs for participants
p = pd.read_csv("06 - Parsed datasets/02 - Parsed locations/participants.csv")
p['fID'] = p.index
p['fID'] = p['fID'].apply(lambda x: "F1" + str(x))
p['mID'] = p.index
p['mID'] = p['mID'].apply(lambda x: "M2" + str(x))
p.to_csv("06 - Parsed datasets/02 - Parsed locations/participants.csv", index=False)

# create objects
def createObjects(file, label, how, cid):
    dicti = {
        'Watching videos': ("Watching", random.choice(['O1', 'O2', 'O3'])),
        'Studying': random.choice([('Writing on', 'O2'), ('Reading slides', 'O4'), ('Reading', 'O5'), ('Writing on', 'O6'), ('Reading', 'O6')]),
        'Eating': random.choice([('Using', 'O7'), ('Drinking from', 'O8')]),
        'Hobbies': random.choice([('Assembling', 'O9'), ('Reading', 'O10'), ('Playing videogames', 'O4'), ('Playing videogames', 'O11')]),
        'Other': random.choice([('Assembling', 'O9'), ('Reading', 'O10'), ('Playing videogames', 'O4'), ('Playing videogames', 'O11'), ("Cleaning the house", 'O12')]),
        'Break': ('Drinking', 'O13'),
        'Chatting/calling': ('Using', 'O3'), 
        'Social media': ('Using', 'O3'),
        'Shopping': random.choice([('Using', 'O14'), ('Using', 'O3'), ('Using', 'O15')]),
        'Sport': ('Play', 'O16'),
        'Housework': ("Cleaning the house", 'O12'),
        'Reading/music': random.choice([('Wearing', 'O17'), ('Reading', 'O10')]),
        'Lesson': random.choice([('Writing on', 'O2'), ('Writing on', 'O6')]),
        'Work': ("Typing", "O4")
    }
    act,obj  = ("walking", "") if (how=="By foot") else dicti.get(label, ("",""))
    if(act != ""):
        file.writerow([cid, act, obj])
    
with open("06 - Parsed datasets/02 - Parsed locations/actions.csv", 'w', newline='') as f:
    file = writer(f)
    file.writerow(["contextID", "action", "object"])
    data.apply(lambda row: createObjects(file, row['what'], row['how'], row['contextID']), axis=1)

# create action IDs for actions
p = pd.read_csv("06 - Parsed datasets/02 - Parsed locations/actions.csv")
p['aID'] = p.index
p['aID'] = p['aID'].apply(lambda x: "A1" + str(x))
p['userid'] = user.iloc[0]['id']
p.to_csv("06 - Parsed datasets/02 - Parsed locations/actions.csv", index=False)

# copying over objects
p = pd.read_csv("04 - Generated data/objects.csv")
p.to_csv("06 - Parsed datasets/02 - Parsed locations/objects.csv", index=False)


# PICTURES
events_counter = len(data)
locs = pd.read_csv("06 - Parsed datasets/02 - Parsed locations/locations.csv")
locs.drop(locs.tail(1).index,inplace=True)  # removing last row => empty location
locs.to_csv("06 - Parsed datasets/02 - Parsed locations/locations.csv", index=False)
locations_counter = len(locs)

def createPictures(url_file, tag_file, id, url, prob_person, prob_event, prob_location):
    global locations_counter
    global events_counter
    global people
    url_file.writerow([id, url, ""])

    # person
    if(random.randint(0, 100) >= (100-prob_person)):
        tag_file.writerow([id, (people['id'].sample(1)).iloc[0]])

    # event
    if(random.randint(0, 100) >= (100-prob_event)):
        tag_file.writerow([id, ("E"+str(random.randint(1, events_counter)))])

    # location
    if(random.randint(0, 100) >= (100-prob_location)):
        tag_file.writerow([id, ("L"+str(random.randint(1, locations_counter)))])

def profilePic(url_file, id, url):
    url_file.writerow([id, url, ""])

with open("06 - Parsed datasets/02 - Parsed locations/picture-urls.csv", 'w', newline='') as f1:
    with open("06 - Parsed datasets/02 - Parsed locations/picture-tags.csv", 'w', newline='') as f2:
        urls = writer(f1)
        urls.writerow(["pictureID", "url", "concepts"])
        tags = writer(f2);
        tags.writerow(["pictureID", "entity"])

        events = pd.read_csv("04 - Generated data/pictures_of_events.csv")
        events.apply(lambda row: createPictures(urls, tags, row['pictureID'], row['url'], 60, 100, 50), axis=1)

        places = pd.read_csv("04 - Generated data/pictures_of_places.csv")
        places.apply(lambda row: createPictures(urls, tags, row['pictureID'], row['url'], 50, 60, 100), axis=1)
        
        peopleds = pd.read_csv("04 - Generated data/pictures_of_people.csv")
        peopleds.apply(lambda row: createPictures(urls, tags, row['pictureID'], row['url'], 100, 70, 40), axis=1)

        # add profile pictures of selected humans
        photos = pd.read_csv("04 - Generated data\profile_pics.csv")
        photos = photos[photos['of_person'].isin(people['id'])]
        photos.apply(lambda row: profilePic(urls, row['pictureID'], row['url']), axis=1)

data.to_csv("06 - Parsed datasets/02 - Parsed locations/context_event.csv", index=False)