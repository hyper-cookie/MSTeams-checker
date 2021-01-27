from Checker.MouseMove import *
import pyscreenshot
from PIL import Image
from numpy import array as np_array
import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
filename = '-screen.png'


class ImageBinarizer:
    def __init__(self):
        self.BLACK_COLOR = (0, 0, 0)
        self.WHITE_COLOR = (255, 255, 255)
        self.THRESHOLD = (185, 185, 185)  # 185 и 190 хорошие параметры

        self.actual_image = None
        self.image_pixels = None

        self.new_image_pixels = None

    def get_image_data(self, screenshot_number):
        self.actual_image = Image.open("Photos\\BadQuality\\" + str(screenshot_number) + filename).convert("LA")
        self.image_pixels = self.actual_image.getdata()

    def threshold_image(self, screenshot_number):
        self.new_image_pixels = []

        for pixel in self.image_pixels:
            if pixel < self.THRESHOLD:
                self.new_image_pixels.append(self.BLACK_COLOR)
            else:
                self.new_image_pixels.append(self.WHITE_COLOR)

        new_image = Image.new("RGB", self.actual_image.size)
        new_image.putdata(self.new_image_pixels)
        new_image.save('Photos\\HighQuality\\' + str(screenshot_number) + filename)


class Croper:
    def __init__(self):
        self.mouse_object = MouseMover()
        self.binarizer_object = ImageBinarizer()

        self.x1, self.y1 = 1541, 331
        self.x2, self.y2 = 1826, 392

        self.screenshot_number = 1
        self.blocks_on_monitor = 10

        self.crop_photos()

    def clear_screenshot(self):
        os.remove('Photos\\HighQuality\\' + str(self.screenshot_number) + filename)

    def clear_screenshots(self):
        bad_quality_photos = [os.remove('Photos\\BadQuality\\' + f) for f in os.listdir('Photos\\BadQuality')]
        high_quality_photos = [os.remove('Photos\\HighQuality\\' + f) for f in os.listdir('Photos\\HighQuality')]

    def get_screenshot(self):
        screenshot = np_array(pyscreenshot.grab(bbox=(self.x1, self.y1, self.x2, self.y2)))
        converted_photo = cv2.resize(screenshot, None, fx=5.0, fy=5.0, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('Photos\\BadQuality\\' + str(self.screenshot_number) + filename, converted_photo)

    def crop_photos(self):
        self.clear_screenshots()
        self.mouse_object.start_move_down()

        while True:
            self.get_screenshot()
            self.binarizer_object.get_image_data(self.screenshot_number)
            self.binarizer_object.threshold_image(self.screenshot_number)

            if self.screenshot_number < self.blocks_on_monitor:
                self.y1 += one_block_size
                self.y2 += one_block_size
            else:
                self.mouse_object.block_move_down()

                penult_text_block = pytesseract.image_to_string(
                    Image.open('Photos\\HighQuality\\' + str(self.screenshot_number - 1) + filename), lang='rus')
                last_text_block = pytesseract.image_to_string(
                    Image.open('Photos\\HighQuality\\' + str(self.screenshot_number) + filename), lang='rus')
                if last_text_block == penult_text_block:
                    self.clear_screenshot()
                    break
                if last_text_block[0] == '›' or last_text_block[0] == 'в' or last_text_block[0] == 'о':
                    self.clear_screenshot()
                    break

            self.screenshot_number += 1
