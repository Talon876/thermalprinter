#!/usr/bin/env python
from argparse import ArgumentParser
import serial
import platform
import traceback
if 'arm' in platform.machine():
    import Image
else:
    from PIL import Image
from tprinter import ThermalPrinter
from imagegen import ImageGenerator
from imagegen import fonts

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

    gen = ImageGenerator()
    img = Image.open(args.image) if args.image else gen.render_string(args.message,
                                                                      font_path=args.font,
                                                                      font_size=args.size)
    img.save('out.bmp')

    if not args.dry:
        try:
            printer = ThermalPrinter()
            printer.set_defaults()
            printer.print_image(img)
        except serial.serialutil.SerialException as ex:
            print('An error occurred while initializing the printer. Use -d to only generate the image.')
            traceback.print_exc(ex)
    else:
        print('Saved out.bmp')

if __name__=='__main__':
    main()

