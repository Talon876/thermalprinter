#!/usr/bin/env python
from tprinter import *

printer = ThermalPrinter()
printer.set_defaults()
saved_img = Image.open('img.bmp')
printer.print_image(saved_img)
