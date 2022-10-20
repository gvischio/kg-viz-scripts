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