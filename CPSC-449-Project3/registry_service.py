import threading
import hug
import requests
import time


@hug.startup()
def startup(api=None):
    x = threading.Thread(target=register, args=(1,), daemon = True)
    x.start()

    y = threading.Thread(target=register, args=(2,), daemon = True)
    y.start()

    print("Exit")


def register(name):
    print("Hello from", name)
    time.sleep(1)
    print("Done thread", name)
