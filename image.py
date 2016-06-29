import json
import os
import subprocess
from tempfile import mkstemp, mkdtemp

from PIL import Image
from selenium.webdriver import PhantomJS


def make_image(term, definition):
    image_path = os.path.join(mkdtemp(), 'euphamism.png')
    html_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'ud.html',
    )
    url = 'file://{}'.format(html_path)
    driver = PhantomJS(service_log_path=mkstemp()[1])
    driver.set_window_size(4000, 4000)
    driver.get(url)
    driver.execute_script('setText({});'.format(json.dumps({
        'term': term,
        'definition': definition,
    })))
    driver.set_window_size(*driver.execute_script('return getSize();'))
    driver.save_screenshot(image_path)

    # prevent twitter jpegs
    img = Image.open(image_path)
    origin = img.getpixel((0, 0))
    new_origin = origin[:3] + (254,)
    img.putpixel((0, 0), new_origin)
    img.save(image_path)

    subprocess.check_call(['optipng', '-quiet', image_path])

    return image_path


if __name__ == '__main__':
    from sys import argv
    term, definition = argv[1:]
    print make_image(term, definition)
