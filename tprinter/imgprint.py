#!/usr/bin/env python
from argparse import ArgumentParser
import platform
if 'arm' in platform.machine():
    import Image
else:
    from PIL import Image
from tprinter import ThermalPrinter

def main():
    printer = ThermalPrinter()
    printer.set_defaults()
    saved_img = Image.open('img.bmp')
    printer.print_image(saved_img)

if __name__=='__main__':
    main()

