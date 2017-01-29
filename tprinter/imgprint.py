#!/usr/bin/env python
from argparse import ArgumentParser
import serial
import platform
import traceback

from PIL import Image

from tprinter import ThermalPrinter
from imagegen import ImageGenerator
from imagegen import fonts

def easy_print(printer, message=None, font=None, size=None, image=None):
    gen = ImageGenerator()
    img = Image.open(image) if image else gen.render_string(message, font_path=font, font_size=size)
    if printer is not None:
        printer.print_image(img)
    return img

def main():
    ap = ArgumentParser(description='Print text and monochrome bitmaps!')
    ap.add_argument('--message', '-m',
                    help='Message to print')
    ap.add_argument('--font', '-f',
                    default=fonts['hack-bold'],
                    help='Path to ttf font to use')
    ap.add_argument('--size', '-s', type=int,
                    help='Font size', default='24')
    ap.add_argument('--image', '-i',
                    help='Path to image to print')
    ap.add_argument('--dry', '-d', action='store_true',
                    help='If set, won\'t actually print')
    args = ap.parse_args()

    if not args.message and not args.image:
        exit(ap.print_usage())

    if not args.dry:
        try:
            printer = ThermalPrinter()
            printer.set_defaults()
            easy_print(printer, args.message, args.font, args.size, args.image)
        except serial.serialutil.SerialException as ex:
            print('An error occurred while initializing the printer. Use -d to only generate the image.')
            traceback.print_exc(ex)
    else:
        img = easy_print(None, args.message, args.font, args.size, args.image)
        img.save('out.bmp')
        print('Saved out.bmp')

if __name__=='__main__':
    main()

