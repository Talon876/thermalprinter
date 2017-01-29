import time

from celery.signals import worker_init

from . import celeryapp
from tprinter import ThermalPrinter

printer = None

@worker_init.connect
def initialize(sender=None, headers=None, body=None, **kwargs):
    global printer
    print('Initializing printer')
    printer = ThermalPrinter()
    printer.set_defaults()

@celeryapp.task
def print_message(msg):
    printer.print_text(msg)

@celeryapp.task
def log_message(msg):
    print(msg)
    return None

