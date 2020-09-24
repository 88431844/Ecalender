#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'screenSaver')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from epd_driver import epd4in2_GD
from PIL import Image



try:
    logging.info("eCalender")

    epd = epd4in2_GD.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.ClearBlack()
    logging.info("Clear done")

    logging.info(".read calender bmp file")
    redImg = Image.new('1', (epd.width, epd.height), 0)
    Himage = Image.open(os.path.join(picdir, 'ma.jpg'))
    flipImg = Himage.transpose(Image.FLIP_LEFT_RIGHT)
    rotateImg = flipImg.rotate(180)
    epd.display(epd.getbuffer(rotateImg),epd.getbuffer(redImg))


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2_GD.epdconfig.module_exit()
    exit()
