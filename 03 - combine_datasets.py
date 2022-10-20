import pandas as pd
from datetime import timedelta

# perform the same operations over all users
for userid in range(158):

    diary = pd.read_csv("02 - Individuals/Diaries/diary"+str(userid)+".csv")
    poi = pd.read_csv("02 - Individuals/POIs/Poi"+str(userid)+".csv")
    gps = pd.read_csv("02 - Individuals/GPS/Gps"+str(userid)+".csv")

    # parsing dates
    diary['date'] = pd.to_datetime(diary['dt'])
    poi['date'] = pd.to_datetime(poi['timestamp'])
    gps['date'] = pd.to_datetime(gps['timestamp'].apply(lambda x: "2018-" + str(x)))

    # set dates all to the same type
    poi['date'] = poi['date'].apply(lambda x: pd.Timestamp(x).tz_localize('UTC'))
    gps['date'] = gps['date'].apply(lambda x: pd.Timestamp(x).tz_localize('UTC'))

    # sort by date
    diary = diary.sort_values(by="date")
    poi = poi.sort_values(by="date")
    gps = gps.sort_values(by="date")

    # creating end timestamp for diaries
    diary['date_end'] = diary['date'].shift(-1)
    diary['date_end'].iloc[-1] = diary['date'].iloc[-1] + timedelta(hours=1)

    # extracting the coordinates
    # I pick the mode of the coordinates in the time interval of the context
    def findCoord(row):
        splice = gps[(gps['date'] >= row['date']) & (gps['date'] < row['date_end'])]
        if splice.size > 0:
            row['latitude'] = splice['latitude'].fillna(0).mode()[0]
            row['longitude'] = splice['longitude'].fillna(0).mode()[0]
            row['altitude'] = splice['altitude'].fillna(0).mode()[0]
        else:   # no value found within the time interval of the context
            row['latitude'] = None
            row['longitude'] = None
            row['altitude'] = None
        return row

    # apply the function to each row of the dataset
    if not gps.empty:
        diary =  diary.apply(lambda x: findCoord(x), axis=1)
    else:
        diary['latitude'] = None
        diary['longitude'] = None
        diary['altitude'] = None

    # creating a mapping between the point of interest based on the given label
    associations = {
        'Other Library': ['library'],
        'Other place': ['pharmacy', 'hairdresser', 'military', 'police', 'recycling', 'chemist', 'atm', 'tourist_info', 
            'town_hall', 'bank', 'christian_catholic', 'post_office', 'hotel', 'hospital', 'swimming_pool', 'laundry',
            'cemetery', 'graveyard', 'cinema', 'dentist', 'dog_park', 'veterinary', 'theme_park', 'nightclub', 'fuel',
            'courthouse', 'prison', 'camp_site', 'beach', 'car_rental', 'castle', 'hostel', 'car_wash'],
        'Outdoors': ['park', 'river', 'track', 'beach', 'playground', 'monument', 'archaeological', 'theme_park'],
        'Shop': ['department_store', 'supermarket', 'clothes', 'furniture_shop', 'florist', 'greengrocer', 'mall', 'shoe_shop', 'vending_cigarette', 'outdoor_shop', 
            'beauty_shop', 'mobile_phone_shop', 'bakery', 'vending_any', 'kiosk', 'jeweller', 'bookshop', 'retail', 'toy_shop', 'vending_machine', 'gift_shop',
            'bicycle_shop', 'sports_shop', 'car_dealership', 'computer_shop', 'car_rental'],
        'Restaurant': ['fast_food', 'bar', 'restaurant', 'cafe', 'vineyard', 'beverages', 'food_court'],
        'Classroom': ['university'],
        'Study hall': ['library', 'university'],
        'Other university place': ['university', 'college', 'library'],
        'UNITN Library': ['library'],
        'Gym': ['sports_centre', 'park', 'playground', 'swimming_pool', 'river', 'track', 'beach', 'stadium'],
        'Cultural': ['theatre', 'museum', 'attraction', 'memorial', 'monument', 'cinema', 'archaeological', 'stadium', 'castle', 'arts_centre']
    }
    # remaining out: 'Relatives home', 'Home', 'Others home','Canteen', 'Work place'

    # extracting info from POIs
    def findPOIandCity(row):
        splice = poi[(poi['date'] >= row['date']) & (poi['date'] < row['date_end'])]
        if(len(splice) > 0):
            row['suburb'] = splice['suburb'].fillna("").mode()[0]
            row['city'] = splice['city'].fillna("").mode()[0]
            row['region'] = splice['region'].fillna("").mode()[0]
        else:
            row['suburb'] = None
            row['city'] = None
            row['region'] = None

    #def findLabel(row):
        #splice = poi[(poi['date'] >= row['date']) & (poi['date'] < row['date_end'])]
        splice = splice[["fclass0", "name0", "fclass1", "name1", "fclass2", "name2", "fclass3", "name3", "fclass4", "name4", "fclass5", "name5", 
                        "fclass6", "name6", "fclass7", "name7", "fclass8", "name8", "fclass9", "name9", "fclass10", "name10",
                        "fclass11", "name11", "fclass12", "name12", "fclass13", "name13", "fclass14", "name14", "fclass15", "name15", 
                        "fclass16", "name16", "fclass17", "name17", "fclass18", "name18", "fclass19", "name19"]]
        lista = list()
        for i in range(20):
            lista.extend(list(zip(splice['fclass'+str(i)], splice['name'+str(i)])))
        labels = pd.DataFrame(lista, columns=['fclass', 'name'])
        labels = labels[labels['fclass'].notna()]

        where = row['where']
        if (where == ""):
            row['where_categ'] = ""
        elif (where in ['Relatives home', 'Home', 'Others home']):
            row['where_categ'] = "residential"

        elif (where in ['Canteen', 'Work place']):
            if labels.size > 0:
                max = labels['name'].fillna("").mode()[0]
                if(max != ""):
                    row['where'] = max
                filt = labels[labels['name'] == max]
                if filt.size > 0:
                    row['where_categ'] = filt['fclass'].fillna("").mode()[0]

        else:
            filt = labels[labels['fclass'].isin(associations.get(where, []))]
            if filt.size > 0:
                max = filt['name'].fillna("").mode()[0]
                if(max != ""):
                    row['where'] = max
                filt = filt[filt['name'] == max]
                if filt.size > 0:
                    row['where_categ'] = filt['fclass'].fillna("").mode()[0]
            
        return row

    # apply the function to each row of the dataset
    if not poi.empty: # to capture a completely empty poi dataset
        diary =  diary.apply(lambda x: findPOIandCity(x), axis=1)
    else:
        diary['suburb'] = None
        diary['city'] = None
        diary['region'] = None
        diary['where_categ'] = None
        # the where column is kept as it is in this case
        
    # save the output dataset
    diary = diary[['userid', 'date', 'date_end', 'what', 'how', 'mood', 'who', 'where', 'where_categ', 'suburb', 'city', 'region', 'latitude', 'longitude', 'altitude']]
    diary.to_csv("03 - Combined/user"+str(userid)+".csv", index=False)

    # logging
    print(userid)