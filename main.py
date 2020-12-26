"""
Windows script to generate ZX Spectrum keyboard type keystroke typed-in animations.

1. You will need to install the ZX spectrum font (creative commons, so not included)
2. you will need these modules:
   pip install pillow
   pip install colour
3. Modify constants as needed

"""
from PIL import Image, ImageFont, ImageDraw
from colour import Color
from math import fabs
import subprocess
import os
import re

spectrum_font = r"C:\\Users\\zapho\\AppData\\Local\\Microsoft\\Windows\\Fonts\\zxspeckb_solid.otf"


class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x = x1
        self.y = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return('Rectangle(' + str(self.x) + ',' + str(self.y) + ','
               + str(self.x2) + ',' + str(self.y2)+')')

    def width(self):
        return int(fabs(self.x - self.x2))

    def height(self):
        return int(fabs(self.y - self.y2))


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def get_bounding_box(font, point_size, string):
    h = point_size * 2
    w = h + h*len(string)
    img = Image.new('RGB', (w, h), color=(0, 0, 0))
    d = ImageDraw.Draw(img)

    d.text((1, 1), string, font=font, fill=(255, 255, 255))
    dims = img.getbbox()
    if dims is None:  # zero length or a nonprintable
        return Rectangle(0, 0, 0, 0)
    return Rectangle(*dims)


def gradient(image, start, end):
    w = image.width
    colors = list(Color(rgb_to_hex(*start)).range_to(Color(rgb_to_hex(*end)), w))
    pen = ImageDraw.Draw(image)
    for x in range(0,w):
        pen.line((x, 0, x, image.height), hex_to_rgb(str(colors[x])))


def purge(directory, pattern):
    for f in os.listdir(directory):
        if re.search(pattern, f):
            os.remove(os.path.join(directory, f))


def save_image_animation(message_string,
                         height=90,
                         gradient_left_color=(27, 40, 56),   # Steam UI dark scheme
                         gradient_right_color=(18, 27, 37),  # Steam UI dark scheme
                         text_color=(240, 240, 230),         # not too bright text
                         ):
    purge(os.getcwd(), "text.*.jpg")
    margin = int(height/10)
    font_weight = int(height*1.2)

    fnt_basic = ImageFont.truetype(spectrum_font, font_weight, layout_engine=ImageFont.LAYOUT_BASIC)
    width = get_bounding_box(fnt_basic, font_weight, message_string).width() + margin * 2
    cursor = get_bounding_box(fnt_basic, font_weight, message_string[0])
    # draw a gradient background
    img_background = Image.new('RGB', (width, height))
    gradient(img_background, gradient_left_color, gradient_right_color)
    cursor_start = cursor.height() - int(cursor.height()/8)
    cursor_end = cursor.height()

    # print the message one character at a time
    # output 2 files form each added char of the message, one is with a blinking cursor painted
    output = 0
    for index in range(0, len(message_string) + 1):
        img = img_background.copy()
        d = ImageDraw.Draw(img)
        d.text((margin, 0), message_string[:index], font=fnt_basic, fill=text_color)
        textwidth = get_bounding_box(fnt_basic, font_weight, message_string[:index]).width()
        if ' ' == message_string[index - 1]:  # draw cursor in correct position for non-printable characters
            textwidth += get_bounding_box(fnt_basic, font_weight, 'a').width()
        img.save(f"text{output+1:02}.jpg")

        # make a blinky cursor frame by just adding to the last frame
        if index < len(message_string):
            x = margin + textwidth
            for i in range(cursor_start, cursor_end):
                d.line((x, i, x + cursor.width(), i), fill="white")
        img.save(f"text{output:02}.jpg")
        output += 2
    # duplicate the final frame for a few "frames"
    for i in range(1, 5):
        img.save(f"text{output+i:02}.jpg")



if __name__ == '__main__':
    # output image files
    message = 'Shooting'
    message = message.swapcase()  # makes the spectrum font look better
    save_image_animation(message)

    # convert to avi: ffmpeg -f image2 -i text%d.jpg video.avi
    command = ['ffmpeg.exe', '-f', 'image2', '-framerate', '4', '-i', 'text%02d.jpg', '-y', 'video.avi']
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)

    # use the message text as a filename
    # convert to animated gif using palette
    out_name = "".join([c for c in message.lower() if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    command = ['ffmpeg.exe', '-i', 'video.avi', '-vf', "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
               '-loop', '0', '-y', f"{out_name}.gif"]
    print(" ".join(command))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)

