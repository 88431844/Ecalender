from PIL import Image, ImageDraw, ImageFont
import calendar
import os
import requests
import json
import time

fontPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
weatherImgPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'weatherImg')


# 保定 莲池区 130606

def drawMonth(year=2020, month=1):
	WEEK = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日')
	MONTH = ('一月', '二月', '三月', '四月', '五月', '六月',
	         '七月', '八月', '九月', '十月', '十一月', '十二月')

	# create new blank picture
	img = Image.new('1', size=(400, 300), color=255)
	width, height = img.size
	# rows = 2 titles + 5 rows of days + 2(head + footer)blank
	# cols = 7 cols of week + 1 blank for left + 3 col for pic
	# rows, cols = 9, len(WEEK) + 4
	rows, cols = 8, len(WEEK) + 2
	colSpace, rowSpace = width // cols, height // rows

	# paste your img on the right, 549*1080
	# bgImg = Image.open('cat1.jpg')
	# bgWidth, _ = bgImg.size
	# img.paste(bgImg, box=(width-bgWidth, 0))

	# define font and size
	month_font = fontPath + r'\font-old.ttc'
	weather_font = fontPath + r'\font-old.ttc'
	week_font = fontPath + r'\font-old.ttc'
	day_work_font = fontPath + r'\font-f930.ttc'
	day_rest_font = fontPath + r'\font-old.ttc'
	month_size, week_size, day_size, weather_size = 20, 13, 16, 13

	draw = ImageDraw.Draw(img)
	temperature, weather, reportTime, city = getWeather()
	tomorrowWeather, tomorrowNightTemp, tomorrowDayTemp, todayWeather, todayNightTemp, todayDayTemp = getWeatherMore()
	for i in range(len(WEEK) + 1):
		# draw month title
		if i == 0:
			draw.text((100, 5), u'' + city,
			          fill=0,
			          font=ImageFont.truetype(weather_font, size=weather_size))
			draw.text((100, 20), u'' + temperature + u'°C ',
			          fill=0,
			          font=ImageFont.truetype(weather_font, size=18))
			draw.text((100, 40), u'' + weather,
			          fill=0,
			          font=ImageFont.truetype(weather_font, size=weather_size))
			draw.text((100, 55), u'最高 ' + todayDayTemp + u'|最低 ' + todayNightTemp + u'|更新时间 '+reportTime[13:18],# 墨水屏需要改为[11:16]
			          fill=0,
			          font=ImageFont.truetype(weather_font, size=weather_size))
			draw.text((colSpace, 30), u' ' + MONTH[month - 1],
			          fill=0,
			          font=ImageFont.truetype(month_font, size=month_size))
			top = rowSpace // 10
			draw.line(xy=[(colSpace, rowSpace * 2 - top * 2 + 5), (colSpace * 8, rowSpace * 2 - top * 2 + 5)], fill=0)
			draw.line(xy=[(colSpace, rowSpace * 2 - top * 1 + 5), (colSpace * 8, rowSpace * 2 - top * 1 + 5)], fill=0)
			continue
		# draw week title
		draw.text((colSpace * i, rowSpace * 2 + 10), u' ' + WEEK[i - 1], fill=0,
		          font=ImageFont.truetype(week_font, size=week_size))

	# draw days
	cal = calendar.Calendar(firstweekday=0)
	row, col = 3, 1
	nowDay = time.strftime('%d')
	for day in cal.itermonthdays(year, month):
		if day > 0:
			# if weekday, draw with red color
			if col == 6 or col == 7:
				fill = 0
				day_font = day_rest_font
			else:
				fill = 0
				day_font = day_work_font
			draw.text((colSpace * col + day_size, rowSpace * row), str(day), fill=fill,
			          font=ImageFont.truetype(day_font, size=day_size))
		# 判断输出日期是否为当天，是则在下面画红色方框标识
		if nowDay == str(day):
			xx = colSpace * col + 11
			yy = rowSpace * row + 22
			size = 30
			draw.line(xy=[(xx, yy), (xx + size, yy)], fill=0)
			draw.line(xy=[(xx, yy), (xx, yy - size)], fill=0)
			draw.line(xy=[(xx, yy - size), (xx + size, yy - size)], fill=0)
			draw.line(xy=[(xx + size, yy - size), (xx + size, yy)], fill=0)

		col += 1
		# to a new week
		if col == 8:
			col = 1
			row += 1

	# print("x:" + str(colSpace * col + day_size), "y:" + str(rowSpace * row))
	# print("nowDay:" + nowDay ,"day:" + str(day))

	# shape = [(1551 + 20, 405 + 80), (1551 + 40 , 405 + 60)]
	# draw.rectangle(shape, fill=0)

	# img = img.resize((400, 300), Image.ANTIALIAS)
	# img.save(MONTH[month-1] + '.png')

	bmp_name = {u'晴': 'WQING.BMP', u'阴': 'WYIN.BMP', u'多云': 'WDYZQ.BMP',
	            u'雷阵雨': 'WLZYU.BMP', u'小雨': 'WXYU.BMP', u'中雨': 'WXYU.BMP'}.get(weather, None)
	if not bmp_name:
		if u'雨' in weather:
			bmp_name = 'WYU.BMP'
		elif u'雪' in weather:
			bmp_name = 'WXUE.BMP'
		elif u'雹' in weather:
			bmp_name = 'WBBAO.BMP'
		elif u'雾' in weather or u'霾' in weather:
			bmp_name = 'WWU.BMP'

	# paste your img on the right, 549*1080

	imgPath = weatherImgPath + r'\\' + bmp_name

	bgImg = Image.open(imgPath)
	bgWidth, _ = bgImg.size

	newbgImg = bgImg.resize((40, 40), Image.ANTIALIAS)
	img.paste(newbgImg, box=(150, 10))
	img.show()


def getWeather():
	r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo?city=130606&key=446bdde0691cffb14c1aff83a8912467')
	r.encoding = 'utf-8'
	weatherData = json.loads(r.text.encode('utf-8'))
	w = weatherData['lives'][0]
	temperature = str(w['temperature'].encode('utf-8'), 'utf-8')
	weather = str(w['weather'].encode('utf-8'), 'utf-8')
	reportTime = str(w['reporttime'].encode('utf-8'))
	city = str(w['city'].encode('utf-8'), 'utf-8')
	return temperature, weather, reportTime, city


def getWeatherMore():
	tomorrowWeather = "00"
	tomorrowNightTemp = "00"
	tomorrowDayTemp = "00"
	todayWeather = "00"
	todayNightTemp = "00"
	todayDayTemp = "00"
	try:
		r = requests.get(
			'http://restapi.amap.com/v3/weather/weatherInfo?extensions=all&city=110108&key=446bdde0691cffb14c1aff83a8912467')
		r.encoding = 'utf-8'
		weatherData = json.loads(r.text.encode('utf-8'))
		forecasts = weatherData['forecasts'][0]
		casts = forecasts['casts']
		tomorrowWeather = casts[1]['dayweather']
		tomorrowNightTemp = casts[1]['nighttemp']
		tomorrowDayTemp = casts[1]['daytemp']

		todayWeather = casts[0]['dayweather']
		todayNightTemp = casts[0]['nighttemp']
		todayDayTemp = casts[0]['daytemp']
	except:
		return tomorrowWeather, tomorrowNightTemp, tomorrowDayTemp, todayWeather, todayNightTemp, todayDayTemp
	return tomorrowWeather, tomorrowNightTemp, tomorrowDayTemp, todayWeather, todayNightTemp, todayDayTemp


if __name__ == '__main__':
	drawMonth(year=2020, month=9)
