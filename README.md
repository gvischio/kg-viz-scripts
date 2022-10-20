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