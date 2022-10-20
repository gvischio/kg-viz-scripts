# kg-viz-scripts

This repository contains the scripts I've used to create the custom database for the PSC.

The full description of the project is available through the internal document '2022 Knowdive - The SU2 sdataset'.

Here, I'll just detail the steps that needs to be performed to replicate the process

## General info

In this repository, the datasets themselves are omitted. Therefore, all the paths need to be manually updated to point towards the correct locations of your files.

All the scripts are in Python and use pandas as data tool.

## 0. Input datasets

I've used 3 datasets from the SmartUnitn2 project, that are:
- TimeDiaries [TimeDiaries]
- Points of Interest [LocationEvent]
- GPS data [LocationEventCoordinates]

## 1. Pre-processing

The pre-processing aims at reducing the scope of the labels in the timediaries dataset.

The basic goal was to reduce the length of the strings by using shorter values.

## 2. Creation of Individuals

The goal of this script is to split the three databases into several DBs, one for each user.

This step was performed since, at least on my computer, the POI and GPS databases were too big to be kept in memory by Python.

The timediaries is split by using Pandas.

The other two, instead, are opened and read line by line and arranged into the different files.
I've followed the actual assumption that the datasets are ordered by userID, from 0 to 157.
Therefore, once the ID i'm reading changes, I can start saving the line to a diffrerent file.
For these operations I've used the csv package

## 3. Combination of datasets

This is the core of the process, that combines the three datasets into a single one. The idea is that we want a single dataset containing all the information.

I made the following simplifications to the database:
- each context has a starting and ending time, which defines exactly the time interval of the context as $[start, end[$.
- each context is connected to exactly one location [MAJOR assumption to be considered]
- each context has a 1-to-1 mapping to an event

The same operations are performed over all the users by picking, for each user, all his three datasets.

Firstly, the dates are parsed to make them all having the same format, then the three datasets are sorted by date.

In the timediaries, we are also creating an 'end_time' field, representing the end timestamp for the context, by picking the timestamp of the successive row (since the rows are ordered by date).

Then, we want to associate a value for the coordinates to each context. There might be many coordinates records for any context at the same time. Therefore, I chose to pick only one value among the possibily many ones, the mode = the most common value. If no record at all can be found within the time interval of the context, the coordinates are left empty.

The same exact process is also applied to the POI dataset to extract city name, suburb and region.

Then arrives the association process with the label provided by the user in the "where" column to the points of interest. The idea here is to pick the value from the POI only if its value is coherent with what the user has said about his location. Indeed, it does not make sense to associate a supermarket as the location of a context if the user has said that he is at home, but it makes sense to capture the name of a restaurant if he says that he is eating out. Of course the mapping I've done is not perfect and there's quite a lot of room for improvement, but it worked well enough for my purposes. The process is the following:
1. for each context, I extract the rows from the POI dataset within the time interval
2. I create a DataFrame containing the extracted columns (class, name) from the POI
3. For selected values (Home, Work, ...), nothing is performed and the category is set accordingly
4. For all the remaining values, the DataFrame is filtered according the associations to pick only the values from the "correct categories", then the most common one = the mode is picked and used as the name of the place

## 4. Generated datasets

In the requirements of my work there was the goal of adding people, pictures and objects to the Knowledge Graph.

The people dataset was created by using the free service provided by Mockaroo, which enabled me to specify the data fields I wanted to generate.

The first script (a) can be used to create a dataset of images taken by unspalsh.com. A category can also be specified to reduce the range of possible images. I've used this script three times to generate three datasets for people, events and locations.

The second script (b) instead can be used to create the dataset for the profile pictures of the people.

The object dataset was instead created manually by adding a few objects and a link to an image to represent it.

## 5. User combination

We wanted to create year-long datasets and not only one-mont-long datasets.

To achieve this, I've combined 12 users into a single dataset, producing in this way 11 datasets.

The Jupyter notebook was used to create the data for the combination. I've looked at the values for the locations "Home" and "relatives home" to combine users by location similarity. Since all the users are students at the University of Trento, we can split the students into 3 categories:
- "fuorisede" = those who are coming from outside the region (usually >1.5 hour) and who usually have an apartment in Trento to live in during the lectures period
- "pendolari" = "commuters" = those who live quite near Trento and commute daily to the university.
- Trento residents, who do not have to commute since they live within 30 minutes of the uni.

This categorisation was used to group people by possible common characteristics and daily patterns. In theory, this will make the year-long dataset more consistet.

The txt file contains a broader description of the groups, while the Python script is the one that actually combines the datasets of the selected users: the sequence of the users is randomly shuffled and each user is assigned to a month. To do that, each timestamp in the user's db is modified in its date but not in its hour.

## 6-1. RAW dataset creation:

With this script, the dataset is completed with the insertion of people and pictures, but not objects. 

People are added randomly and with a random quantity to all the contexts where the user has responded to the "who" question with an answer different than "alone". The operations produces a "participants" dataset with pairs (contextID, personID)

Tags about random locations, people and events are added to pictures following a predefined probability distribution.