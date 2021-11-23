# Members: Quang Nguyen, Vinh Tran
# CPSC 449
# Project 3: Polyglot Persistence and Service Discovery


import hug
import configparser
import logging.config
import requests
import time
import threading
import concurrent.futures
import os
import socket

lock = threading.Lock()
'''
users = []
posts = []
likes = []
polls = []
'''
registered_services = {
    "users": [],
    "posts": [],
    "likes": [],
    "polls": []
}

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/service_registry.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)
# hug.API(__name__).http.serve(port=int(config["port"]["config"]))

def health_check():
    lock.acquire()
    '''
    for i in users:
        print("Checking", i)
        res = requests.get(i)
        if res.status_code != 200:
            users.remove(i)
            break;
        else:
            print(i, "is working ...")

    for i in posts:
        print("Checking", i)
        res = requests.get(i)
        if res.status_code != 200:
            users.remove(i)
            break;
        else:
            print(i, "is working ...")

    for i in likes:
        print("Checking", i)
        res = requests.get(i)
        if res.status_code != 200:
            users.remove(i)
            break;
        else:
            print(i, "is working ...")

    for i in polls:
        print("Checking", i)
        res = requests.get(i)
        if res.status_code != 200:
            users.remove(i)
        else:
            print(i, "is working ...")
    '''

    for i in registered_services:
        for j in registered_services[i]:
            print("[CHECKING]", j)
            try:
                res = requests.get(j)
                if res.status_code != 200:
                    registered_services[i].remove(j)
                    break;
            except requests.ConnectionError as e:
                e = "Connection Failed"
                print({"error": e})
                registered_services[i].remove(j)
                break;
            print(j, res.status_code, "\n")

    lock.release()

@hug.startup()
def startup(api=None):
    myThread = threading.Thread(target=health_check, daemon=True)
    myThread.start()
    threading.Timer(10.0, startup).start()

# Arguments to inject into route functions
@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

'''
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
'''

@hug.get("/{service}/")
def get_services(service: hug.types.text):
    services = []
    try:
        for i in registered_services[service]:
            services.append(i)
    except Exception as e:
        response.status = hug.falcon.HTTP_404
    return services

######## Register service instance ########
@hug.post("/register-instance/", status=hug.falcon.HTTP_201)
def register_intances(request,response,
    service: hug.types.text,
    URL: hug.types.text):
    try:
        '''
        if (service == "users"):
            users.append(URL)
        elif (service == "posts"):
            posts.append(URL)
        elif (service == "likes"):
            likes.append(URL)
        elif (service == "polls"):
            polls.append(URL)
        '''
        registered_services[service].append(URL)

    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

hug.API(__name__).http.serve(port=1234)
