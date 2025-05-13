import requests
import pymongo
from mongo_helpers import *

mongo_hostname = 'mongodb://127.0.0.1'
mongo_portnumber = 27017
client = pymongo.MongoClient(mongo_hostname, mongo_portnumber)
db = client['movieData']

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
        subreddit_list = ['politics']
        for subreddit in subreddit_list:
            url = 'https://oauth.reddit.com/r/' + subreddit + '/'
            response = requests.request("GET", url, headers=headers).json()
            after = response['data'].get('after');
            reddit_data = response['data']['children']
            final_reddits = []
            for each_reddit in reddit_data:
                reddit_id = each_reddit.get('data', {}).get('id')
                comments = []
                commentUrl = 'https://oauth.reddit.com/comments/' + reddit_id + '?sort=best&threaded=false'
                commentResponse = requests.request("GET", commentUrl, headers=headers).json();
                comment_data = commentResponse[1]['data']['children']
                for comment in comment_data:
                    if reddit_comment_exists(db, comment['data']['id']):
                        print("Reddit id exists")
                    else:
                        if "subreddit_id" in comment['data'].keys() : 
                            comments.append( {
                                    'parent_id': reddit_id,
                                    'kind': comment['kind'],
                                    'subreddit_id': comment['data']['subreddit_id'],
                                    'id': comment['data']['id'],
                                    'Comment': comment['data']['body'],
                                })
                            save_to_mongo(db, comments, 'politics_comments', False)

                if reddit_id_exists(db, reddit_id):
                    print("Reddit id exists")
                else:
                    filtered_data = get_subreddit_fields(each_reddit)
                    final_reddits.append(filtered_data)
                    save_to_mongo(db, final_reddits, 'politics', False)
            
            while(after is not None):
                url = 'https://oauth.reddit.com/r/' + subreddit + '/?after=' + after
                response = requests.request("GET", url, headers=headers).json()
                after = response['data'].get('after');
                print(after);
                reddit_data = response['data']['children']
                final_reddits = []
                for each_reddit in reddit_data:
                    reddit_id = each_reddit.get('data', {}).get('id')
                    comments = []
                    commentUrl = 'https://oauth.reddit.com/comments/' + reddit_id + '?sort=best&threaded=false'
                    commentResponse = requests.request("GET", commentUrl, headers=headers).json();
                    comment_data = commentResponse['data']
                    for comment in comment_data:
                        if reddit_comment_exists(db, comment['data']['id']):
                            print("Reddit id exists")
                        else:
                            if "subreddit_id" in comment['data'].keys() : 
                                comments.append( {
                                        'parent_id': reddit_id,
                                        'kind': comment['kind'],
                                        'subreddit_id': comment['data']['subreddit_id'],
                                        'id': comment['data']['id'],
                                        'Comment': comment['data']['body'],
                                    })
                                save_to_mongo(db, comments, 'politics_comments', False)
                    if reddit_id_exists(db, reddit_id):
                        print("Reddit id exists")
                    else:
                        filtered_data = get_subreddit_fields(each_reddit)
                        final_reddits.append(filtered_data)
                        save_to_mongo(db, final_reddits, 'politics', False)
                
                    
        return "Data Stored from Reddit"
    except Exception as error:
        print(error)
        pass

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
                    "reddit_date": each_reddit.get('data', {}).get('created'),
                    "created_date": datetime.now()
                }
    
    return filtered_data

def reddit_id_exists(db, reddit_id):
    reddit_details = list(db.politics.find({"id": reddit_id}))
    if len(reddit_details) > 0:
        return True
    else:
        return False
    
def reddit_comment_exists(db, reddit_id):
    reddit_details = list(db.politics_comments.find({"id": reddit_id}))
    if len(reddit_details) > 0:
        return True
    else:
        return False
    
if __name__ == "__main__":
    get_subreddit_data();