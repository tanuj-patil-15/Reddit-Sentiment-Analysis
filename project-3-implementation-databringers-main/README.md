# Social Media Data Science Pipeline (CS 515-01)

## Project-3 Implementation

### Group 

Shreya Adap, sadap1@binghamton.edu
Vrushali More, vmore@binghamton.edu
Tanuj Patil, tpatil1@binghamton.edu
Allen Clement, aclemen4@binghamton.edu

### Introduction

Aspect-based Sentiment Analysis of movie-related discussions involves analyzing user comments and posts across various social media platforms. People often discuss their movie experiences and opinions online and these discussions can be used to analyze user's sentiments related to various aspects in a movie like ratings, run-time, popularity etc. This project aims to extract specific aspects of movies, such as plot, cast, and production companies, from user-generated content in real-time. By classifying the sentiment associated with each aspect, the project provides insights into which aspects of movies are particularly liked or disliked by users. We perform this analysis on data collected from various movie related subreddits and The Movie Database (TMDB) to enrich our analysis further. This analysis can be valuable for understanding audience sentiments, improving movie quality, and tailoring marketing strategies.

## Intro to Flask

Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.

## Description

* The analysis of Reddit data commenced with the extraction of top phrases from posts, prioritizing those with the highest upvote ratios in each subreddit. This process aimed to identify significant trends within the content. Subsequently, the extracted data was utilized to construct a structured data frame, providing a comprehensive overview of the analyzed Reddit posts. A descriptive analysis was conducted, capturing the number of comments for each subreddit and extending to evaluate comment counts for the top five subreddits. Furthermore, posts and comments specific to the r/politics subreddit were fetched and stored in the 'politics' and 'politics_comments' collections, respectively.

* The TMDB data analysis initiative involved the establishment of a connection with MongoDB to retrieve and preprocess available data. Following retrieval, the data underwent conversion into a pickle file, streamlining the serialization and deserialization of Python objects. The resulting data frame, named df_tmdb, incorporated both independent variables (e.g., id, title, release_date, genre) and the dependent variable, popularity. Rigorous data cleaning procedures were implemented to address null, missing, and duplicate values. The dataset was then divided into training and testing sets, and supervised learning, specifically employing "Linear Regression," was applied to predict popularity based on identified independent factors. Visualization techniques, including plotting graphs, were utilized to enhance the understanding of relationships between various movie-related variables and popularity.

## How to run the project?

Install `Python` and `MongoDB`
Python Lib required-> urllib, requests, json, pandas, pymongo, time, flask, pusher, matplotlib, plotly, os, collections, spotipy, tablet, PrettyTable etc


pip install pandas, numpy, pymongo, schedule, requests and such

In order to find the program files go to VM and in that access the https://github.com/2023-Fall-CS-415-515/project-3-implementation-databringers 
The data is fetched in real time for for all data source. We have used faktory job to run the project 1 files for data collection.
This helps us to achieve visualization of real time data.
In order to execute the code follow the below steps:
1. Go to https://github.com/2023-Fall-CS-415-515/project-3-implementation-databringers
2. MongoDb from one terminal. Below are the commands:
3. Once MongoDB is up simulataneously to start scheduling open another terminal. Same directory as above. 
3. For Web API:Run the command
    python3 main.py
    Application will load on http://localhost:8006/.





