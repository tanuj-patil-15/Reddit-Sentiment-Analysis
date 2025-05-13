from datetime import datetime, timedelta
import requests
import pymongo
import faktory
from mongo_helpers import *
from dotenv import load_dotenv
import os
from faktory import Worker
import logging
load_dotenv()

mongo_hostname = 'mongodb://127.0.0.1'
mongo_portnumber = 27017
client = pymongo.MongoClient(mongo_hostname, mongo_portnumber)
db = client['movieData']
base_url = "https://api.themoviedb.org/3/"
api_key = "2682e7dfbdb68561f1787e7e8aab91f9"

def get_reddit_auth():
    client_id = '9gOtZNvLj2MoT2ehVcQfcw'
    secret_key = 'Rr7Ywf6Z4ulTe-tLAJ_UdKHKF56Tbg'
    username = 'sadap1'
    password = 'databringers'
    auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    data = {'grant_type': 'password',
            'username': username,
            'password': password}
    headers = {'User-Agent': 'User agent'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers

def get_subreddit_data():
    try:
        headers = get_reddit_auth()
        subreddit_list = ['moviereviews','movies','TrueFilm','boxoffice','IMDbFilmGeneral','horror','scifi','filmmakers','animation','DC_Cinematic','Marvel','StarWars','JamesBond','pixar','lotr','harrypotter','flicks','MovieSuggestions']
        for subreddit in subreddit_list:
            url = 'https://oauth.reddit.com/r/' + subreddit
            response = requests.request("GET", url, headers=headers).json()
            reddit_data = response['data']['children']
            #print(reddit_data)
            final_reddits = []
            for each_reddit in reddit_data:
                reddit_id = each_reddit.get('data', {}).get('id')
                if reddit_id_exists(db, reddit_id):
                    print("Reddit id exists")
                else:
                    filtered_data = get_subreddit_fields(each_reddit)
                    final_reddits.append(filtered_data)
                    save_to_mongo(db, final_reddits, 'reddit', False)
                    #print("data stored for subreddit {}".format(subreddit))
        return "Data Stored from Reddit"
    except Exception as error:
        print(error)
        pass
    finally:
        run_at = datetime.utcnow() + timedelta(minutes=10)
        run_at = run_at.isoformat()[:-7] + "Z"
        logging.info(f'scheduling a new catalog crawl to run at: {run_at}')
        with faktory.connection("tcp://:c4619cfc71ebdcb7@localhost:7419") as client:
            client.queue("reddit", args=(), queue="reddits", reserve_for=60, at=run_at)

def get_subreddit_fields(each_reddit):
    filtered_data = {
                    "id" : each_reddit.get('data', {}).get('id'),
                    "subreddit_id": each_reddit.get('data', {}).get('subreddit_id'),
                    "subreddit": each_reddit.get('data', {}).get('subreddit'),
                    "text": each_reddit.get('data', {}).get('selftext'),
                    "author_fullname": each_reddit.get('data', {}).get('author_fullname'),
                    "title": each_reddit.get('data', {}).get('title'),
                    "upvote_ratio": each_reddit.get('data', {}).get('upvote_ratio'),
                    "domain": each_reddit.get('data', {}).get('domain'),
                    "created_date": datetime.now()
                }
    
    return filtered_data

def get_tmdb_data():
    try:
        popular_movie_url = base_url+ "movie/popular"+ "?api_key=" + api_key + "&language=en-US&page=1"
        popular_movie_response = requests.get(popular_movie_url).json()
        if 'results' in popular_movie_response and len(popular_movie_response['results']) > 0:
            popular_movie_list = popular_movie_response['results']
            for popular_movies in popular_movie_list:
                #filtered_data = get_popular_fields(popular_movies)
                movie_id = popular_movies['id']
                if movie_id_exists(db, movie_id):
                    print("Movie id exists")
                else:
                    movie_detail_url =  base_url+ "movie/" + str(movie_id) + "?api_key=" + api_key
                    movie_detail_response = requests.get(movie_detail_url).json()
                    if movie_detail_response:
                        filtered_data = get_popular_fields(popular_movies,movie_detail_response)
                        save_to_mongo(db, filtered_data, 'tmdb_data')
                    else:
                        filtered_data = get_fields(popular_movies)
                        save_to_mongo(db, filtered_data, 'tmdb_data')
                    print("New movie details with movie_id {} added to the database".format(movie_id))
            return "All movie details are updated for date: {}".format(datetime.now)
    except Exception as error:
        print(error)
    finally:
        run_at = datetime.utcnow() + timedelta(minutes=10)
        run_at = run_at.isoformat()[:-7] + "Z"
        logging.info(f'scheduling a new tmdb job to run at: {run_at}')
            
        with faktory.connection("tcp://:c4619cfc71ebdcb7@localhost:7419") as client:
            client.queue("tmdb", args=(), queue="tmdbs", reserve_for=60, at=run_at)
        return "All movie details are updated for date: {}".format(datetime.now)

def movie_id_exists(db, movie_id):
    movie_details = list(db.tmdb_data.find({"id": movie_id}))
    if len(movie_details) > 0:
        return True
    else:
        return False

def reddit_id_exists(db, reddit_id):
    reddit_details = list(db.reddit.find({"id": reddit_id}))
    if len(reddit_details) > 0:
        return True
    else:
        return False

def get_popular_fields(popular_movies,movie_detail_response):
    filtered_data = {
                    "id" : popular_movies['id'],
                    "adult" : popular_movies['adult'],
                    "title": popular_movies['original_title'],
                    "overview": popular_movies['overview'],
                    "popularity": popular_movies['popularity'],
                    "vote_average": popular_movies['vote_average'],
                    "vote_count": popular_movies['vote_count'],
                    "movie_details":movie_detail_response,
                    "created_date": datetime.now()
                }
    return filtered_data

def get_fields(popular_movies):
    filtered_data = {
                    "id" : popular_movies['id'],
                    "adult" : popular_movies['adult'],
                    "title": popular_movies['original_title'],
                    "overview": popular_movies['overview'],
                    "popularity": popular_movies['popularity'],
                    "vote_average": popular_movies['vote_average'],
                    "vote_count": popular_movies['vote_count'],
                    "created_date": datetime.now()
                }
    return filtered_data

if __name__ == "__main__":
    #get_subreddit_data()
    w = Worker("tcp://:c4619cfc71ebdcb7@localhost:7419", queues=["reddits","tmdbs"])
    w.register("reddit", get_subreddit_data)
    w.register("tmdb", get_tmdb_data)
    w.run()