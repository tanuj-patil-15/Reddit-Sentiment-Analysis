#!/usr/bin/env python
# encoding: utf-8
from datetime import timedelta
import logging
from flask import Flask, request, jsonify
import pymongo
import faktory
from mongo_helpers import *
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

mongo_hostname = 'mongodb://127.0.0.1'
mongo_portnumber = 27017
client = pymongo.MongoClient(mongo_hostname, mongo_portnumber)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

with faktory.connection(faktory="tcp://:c4619cfc71ebdcb7@localhost:7419") as client:
    run_at = datetime.utcnow() + timedelta(minutes=1)
    run_at = run_at.isoformat()[:-7] + "Z"
    logging.info(f'run_at: {run_at}')
    client.queue("reddit", args=(), queue="reddits", reserve_for=60, at=run_at)
    client.queue("tmdb", args=(), queue="tmdbs", reserve_for=60, at=run_at)