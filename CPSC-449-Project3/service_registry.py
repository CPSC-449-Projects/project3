# Members: Quang Nguyen, Vinh Tran
# CPSC 449
# Project 3: Polyglot Persistence and Service Discovery


import hug
import configparser
import logging.config
import requests
import os
import socket

users = []
posts = []
likes = []
polls = []

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/service_registry.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)
# hug.API(__name__).http.serve(port=int(config["port"]["config"]))


# Arguments to inject into route functions
@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Using Routes
######## Return all user service instances ########
@hug.get("/users/")
def get_users():
    return users[0:]

######## Return all timeline service instances ########
@hug.get("/posts/")
def get_posts():
    return posts[0:]

######## Return all like service instances ########
@hug.get("/likes/")
def get_likes():
    return likes[0:]

######## Return all poll service instances ########
@hug.get("/polls/")
def get_polls():
    return polls[0:]

######## Register service instance ########
@hug.post("/register-instance/", status=hug.falcon.HTTP_201)
def register_intances(request,response,
    service: hug.types.text,
    URL: hug.types.text):
    try:
        if (service == "users"):
            users.append(URL)
        elif (service == "posts"):
            posts.append(URL)
        elif (service == "likes"):
            likes.append(URL)
        elif (service == "polls"):
            polls.append(URL)

    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

hug.API(__name__).http.serve(port=1234)
