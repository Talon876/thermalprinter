import os
from celery import Celery
celeryapp = Celery(__name__, broker=os.environ['TASK_QUEUE_URI'])

import actions
from irclurker import LurkerBot

