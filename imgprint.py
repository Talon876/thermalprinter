#!/usr/bin/env python
from tprinter import *
if 'arm' in platform.machine():
    import Image
else:
    from PIL import Image

printer = ThermalPrinter()
printer.set_defaults()
saved_img = Image.open('img.bmp')
printer.print_image(saved_img)
