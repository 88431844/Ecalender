#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from epd_driver import epd4in2_GD
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd4in2_GD Demo")

    epd = epd4in2_GD.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)

    # Drawing on the image
    logging.info("Drawing")
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    LBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 126*298
    LRYimage = Image.new('1', (epd.height, epd.width), 255)  # 126*298
    drawblack = ImageDraw.Draw(LBlackimage)
    drawry = ImageDraw.Draw(LRYimage)

    drawblack.text((2, 0), 'hello world', font=font18, fill=0)
    drawblack.text((2, 20), '4.2inch epd bc', font=font18, fill=0)
    drawblack.text((20, 50), u'微雪电子', font=font18, fill=0)
    drawblack.line((10, 90, 60, 140), fill=0)
    drawblack.line((60, 90, 10, 140), fill=0)
    drawblack.rectangle((10, 90, 60, 140), outline=0)
    drawry.line((95, 90, 95, 140), fill=0)
    drawry.line((70, 115, 120, 115), fill=0)
    drawry.arc((70, 90, 120, 140), 0, 360, fill=0)
    drawry.rectangle((10, 150, 60, 200), fill=0)
    drawry.chord((70, 150, 120, 200), 0, 360, fill=0)
    epd.display(epd.getbuffer(LBlackimage), epd.getbuffer(LRYimage))



except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2_GD.epdconfig.module_exit()
    exit()
