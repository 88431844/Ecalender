#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'img')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from epd_driver import epd4in2_GD
from PIL import Image, ImageDraw, ImageFont



try:
    logging.info("eCalender")

    epd = epd4in2_GD.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.ClearBlack()
    logging.info("Clear done")

    logging.info(".read calender bmp file")
    Himage = Image.open(os.path.join(picdir, '2020年9月14日日历400_300.bmp'))
    epd.display(epd.getbuffer(Himage))


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2_GD.epdconfig.module_exit()
    exit()