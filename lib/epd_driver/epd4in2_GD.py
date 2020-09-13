# *****************************************************************************
# * | File        :	  epd4in2_GD.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0
# * | Date        :   2019-06-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from . import epdconfig

# Display resolution
EPD_WIDTH = 400
EPD_HEIGHT = 300


class EPD:

    def __init__(self):
        #done
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    # Hardware reset
    def reset(self):
        #done
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)

    def send_command(self, command):
        #done
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        #done
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        #done
        logging.debug("e-Paper busy")
        while (epdconfig.digital_read(self.busy_pin) == 1):  # 0: idle, 1: busy
            epdconfig.delay_ms(100)

    def init(self):
        #done
        if (epdconfig.module_init() != 0):
            return -1

        self.reset()

        self.ReadBusy()
        self.send_command(0x12)  # soft reset
        self.ReadBusy()

        self.send_command(0x74)  # set analog block control
        self.send_data(0x54)
        self.send_command(0x7E)  # set digital block control
        self.send_data(0x3B)
        self.send_command(0x2B)  # Reduce glitch under ACVCOM
        self.send_data(0x04)
        self.send_data(0x63)

        self.send_command(0x0C)  # Soft start setting
        self.send_data(0x8B)
        self.send_data(0x9C)
        self.send_data(0x96)
        self.send_data(0x0F)

        self.send_command(0x01)  # Set MUX as 300
        self.send_data(0x2B)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x01)

        self.send_command(0x44)  # set Ram-X address start/end position
        self.send_data(0x00)
        self.send_data(0x31)  # RAM x address end at 31h(49+1)*8->400

        self.send_command(0x45)  # set Ram-Y address start/end position
        # self.send_data(0x2B)  # RAM y address start at 12Bh
        # self.send_data(0x01)
        
        self.send_data(0x01)
        self.send_data(0x2B)  # RAM y address start at 12Bh

        self.send_data(0x00)  # RAM y address end at 00h
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x01)  # HIZ

        self.send_command(0x18)
        self.send_data(0X80)

        self.send_command(0x22)
        self.send_data(0XB1)  #Load Temperature and waveform setting.

        self.send_command(0x20)
        self.ReadBusy()    #waiting for the electronic paper IC to release the idle signal


        self.send_command(0x4E)
        self.send_data(0x00)

        self.send_command(0x4F)
        self.send_data(0x2B)
        self.send_data(0x01)

        return 0

    # def getbuffer(self, image):
    #     # logging.debug("bufsiz = ",int(self.width/8) * self.height)
    #     buf = [0xFF] * (int(self.width / 8) * self.height)
    #     image_monocolor = image.convert('1')
    #     imwidth, imheight = image_monocolor.size
    #     pixels = image_monocolor.load()
    #     # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
    #     if (imwidth == self.width and imheight == self.height):
    #         logging.debug("Horizontal")
    #         for y in range(imheight):
    #             for x in range(imwidth):
    #                 # Set the bits for the column of pixels at the current position.
    #                 if pixels[x, y] == 0:
    #                     buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
    #     elif (imwidth == self.height and imheight == self.width):
    #         logging.debug("Vertical")
    #         for y in range(imheight):
    #             for x in range(imwidth):
    #                 newx = y
    #                 newy = self.height - x - 1
    #                 if pixels[x, y] == 0:
    #                     buf[int((newx + newy * self.width) / 8)] &= ~(0x80 >> (y % 8))
    #     return buf

    def getbuffer(self, image):
        buf = [0xFF] * int(self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] == 0:
                    buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        return buf

    def display(self, imageblack, imagered):
        #done
        self.send_command(0x24)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imageblack[i])

        self.send_command(0x26)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])

        self.UpdateDisplay()

    def displayRed(self, imagered):
        #done
        self.send_command(0x26)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])

        self.UpdateDisplay()

    def displayBlack(self, imageblack):
        #done
        self.send_command(0x24)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imageblack[i])

        self.UpdateDisplay()

    def displayPartialRed(self, image):
        #done
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1

        self.send_command(0x26)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(image[i + j * linewidth])

        self.UpdateDisplayPart()

    def displayPartialBlack(self, image):
        #done
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1

        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(image[i + j * linewidth])

        self.UpdateDisplayPart()

    def Clear(self):
        #done
        #clear black
        self.send_command(0x24)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)

        #clear red
        self.send_command(0x26)
        for i in range(0, int(self.width * self.height / 8)):
            # self.send_data(0xFF)
            self.send_data(0x00)

        self.UpdateDisplay()


    def ClearBlack(self):
        #done
        #clear black
        self.send_command(0x24)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)

        self.UpdateDisplay()

    def sleep(self):
        #done
        self.send_command(0x22) #POWER OFF
        self.send_data(0xC3)
        self.send_command(0x20)

        self.send_command(0x10) #enter deep sleep
        self.send_data(0x01)
        epdconfig.delay_ms(100)

        epdconfig.module_exit()

    def UpdateDisplay(self):
        #done
        self.send_command(0x22)
        self.send_data(0xC7)
        self.send_command(0x20)
        self.ReadBusy()

    def UpdateDisplayPart(self):
        self.send_command(0x22)
        self.send_data(0x0c)
        self.send_command(0x20)
        self.ReadBusy()
### END OF FILE ###
