import time

from celery.signals import worker_init

from . import celeryapp
from tprinter import ThermalPrinter
from tprinter.imgprint import easy_print
from tprinter.imagegen import fonts

printer = None

@worker_init.connect
def initialize(sender=None, headers=None, body=None, **kwargs):
    global printer
    print('Initializing printer')
    printer = ThermalPrinter(heatTime=95)
    printer.set_defaults()

@celeryapp.task
def print_message(msg):
    easy_print(printer, msg, fonts['hack-bold'], 24)

@celeryapp.task
def log_message(msg):
    print(msg)
    return None

