#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, requests, json, datetime
import os
import calendar

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

    calender_image = Image.new('1', (epd.width, epd.height), 255)
    calender_draw = ImageDraw.Draw(calender_image)
    # time_draw = ImageDraw.Draw(calender_image)
    # time_draw.text((0, 0), time.strftime('%H:%M'), font=font, fill=0)
    # # epd.displayBlack(epd.getbuffer(calender_image.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)))
    #
    # flipImg = calender_image.transpose(Image.FLIP_LEFT_RIGHT)
    # rotateImg = flipImg.rotate(180)
    # epd.displayBlack(epd.getbuffer(rotateImg))

    month=9
    WEEK = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')
    MONTH = ('January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December')

    # create new blank picture
    # img = Image.new('RGB', size=(1920, 1080), color=(255,255,255))
    width, height = calender_image.size

    # rows = 2 titles + 5 rows of days + 2(head + footer)blank
    # cols = 7 cols of week + 1 blank for left + 3 col for pic
    rows, cols = 9, len(WEEK) + 4
    colSpace, rowSpace = width // cols, height // rows

    # paste your img on the right, 549*1080
    # bgImg = Image.open('cat1.jpg')
    # bgWidth, _ = bgImg.size
    # img.paste(bgImg, box=(width-bgWidth, 0))

    # define font and size
    # font = ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 87)
    # month_font = r'C:\Windows\Fonts\BAUHS93.TTF'
    # title_font = r'C:\Windows\Fonts\STCAIYUN.TTF'
    # day_font = r'C:\Windows\Fonts\SitkaB.ttc'
    # month_size, title_size, day_size = 80, 58, 34

    # draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            calender_draw.text((colSpace, rowSpace), MONTH[month-1], fill=0, font=ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 16))
            top = rowSpace // 10
            calender_draw.line(xy=[(colSpace, rowSpace*2-top * 2), (colSpace*7.5, rowSpace*2-top * 2)], fill=0)
            calender_draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 7.5, rowSpace * 2 - top * 1)], fill=0)
            continue
        # draw week title
        calender_draw.text((colSpace*i, rowSpace*2), WEEK[i-1], fill=0, font=ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 10))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 1
    for day in cal.itermonthdays(2020, month):
        if day > 0:
            # if weekday, draw with red color
            if col == 6 or col == 7:
                fill = 0
            else:
                fill = 0
            calender_draw.text((colSpace * col + 34, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 16))
        col += 1
        # to a new week
        if col == 8:
            col = 1
            row += 1

    flipImg = calender_image.transpose(Image.FLIP_LEFT_RIGHT)
    rotateImg = flipImg.rotate(180)
    epd.displayBlack(epd.getbuffer(rotateImg))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2bc.epdconfig.module_exit()
    exit()
