import pandas as pd

td = pd.read_csv("00 - Input from SU2\TimeDiaries.csv", usecols= lambda x: x in ['dt', 'what', 'how', 'withwhom', 'where', 'userid', 'mood'])

# mapping of the strings of WHAT column into new values
def repWhat(str):
    rep = {
            "I will go to sleep": "Sleeping",
            "Watcing Youtube, Tv-shows, etc.": "Watching videos",
            "Expired": "",
            "En route": "Travelling",
            "Social media (Facebook, Instagram, etc.)": "Social media",
            "Phone calling; WhatsApp": "Chatting/calling",
            "Coffee break, cigarette, beer, etc.": "Break",
            "Reading a book; listening to music": "Reading/music",
            "Movie Theater, Concert, Exhibit,...": "Cultural event"
        }
    return rep.get(str, str)

td['what'] = td['what'].apply(lambda x: repWhat(x))

# mapping the values for the WHERE column into new values
def repWhere(str):
    rep = {
        "Shop, supermarket, etc": "Shop",
        "Pizzeria, pub, bar, restaurant": "Restaurant",
        "House (friends, others)": "Others home",
        "Relatives Home": "Relatives home",
        "Movie Theater, Museum, ...": "Cultural",
        "Classroom / Laboratory": "Classroom",
        "Classroom / Study hall": "Study hall"
    }
    return rep.get(str, str)

td['where'] = td['where'].apply(lambda x: repWhere(x))

# mapping the values for the WHO column
def repWho(str):
    rep = {
        "Relative(s)": "Relatives",
        "Friend(s)": "Friends",
        "Roommate(s)": "Roommates",
        "Classmate(s)": "Classmates",
        "Colleague(s)": "Colleagues"
    }
    return rep.get(str, str)

td['who'] = td['withwhom'].apply(lambda x: repWho(x))

td = td.drop(columns=['withwhom'])

td.to_csv("01 - Pre-processed\TimeDiariesPP.csv", index=False)
