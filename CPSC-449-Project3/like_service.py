# Members: Quang Nguyen, Vinh Tran
# CPSC 449
# Project 3:

import hug
import configparser
import logging.config
import requests
import redis

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/like_service.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

redis = redis.Redis(host="localhost", port="6379")

# Arguments to inject into route functions
#
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Using Routes
######## Like a post ########
@hug.post("/like-post/")
def like_post(response,
    username: hug.types.text,
    post_id: hug.types.number):
    r = requests.get(f'http://127.0.0.1/posts/{post_id}')
    if r.status_code != 200:
        response.status = hug.falcon.HTTP_404
    else:
        if (redis.sismember(username, post_id) == False):
            redis.sadd(username, post_id)
            if (redis.exists(post_id) == 1):
                redis.incrby(post_id, 1)
                redis.zincrby('pposts', 1, post_id)
                return
            else:
                redis.set(post_id, '1')
                redis.zadd('pposts', {post_id : 1})
                return {1123}


######## Show like of a post ########
@hug.get("/like-count/{post_id}")
def show_like_count(response, post_id: hug.types.number):
    r = requests.get(f'http://127.0.0.1/posts/{post_id}')
    if r.status_code != 200:
        response.status = hug.falcon.HTTP_404
    else:
        if (redis.exists(post_id) == 1):
            return redis.get(post_id)
        else:
            return {"post": 0}

######## Show posts that user liked ########
@hug.get("/user-liked/{username}")
def show_user_liked(username: hug.types.text):
    return redis.smembers(username)

######## Show popular posts ########
@hug.get("/popular-posts/")
def show_popular_posts():
    posts = redis.zrange('pposts', 0, 4, desc=True, withscores=True)
    return posts
