from PIL import Image, ImageDraw, ImageFont
import calendar
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
def drawMonth(month=1):
    WEEK = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')
    MONTH = ('January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December')

    # create new blank picture
    img = Image.new('RGB', size=(1920, 1080), color=(255,255,255))
    width, height = img.size
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

    draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            draw.text((colSpace, rowSpace), MONTH[month-1], fill=(0,0,0,), font=ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 87))
            top = rowSpace // 10
            draw.line(xy=[(colSpace, rowSpace*2-top * 2), (colSpace*7.5, rowSpace*2-top * 2)], fill=(0,0,0))
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 7.5, rowSpace * 2 - top * 1)], fill=(0, 0, 0))
            continue
        # draw week title
        draw.text((colSpace*i, rowSpace*2), WEEK[i-1], fill=(0,0,0), font=ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 50))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 1
    for day in cal.itermonthdays(2019, month):
        if day > 0:
            # if weekday, draw with red color
            if col == 6 or col == 7:
                fill = (255, 0, 0)
            else:
                fill = (0, 0, 0)
            draw.text((colSpace * col + 34, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 87))
        col += 1
        # to a new week
        if col == 8:
            col = 1
            row += 1

    img.save(MONTH[month-1] + '.png')

if __name__ == '__main__':
    drawMonth(month=4)

