import os
from tempfile import mkdtemp
from random import choice

from PIL import (
    Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageOps,
)


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


def get_mask(size, colour):
    return Image.new('RGBA', size, colour)


def make_image(term, definition):
    canvas = Image.new('RGBA', (SIZE, SIZE))
    text = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text)
    tile = get_tile()

    x = 0
    while x <= SIZE:
        y = 0
        while y <= SIZE:
            canvas.paste(tile, (x, y))
            y += tile.height
        x += tile.width

    header_font = get_font('Lora-Bold.ttf', PT*7)
    body_font = get_font('DroidSans.ttf', PT*5)
    logo_font = get_font('TypicalWriter.ttf', PT*10)

    words = term.split(' ')
    lines = []
    while words:
        line = [words.pop(0)]
        while words and text_draw.textsize(
            ' '.join(line + [words[0]]),
            font=header_font,
        )[0] < 80*PT:
            line.append(words.pop(0))

        lines.append(' '.join(line))

    text_draw.multiline_text(
        (PT*4.5, PT*3), '\n'.join(lines), font=header_font, spacing=PT*2)

    text_draw.text((PT*4.5, PT*90), definition, font=body_font)

    b = Image.new('RGBA', (PT*11, PT*10), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(b)
    b_draw.text((0, 0), 'b', font=logo_font)
    logo = b.transpose(Image.FLIP_LEFT_RIGHT)
    logo_draw = ImageDraw.Draw(logo)
    logo_draw.text((0, 0), 'u', font=logo_font)
    logo = logo.filter(ImageFilter.GaussianBlur(PT/10))

    canvas.paste(get_mask(logo.size, 'white'), (PT*84, PT*2), logo)

    shadow = text.filter(ImageFilter.GaussianBlur(PT/6))

    canvas.paste(get_mask(text.size, (50, 50, 50)), (PT/4, PT/4), shadow)
    canvas.paste(get_mask(text.size, 'white'), (0, 0), text)

    path = os.path.join(mkdtemp(), 'out.png')
    canvas.save(path)
    return path


if __name__ == '__main__':
    from sys import argv
    term, definition = argv[1:]
    make_image(term, definition)
