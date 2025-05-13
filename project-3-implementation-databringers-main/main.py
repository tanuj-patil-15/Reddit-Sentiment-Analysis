import utils.mongo_db_client as mdc
import datetime
import math
from flask import Flask,render_template,request
from bson.objectid import ObjectId
import utils.perspective as perspective
import pandas as pd


app = Flask(__name__)


reddit_collection = mdc.getCollection("movieData", "reddit").find()
rd_exist = mdc.getCollection("movieData", "reddit").find({'toxicity': {'$exists': True}})

tmdb_collection = mdc.getCollection("movieData", "tmdb_reviews").find({'toxicity': {'$exists': True}})

politics_comment_collection = mdc.getCollection("movieData", "politics_comments").find()
pc_exist = mdc.getCollection("movieData", "politics_comments").find({'toxicity': {'$exists': True}})


politics_collection = mdc.getCollection("movieData", "politics").find()


df_reddit = pd.DataFrame(reddit_collection)
df_reddit_exist = pd.DataFrame(rd_exist)

df_tmdb = pd.DataFrame(tmdb_collection)

df_politics = pd.DataFrame(politics_collection)

df_comment_politics = pd.DataFrame(politics_comment_collection)
df_pc_exist = pd.DataFrame(pc_exist)


@app.route("/")

def home():
    val = df_comment_politics['_id'].count()
    return render_template("index.html",tc=str(math.floor(val/1000)) + str("K"))

@app.route("/senti/data")
def getSentiData():
    args = request.args
    start_date = args["sd"]
    end_date = args["ed"]
    s1=0
    s1c = 0
    s2=0
    s2c = 0
    s3 = 0
    s3c =0
    dates= []
    start_date = pd.Timestamp(datetime.datetime.strptime( start_date,"%m/%d/%Y" ))
    end_date =pd.Timestamp(datetime.datetime.strptime( end_date,"%m/%d/%Y" ))

    reddit = []
    tmdb = []
    politics = []
   
    print("all fine")

    filtered_df_reddit = df_reddit_exist
    filtered_df_tmdb = df_tmdb
    filtered_df_comment_politics = df_pc_exist
    
    print(filtered_df_comment_politics)
    print(filtered_df_tmdb)
    print(filtered_df_reddit)
    for index, row in filtered_df_reddit.iterrows():
        reddit.append(row["toxicity"])
    
    for index, row in filtered_df_tmdb.iterrows():
        tmdb.append(row["toxicity"])
    
    for index, row in filtered_df_comment_politics.iterrows():
        politics.append(row["toxicity"])

    avg1 = 0
    avg2 = 0
    avg3 = 0
    for item in reddit:
        sub = item
        s1 += sub
        s1c +=1

    for item in tmdb:
        sub = item
        s2 += sub
        s2c +=1

    for item in politics:
        sub = item
        s3 += sub
        s3c +=1 

    subjectives = [s1/s1c,s2/s2c,s3/s3c]
    return render_template("subject.html",sub = subjectives)


@app.route("/daily/data/l")
def getToxiDatal():
    args = request.args
    start_date = args["sd"]
    end_date = args["ed"]
    dates= []
    start_date = pd.Timestamp(datetime.datetime.strptime( start_date,"%m/%d/%Y" ))
    end_date =pd.Timestamp(datetime.datetime.strptime( end_date,"%m/%d/%Y" ))
    df_comment_politics['reddit_date'] = pd.to_datetime(df_comment_politics['reddit_date'])
    filtered_df = df_comment_politics[(df_comment_politics['reddit_date'] >= start_date) & (df_comment_politics['reddit_date'] <= end_date)]
    filtered_df['Date'] = filtered_df['reddit_date'].dt.floor('D')
    grouped_df = filtered_df.groupby('Date').size().reset_index(name='count')

    politics = []
    date = []
    for index, row in grouped_df.iterrows():
        politics.append(row["count"])
        date.append(row["Date"].strftime("%m/%d/%Y"))
    
    print(date)
    print(politics)
    
    return render_template("count.html",count = politics,  dates = date) 

@app.route("/hourly/data/l")
def getHour():
    args = request.args
    start_date = args["sd"]
    end_date = args["ed"]
    dates= []
    start_date = pd.Timestamp(datetime.datetime.strptime( start_date,"%m/%d/%Y" ))
    end_date =pd.Timestamp(datetime.datetime.strptime( end_date,"%m/%d/%Y" ))
    df_comment_politics['reddit_date'] = pd.to_datetime(df_comment_politics['reddit_date'])
    filtered_df = df_comment_politics[(df_comment_politics['reddit_date'] >= start_date) & (df_comment_politics['reddit_date'] <= end_date)]
    filtered_df['Hour'] = filtered_df['reddit_date'].dt.floor('H')
    grouped_df = filtered_df.groupby('Hour').size().reset_index(name='count')
    politics = []
    date = []
    for index, row in grouped_df.iterrows():
        politics.append(row["count"])
        date.append(row["Hour"])
    
    print(date)
    print(politics)
    
    return render_template("count.html",count = politics,  dates = date) 

if __name__ == "__main__":
    app.run(port=8006, debug=True, host="0.0.0.0")    
