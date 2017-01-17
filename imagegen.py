#!/usr/bin/python
import platform
if 'arm' in platform.machine():
    import Image, ImageDraw, ImageFont
else:
    from PIL import Image, ImageDraw, ImageFont
import textwrap
import string

PRINTER_WIDTH = 384


class ImageGenerator(object):

    def __init__(self):
        self.wrapper = textwrap.TextWrapper()

    def render_string(self, msg, font=None, font_path=None, font_size=24, accurate=True):
        font = font if font is not None else ImageFont.truetype(font_path, font_size)
        # w is the widest and y is the tallest
        glyph_w, glyph_h = font.getsize('w')[0], font.getsize('y')[1]
        chars_per_line = PRINTER_WIDTH / glyph_w
        self.wrapper.width = chars_per_line

        msg_lines = self.wrapper.wrap(msg)
        # lines may vary in height so loop over all of them when accurate is True
        # otherwise just count each line as the height of a 'y'
        height = sum([font.getsize(h)[1] for h in msg_lines]) if accurate else glyph_h * len(msg_lines)

        image = Image.new('1', (PRINTER_WIDTH, height + glyph_h/3), color='white')
        draw = ImageDraw.Draw(image)

        y = 0
        for line in msg_lines:
            h = font.getsize(line)[1]
            draw.text([0, y], line, font=font)
            y += h
        return image

    def render_image_code(self, image_code, pixel_size=8):
        image_data = ''.join([str(bin(int(s, 16)))[2:].zfill(32) for s in image_code.split('-')])
        img = Image.new('1', (PRINTER_WIDTH, 64), color='white')
        draw = ImageDraw.Draw(img)

        for ty, row in enumerate(chunks(image_data, PRINTER_WIDTH/pixel_size)):
            for tx, cell in enumerate(row):
                if cell == '1':
                    x, y = tx*pixel_size, ty*pixel_size
                    draw.rectangle([x, y, x + pixel_size, y + pixel_size], fill='black')
        return img

    def font_test_image(self, font_path, sizes=None):
        if sizes is None:
            sizes = [16, 24, 32]
        images = []
        for size in sizes:
            image = self.render_string(string.printable, font_path, size)
            images.append(image)

        total_height = sum([w.size[1] for w in images])
        combined_sizes = Image.new('1', (PRINTER_WIDTH, total_height), color='white')
        y = 8
        for img in images:
            w, h = img.size
            combined_sizes.paste(img, [0, y, PRINTER_WIDTH, y + h])
            y += h
        return combined_sizes


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def convert(fname='in.png'):
    input_img = Image.open(fname)
    out_img = input_img.convert('1')
    w, h = out_img.size

    if w > h:
        out_img = out_img.rotate(90, expand=True)
        w, h = out_img.size

    ratio = float(PRINTER_WIDTH) / w
    print('Image is {}x{} ratio for printer is {}'.format(w, h, round(ratio, 2)))
    new_height = int(ratio * h)
    print('Resizing to {}px tall'.format(new_height, ratio))
    out_img = out_img.resize((PRINTER_WIDTH, new_height))
    return out_img


def main():
    gen = ImageGenerator()
    font = ImageFont.truetype('fonts/hack-bold.ttf', 36)
    image = gen.render_string('Well *he* roped ME in to this!', font=font)
    image.save('out.bmp')


if __name__ == '__main__':
    main()
