from PIL import Image, ImageDraw, ImageFont
import calendar
import os
import requests
import json
import time

fontPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')


#保定 莲池区 130606

def drawMonth(year=2020, month=1):
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

    # paste your img on the right, 549*1080
    # bgImg = Image.open('cat1.jpg')
    # bgWidth, _ = bgImg.size
    # img.paste(bgImg, box=(width-bgWidth, 0))

    # define font and size
    month_font = fontPath + r'\font-old.ttc'
    week_font = fontPath + r'\font-old.ttc'
    day_work_font = fontPath + r'\font-old.ttc'
    day_rest_font = fontPath + r'\font-f930.ttc'
    month_size, title_size, day_size = 80, 60, 60

    draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            temperature, weather = getWeather()
            draw.text((colSpace, rowSpace), u' ' + MONTH[month - 1] + u'|温度:' + temperature + u'|天气:' + weather,
                      fill=(0, 0, 0,),
                      font=ImageFont.truetype(month_font, size=month_size))
            top = rowSpace // 10
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 2), (colSpace * 8, rowSpace * 2 - top * 2)], fill=(0, 0, 0))
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 8, rowSpace * 2 - top * 1)], fill=(0, 0, 0))
            continue
        # draw week title
        draw.text((colSpace * i, rowSpace * 2), u' ' + WEEK[i - 1], fill=(0, 0, 0),
                  font=ImageFont.truetype(week_font, size=title_size))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 1
    nowDay = time.strftime('%d')
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

        # print("x:" + str(colSpace * col + day_size), "y:" + str(rowSpace * row))
        # print("nowDay:" + nowDay ,"day:" + str(day))

    # shape = [(1551 + 20, 405 + 80), (1551 + 40 , 405 + 60)]
    # draw.rectangle(shape, fill=0)

    img = img.resize((400, 300), Image.ANTIALIAS)
    # img.save(MONTH[month-1] + '.png')
    img.show()


def getWeather():
    r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo?city=130606&key=446bdde0691cffb14c1aff83a8912467')
    r.encoding = 'utf-8'
    weatherData = json.loads(r.text.encode('utf-8'))
    w = weatherData['lives'][0]
    temperature = str(w['temperature'].encode('utf-8'), 'utf-8')
    weather = str(w['weather'].encode('utf-8'), 'utf-8')
    return temperature, weather


if __name__ == '__main__':
    drawMonth(year=2020, month=9)
