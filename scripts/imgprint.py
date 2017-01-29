#!/usr/bin/env python
import platform
if 'arm' in platform.machine():
    import Image
else:
    from PIL import Image
from tprinter import *

printer = ThermalPrinter()
printer.set_defaults()
saved_img = Image.open('img.bmp')
printer.print_image(saved_img)
