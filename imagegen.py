from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import string

PRINTER_WIDTH = 384

wrapper = textwrap.TextWrapper()


def render_message(msg, font):
    glyph_w, glyph_h = font.getsize('w')[0], font.getsize('y')[1]
    chars_per_line = PRINTER_WIDTH / glyph_w
    wrapper.width = chars_per_line

    msg_lines = wrapper.wrap(msg)
    height = sum([font.getsize(h)[1] for h in msg_lines])

    image = Image.new('1', (PRINTER_WIDTH, height + glyph_h/2), color='white')
    draw = ImageDraw.Draw(image)
    draw.text([0, 0], '\n'.join(msg_lines), font=font)
    # print('\n'.join(msg_lines))
    # print('{} lines. Image height {}'.format(len(msg_lines), height))
    # print('Glyphs are {}x{}. {} chars per line.'.format(glyph_w, glyph_h, chars_per_line))
    return image


# image
def render_ascii(text_data, pixel_size=8):
    lines = text_data.split('\n')
    image = Image.new('1', (PRINTER_WIDTH, len(lines) * pixel_size), color='white')
    draw = ImageDraw.Draw(image)
    for idx, line in enumerate(lines):
        for i, c in enumerate(line):
            fill = 'black' if c == 'x' else 'white'
            x, y = i * pixel_size, idx * pixel_size
            draw.rectangle([x, y, x + pixel_size, y + pixel_size], fill=fill)
    return image


def render_image_code(image_code, pixel_size=8):
    image_data = ''.join([str(bin(int(s, 16)))[2:].zfill(32) for s in image_code.split('-')])
    img = Image.new('1', (PRINTER_WIDTH, 64), color='white')
    draw = ImageDraw.Draw(img)

    for ty, row in enumerate(chunks(image_data, 48)):
        for tx, cell in enumerate(row):
            if cell == '1':
                x, y = tx*pixel_size, ty*pixel_size
                draw.rectangle([x, y, x + pixel_size, y + pixel_size], fill='black')
    return img


# image
def ascii_fun(height=256, sizes=[1, 2, 4, 8, 16, 32, 64]):
    images = {}

    for pixel_size in sizes:
        thing = [''.join(['.' if random.randrange(1, 100) < 80 else 'x' for i in range(PRINTER_WIDTH / pixel_size)]) for
                 x in
                 range(height / pixel_size)]
        image = render_ascii('\n'.join(thing), pixel_size)
        images[pixel_size] = image

    image = Image.new('1', (PRINTER_WIDTH, height * len(sizes)), color='white')
    for idx, size in enumerate(sizes):
        img = images[size]
        image.paste(img, [0, idx * height, PRINTER_WIDTH, (idx + 1) * height])
    return image


# image[]
def font_test_image(font_path, sizes=[16, 24, 32]):
    images = []
    for size in sizes:
        font = ImageFont.truetype(font_path, size)
        msg = ''.join(open('files/test.txt')) + string.printable
        image = render_message(msg, font)
        images.append(image)

    total_height = sum([w.size[1] for w in images])
    all_sizes = Image.new('1', (PRINTER_WIDTH, total_height), color='white')
    y = 8
    for img in images:
        w, h = img.size
        all_sizes.paste(img, [0, y, PRINTER_WIDTH, y + h])
        y += h
    return all_sizes


# image
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
    out_img.save('out.bmp')


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main():
    size = 16
    font = ImageFont.truetype('fonts/hack-bold.ttf', size)
    msg = ''.join(open('files/test.txt'))
    image = render_message(msg, font)
    image.save('out.bmp')


if __name__ == '__main__':
    main()
