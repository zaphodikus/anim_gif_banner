# anim_gif_banner
An animated gif banner console-typing-simulation for Steam game guides.

I'm using the Pillow library and a favourite tool ffmpeg. This code will thus also work on linux, with minor modifications. This is not a marquee as you can see in the sample. It's meant to simulate someone typing.
![Example clip](sample/shooting.gif "Animated gif")

# How this Python script works

* After loading the desired font, the script will draw the font into a large bitmap to determine it's full extent or text path width.
* Next, we work out the width of the final gif/bitmap using a tenth of the height as a margin on either side, and then fill the background with a gradient.
* We then alternate adding a single character at a time to a copy of the background image, with a cursor.
* The clip is intended for 29fps, so 4 frames per image and cursor gives a typing speed of around 3.5 characters per second.
* To end the clip, we copy the last bitmap (with no cursor blinks,) 4 more times, to give us 1 second of static banner before the video end.
* Feed all the images into ffmpeg to create an avi
* Feed the avi with a filter into ffmpeg to create animated gif with infinite loop.

Frame1

![Frame1](sample/text00.jpg)

Frame2

![Frame2](sample/text01.jpg)

Frame3

![Frame3](sample/text02.jpg)

...

# Requirements
* Python 3.7+

* Installed ffmpeg on your system

* pip install pillow

* pip install colour

# Tweaks
At various points in the script, you will see a TODO comment which allows customization.

* You can specify your own font, and the banner text of course.
* You set the banner size by changing it's height, the script works out the width for you and adds a little padding.
* All temporary files get overwritten, the result gif filename is derived from  the message-text used.

Example: [Steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2267536787)