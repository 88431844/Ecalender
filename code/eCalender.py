#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import calendar
import requests
import json
import logging
import time
import sys

from epd_driver import epd4in2_GD
from PIL import Image, ImageDraw, ImageFont

reload(sys)
sys.setdefaultencoding('utf8')
fontPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

try:
    logging.info("eCalender")

    epd = epd4in2_GD.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    logging.info("Clear done")

    WEEK = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日')
    MONTH = ('一月', '二月', '三月', '四月', '五月', '六月',
             '七月', '八月', '九月', '十月', '十一月', '十二月')

    # create new blank picture
    img = Image.new('RGB', size=(1920, 1080), color=(255, 255, 255))
    width, height = img.size
    # rows = 2 titles + 5 rows of days + 2(head + footer)blank
    # cols = 7 cols of week + 1 blank for left + 3 col for pic
    # rows, cols = 9, len(WEEK) + 4
    rows, cols = 8, len(WEEK) + 2
    colSpace, rowSpace = width // cols, height // rows

    # define font and size
    month_font = fontPath + r'\font-old.ttc'
    weather_font = fontPath + r'\font-old.ttc'
    week_font = fontPath + r'\font-old.ttc'
    day_work_font = fontPath + r'\font-old.ttc'
    day_rest_font = fontPath + r'\font-f930.ttc'
    month_size, title_size, day_size, weather_size = 80, 60, 60, 50

    draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            temperature, weather, reportTime = getWeather()
            draw.text((colSpace, rowSpace + 20), u'温度:' + temperature + u'|天气:' + weather + u'|最后更新:' + reportTime,
                      fill=(0, 0, 0,),
                      font=ImageFont.truetype(weather_font, size=weather_size))
            draw.text((colSpace, rowSpace - 80), u' ' + MONTH[month - 1],
                      fill=(0, 0, 0,),
                      font=ImageFont.truetype(month_font, size=month_size))
            top = rowSpace // 10
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 2), (colSpace * 8, rowSpace * 2 - top * 2)],
                      fill=(0, 0, 0))
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 8, rowSpace * 2 - top * 1)],
                      fill=(0, 0, 0))
            continue
        # draw week title
        draw.text((colSpace * i, rowSpace * 2), u' ' + WEEK[i - 1], fill=(0, 0, 0),
                  font=ImageFont.truetype(week_font, size=title_size))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 1
    nowDay = time.strftime('%d')
    year = time.strftime('%y')
    month = time.strftime('%m')
    for day in cal.itermonthdays(year, month):
        if day > 0:
            # if weekday, draw with red color
            if col == 6 or col == 7:
                fill = (255, 0, 0)
                day_font = day_rest_font
            else:
                fill = (0, 0, 0)
                day_font = day_work_font
            draw.text((colSpace * col + day_size, rowSpace * row), str(day), fill=fill,
                      font=ImageFont.truetype(day_font, size=day_size))
        # 判断输出日期是否为当天，是则在下面话点标识
        if nowDay == str(day):
            shape = [(colSpace * col + day_size + 20, rowSpace * row + 80),
                     (colSpace * col + day_size + 40, rowSpace * row + 60)]
            draw.rectangle(shape, fill=0)

        col += 1
        # to a new week
        if col == 8:
            col = 1
            row += 1

    img = img.resize((400, 300), Image.ANTIALIAS)
    flipImg = img.transpose(Image.FLIP_LEFT_RIGHT)
    rotateImg = flipImg.rotate(180)
    epd.displayBlack(epd.getbuffer(rotateImg))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2_GD.epdconfig.module_exit()
    exit()

# 保定 莲池区 130606
def getWeather():
    r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo?city=130606&key=446bdde0691cffb14c1aff83a8912467')
    r.encoding = 'utf-8'
    weatherData = json.loads(r.text.encode('utf-8'))
    w = weatherData['lives'][0]
    temperature = str(w['temperature'].encode('utf-8'), 'utf-8')
    weather = str(w['weather'].encode('utf-8'), 'utf-8')
    reportTime = str(w['reporttime'].encode('utf-8'), 'utf-8')
    return temperature, weather, reportTime