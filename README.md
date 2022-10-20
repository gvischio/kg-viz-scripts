# kg-viz-scripts

This repository contains the scripts I've used to create the custom database for the PSC.

The full description of the project is available through the internal document '2022 Knowdive - The SU2 sdataset'.

Here, I'll just detail the steps that needs to be performed to replicate the process

## General info

In this repository, the datasets themselves are omitted. Therefore, all the paths need to be manually updated to point towards the correct locations of your files.

All the scripts are in Python and use pandas as data tool.

## 0. Input datasets

I've used 3 datasets from the SmartUnitn2 project, that are:
- TimeDiaries
- Points of Interest
- GPS data

## 1. Pre-processing

The pre-processing aims at reducing the scope of the labels in the timediaries dataset.

The basic goal was to reduce the length of the strings by using shorter values.