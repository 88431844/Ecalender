#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import calendar
import os
import requests
import json
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

fontPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
	sys.path.append(libdir)

import logging
from epd_driver import epd4in2_GD
import time
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)


def getWeather():
	r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo?city=130606&key=446bdde0691cffb14c1aff83a8912467')
	r.encoding = 'utf-8'
	weatherData = json.loads(r.text.encode('utf-8'))
	w = weatherData['lives'][0]
	temperature = str(w['temperature'].encode('utf-8'))
	weather = str(w['weather'].encode('utf-8'))
	reportTime = str(w['reporttime'].encode('utf-8'))
	return temperature, weather, reportTime


try:
	logging.info("eCalender")

	epd = epd4in2_GD.EPD()
	logging.info("init and Clear")
	epd.init()
	epd.Clear()
	logging.info("Clear done")

	month = int(time.strftime('%m'))
	year = int(time.strftime('%y'))
	nowDay = int(time.strftime('%y'))

	WEEK = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日')
	MONTH = ('一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月')

	# create new blank picture
	blackImg = Image.new('1', (epd.width, epd.height), 255)
	blackDraw = ImageDraw.Draw(blackImg)
	redImg = Image.new('1', (epd.width, epd.height), 0)
	redDraw = ImageDraw.Draw(redImg)

	width, height = blackImg.size
	# rows = 2 titles + 5 rows of days + 2(head + footer)blank
	# cols = 7 cols of week + 1 blank for left + 3 col for pic
	# rows, cols = 9, len(WEEK) + 4
	rows, cols = 8, len(WEEK) + 2
	colSpace, rowSpace = width // cols, height // rows

	# define font and size
	month_font = os.path.join(fontPath, 'font-old.ttc')
	weather_font = os.path.join(fontPath, 'font-old.ttc')
	week_font = os.path.join(fontPath, 'font-old.ttc')
	day_font = os.path.join(fontPath, 'font-f930.ttc')
	month_size, week_size, day_size, weather_size = 16, 13, 16, 13
	for i in range(len(WEEK) + 1):
		# draw month title
		if i == 0:
			temperature, weather, reportTime = getWeather()
			blackDraw.text((colSpace, rowSpace + 20), u'温度:' + temperature + u'|天气:' + weather + u'|最后更新:' + reportTime,
			               fill=0,
			               font=ImageFont.truetype(weather_font, size=weather_size))
			blackDraw.text((colSpace, rowSpace), u' ' + MONTH[month - 1],
			               fill=0,
			               font=ImageFont.truetype(month_font, size=month_size))
			top = rowSpace // 10
			blackDraw.line(xy=[(colSpace, rowSpace * 2 - top * 2 + 5), (colSpace * 8, rowSpace * 2 - top * 2 + 5)],
			               fill=0)
			blackDraw.line(xy=[(colSpace, rowSpace * 2 - top * 1 + 5), (colSpace * 8, rowSpace * 2 - top * 1 + 5)],
			               fill=0)
			continue
		# draw week title
		blackDraw.text((colSpace * i, rowSpace * 2 + 10), u' ' + WEEK[i - 1], fill=0,
		               font=ImageFont.truetype(week_font, size=week_size))

	# draw days
	cal = calendar.Calendar(firstweekday=0)
	row, col = 3, 1
	for day in cal.itermonthdays(year, month):
		if day > 0:
			# if weekday, draw with red color
			if col == 6 or col == 7:
				fill = 255
				redDraw.text((colSpace * col + day_size, rowSpace * row), str(day), fill=fill,
				             font=ImageFont.truetype(day_font, size=day_size))
			else:
				fill = 0
				blackDraw.text((colSpace * col + day_size, rowSpace * row), str(day), fill=fill,
				               font=ImageFont.truetype(day_font, size=day_size))

		# 判断输出日期是否为当天，是则在下面画红色方框标识
		if nowDay == int(day):
			xx = colSpace * col + 11
			yy = rowSpace * row + 22
			size = 30
			redDraw.line(xy=[(xx, yy), (xx + size, yy)], fill=255)
			redDraw.line(xy=[(xx, yy), (xx, yy - size)], fill=255)
			redDraw.line(xy=[(xx, yy - size), (xx + size, yy - size)], fill=255)
			redDraw.line(xy=[(xx + size, yy - size), (xx + size, yy)], fill=255)

		col += 1
		# to a new week
		if col == 8:
			col = 1
			row += 1

	flipBlackImg = blackImg.transpose(Image.FLIP_LEFT_RIGHT)
	rotateBlackImg = flipBlackImg.rotate(180)

	flipRedImg = redImg.transpose(Image.FLIP_LEFT_RIGHT)
	rotateRedImg = flipRedImg.rotate(180)

	epd.display(epd.getbuffer(rotateBlackImg), epd.getbuffer(rotateRedImg))


except IOError as e:
	logging.info(e)

except KeyboardInterrupt:
	logging.info("ctrl + c:")
	epd4in2_GD.epdconfig.module_exit()
	exit()
