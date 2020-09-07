#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, requests, json, datetime
import os

reload(sys)
sys.setdefaultencoding('utf8')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2bc
import time
from PIL import Image, ImageDraw, ImageFont

try:
    logging.info("eCalender")

    epd = epd4in2bc.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    logging.info("Clear done")

    font = ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 87)

    calender_image = Image.new('1', (epd.height, epd.width), 255)
    calender_draw = ImageDraw.Draw(calender_image)
    time_draw = ImageDraw.Draw(calender_image)
    time_draw.text((0, 0), time.strftime('%H:%M'), font=font, fill=0)
    # epd.displayBlack(epd.getbuffer(calender_image.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)))

    logging.info("displayBlack ing")
    epd.displayBlack(epd.getbuffer(calender_image))
    logging.info("displayBlack done")

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2bc.epdconfig.module_exit()
    exit()
