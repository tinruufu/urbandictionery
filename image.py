import os
from random import choice

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


COLOURS = [
    ((123, 69, 172), (136, 82, 180)),  # purple
    ((177, 135, 0), (177, 150, 1)),  # yellow
    ((174, 64, 98), (176, 83, 112)),  # pink
    ((70, 167, 42), (86, 182, 60)),  # green
    ((87, 97, 158), (102, 111, 182)),  # blue
    ((49, 149, 161), (75, 157, 165)),  # turquoise
]
SIZE = 1000
PT = SIZE/100
ROOT = os.path.dirname(__file__)


def get_tile():
    tile_dir = os.path.join(ROOT, 'tiles')
    tile_filenames = [
        f for f in os.listdir(tile_dir)
        if os.path.splitext(f)[-1] in ('.jpg', '.png')
    ]
    tile = Image.open(os.path.join(tile_dir, choice(tile_filenames)))
    greyscale = ImageEnhance.Color(tile).enhance(0).convert(mode='L')
    bw = ImageOps.autocontrast(greyscale)
    return ImageOps.colorize(bw, *choice(COLOURS))


def get_font(name, size):
    return ImageFont.truetype(os.path.join(ROOT, 'fonts', name), size)


def make_image(term, definition):
    canvas = Image.new('RGBA', (SIZE, SIZE))
    tile = get_tile()

    x = 0
    while x <= SIZE:
        y = 0
        while y <= SIZE:
            print x, y
            canvas.paste(tile, (x, y))
            y += tile.height
        x += tile.width

    canvas_draw = ImageDraw.Draw(canvas)
    header_font = get_font('Lora-Bold.ttf', PT*7)
    body_font = get_font('DroidSans.ttf', PT*5)
    logo_font = get_font('TypicalWriter.ttf', PT*10)

    canvas_draw.text((PT*4.5, PT*3), term, font=header_font)
    canvas_draw.text((PT*4.5, PT*90), definition, font=body_font)

    b = Image.new('RGBA', (PT*11, PT*10), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(b)
    b_draw.text((0, 0), 'b', font=logo_font)
    d = b.transpose(Image.FLIP_LEFT_RIGHT)
    d_draw = ImageDraw.Draw(d)
    d_draw.text((0, 0), 'u', font=logo_font)

    canvas.paste(d, (PT*84, PT*2), d)

    canvas.save('out.png')


if __name__ == '__main__':
    from sys import argv
    term, definition = argv[1:]
    make_image(term, definition)
