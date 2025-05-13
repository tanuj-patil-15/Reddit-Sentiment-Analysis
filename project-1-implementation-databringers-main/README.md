# Aspect-based Sentiment Analysis of Movie Reviews

## Description

The project focuses on collecting real-time data from two primary sources: Reddit, and TMDB.For Reddit, it gathers domain data from various TV show-related subreddit threads. Lastly, it utilizes four crucial TMDB APIs to obtain TV show-related data, ensuring real-time database updates. The Reddit and TMDB APIs run on a daily schedule, storing data in MongoDB.

## Tech-stack

- `python`: The project is developed and tested using Python.
- `requests`: This popular HTTP networking library for Python (version 2.25.1) is used for API interactions.
- `MongoDB`: The project utilizes a NoSQL document database to store the collected data.
- `PyMongo`: This Python distribution contains tools for working with MongoDB (version 4.3.2).
- `Python-dotenv`: It reads key-value pairs from a .env file and can set them as environment variables (version 2.25.1).

## Two Data-source Documentation

### Reddit

- We are using a list of subreddits:
  - Subreddit list = ['moviereviews', 'movies', 'TrueFilm', 'boxoffice', 'IMDbFilmGeneral', 'horror', 'scifi', 'filmmakers', 'animation',    'DC_Cinematic', 'Marvel', 'StarWars', 'JamesBond', 'pixar', 'lotr', 'harrypotter', 'flicks', 'MovieSuggestions']
  - Subreddit Data Retrieval: Real-time data is retrieved from the selected subreddit list.

### TMDB

- Real-time data is collected from The Movie Database (TMDB), a community-built TV and movie database, using various API endpoints:
  - `/movie/popular`: Get a list of movies ordered by popularity.
  - `/movie/{movie_id}`: Get the top level details of a movie by ID.
  - `/movie/{movie_id}/reviews`: Get the user reviews for a movie.
  - `/movie-reviews`: Get the user reviews for a movie.
  - `/movie/top_rated`: Get a list of movies ordered by rating.

1. To launch the scheduler for Reddit and TMDB APIs, run:
    python3 app.py
2. Run the Reddit stream using:
   python3 reddit.py



## Database schema - MongoDb 

<details>
  <summary markdown="span"> collection_1: reddit </summary>
  
```
{
  "id": "17kd2r6",
  "subreddit_id": "t5_2r23w",
  "subreddit": "moviereviews",
  "text": "I heard alot of bad things about Prey when it first came out so I never gave it a chance until now. Absolutely fulfilled my expectations for a predator movie. It’s follows the first Predator movie in terms of a smaller and weaker opponent out smarting an opponent that seems unkillable. 9/10 in terms of the AVP movies",
  "author_fullname": "t2_593ipxkz",
  "title": "Underestimated Prey",
  "upvote_ratio": 1,
  "domain": "self.moviereviews",
  "created_date": {
    "$date": "2023-10-31T22:10:52.633Z"
  }
}
```
</details>


<details>

  <summary markdown="span"> collection_1: TMDB </summary>

```
{
  "id": 507089,
  "adult": false,
  "title": "Five Nights at Freddy's",
  "overview": "Recently fired and desperate for work, a troubled young man named Mike agrees to take a position as a night security guard at an abandoned theme restaurant: Freddy Fazbear's Pizzeria. But he soon discovers that nothing at Freddy's is what it seems.",
  "popularity": 7124.811,
  "vote_average": 8.469,
  "vote_count": 1012,
  "movie_details": {
    "budget": 20000000,
    "genres": [
      {
        "id": 27,
        "name": "Horror"
      },
      {
        "id": 9648,
        "name": "Mystery"
      }
    ],
    "imdb_id": "tt4589218",
    "original_language": "en",
    "production_companies": [
      {
        "id": 3172,
        "logo_path": "/kDedjRZwO8uyFhuHamomOhN6fzG.png",
        "name": "Blumhouse Productions",
        "origin_country": "US"
      },
      {
        "id": 211144,
        "logo_path": null,
        "name": "Scott Cawthon Productions",
        "origin_country": "US"
      }
    ],
    "revenue": 132700000,
    "runtime": 110,
    "tagline": "Can you survive five nights?",
  },
  "created_date": {
    "$date": "2023-10-31T23:02:46.580Z"
  }
}
```
</details>
