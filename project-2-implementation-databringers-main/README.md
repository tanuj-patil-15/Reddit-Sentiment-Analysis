## Aspect-based Sentiment Analysis of Movie Reviews

## Description

Aspect-based Sentiment Analysis of movie-related discussions involves analyzing user comments and posts across various social media platforms. People often discuss their movie experiences and opinions online and these discussions can be used to analyze user's sentiments related to various aspects in a movie like ratings, run-time, popularity etc. This project aims to extract specific aspects of movies, such as plot, cast, and production companies, from user-generated content in real-time. By classifying the sentiment associated with each aspect, the project provides insights into which aspects of movies are particularly liked or disliked by users. We perform this analysis on data collected from various movie related subreddits and The Movie Database (TMDB) to enrich our analysis further. This analysis can be valuable for understanding audience sentiments, improving movie quality, and tailoring marketing strategies.

## Team - The DataBringers

* Shreya Adap, sadap1@binghamton.edu
* Vrushali More, vmore@binghamton.edu
* Tanuj Patil, tpatil1@binghamton.edu
* Allen Clement, aclemen4@binghamton.edu


## Methodology for Data Analysis

* `Reddit` 
  *  The reddit data analysis involved extracting the top phrases from the stored data by using the maximum upvote ratio for reddit posts for each subreddit, followed by the creation of a data frame.
  *  Additionally, to conduct descriptive analysis, the number of comments for each subreddit was gathered.
  *  The analysis extended to evaluating the number of comments for the top five subreddits. We have also fetched posts and comments for r/politics subreddit and stored the same in 'politics' and 'politics_comments' collections respectively.

 
* `TMDB` 
  *  For TMDB, the process begins by establishing a connection with MongoDB to retrieve and preprocess the available data. The accessed data is converted into a pickle file, allowing for easy serialization and deserialization of Python objects.
  *  The resulting dataframe, named df_tmdb, incorporates both independent and dependent variables. 
  * Independent variables include id, title, release_date, genre, run_time, overview, production_companies, and status. The dependent variable is popularity.
  * Data cleaning is performed to eliminate null, missing, and duplicate values.
  * The dataset is divided into training and testing sets, and supervised learning, specifically "Linear Regression," is employed. Linear Regression is utilized to predict the target value (popularity) based on independent factors.
  *  The final step involves plotting graphs to visualize and predict popularity based on the identified independent factors.
  *  The methodology combines data preprocessing, model training, and visualization techniques to gain insights into the relationships between various movie-related variables and popularity.


## Project Deliverables
  *  Project deliverables includes python code in Jupyter notebooks. The code can be run in the notebooks itself to visualize all the graphs that are summarized in the project report.
  *  It also includes a python file 'politics.py' used for fetching r/politics subreddit submissions and comments into the mongodb collections 'politics' and 'politics_comments' respectively.
  * The file can be run using python3 /path to politics.py
  * It also includes a config.json file to store all the sensitive information related to APIs, databases and subreddit lists to be fetched.
  * It also includes util folder, containing necessary util files for performing mongodb operations, performing ModerateHateSpeech polarity Analysis and performing Perspective API toxicity analysis.