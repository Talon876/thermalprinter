import time
from . import celeryapp

@celeryapp.task
def log_message(msg):
    print(msg)
    return None

