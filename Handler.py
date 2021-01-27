from Checker.ColledgeGroups import *
from PIL import Image
from xlutils.copy import copy
import pytesseract
import os
import xlrd
import excel2img

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


class Handler:
    def __init__(self):
        self.files_number = None

        self.count_files()
        self.clear_last_results()
        self.open_xl_file()
        self.write_and_check_names()
        self.screen_excel_files()

    def count_files(self):
        DIR = "Photos\\HighQuality"
        self.files_number = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    def clear_last_results(self):
        result_files = [os.remove('Result\\' + f) for f in os.listdir('Result')]

    def open_xl_file(self):
        self.rb_4 = xlrd.open_workbook('TablesOfGroups\\ISP-4.xlsx')
        self.rb_sheet_of_4_group = self.rb_4.sheet_by_index(0)

        self.wb_4 = copy(self.rb_4)
        self.wb_sheet_of_4_group = self.wb_4.get_sheet(0)
        self.wb_sheet_of_4_group.col(0).width = 4 * 256
        self.wb_sheet_of_4_group.col(1).width = 28 * 256

        self.rb_3 = xlrd.open_workbook('TablesOfGroups\\ISP-3.xlsx')
        self.rb_sheet_of_3_group = self.rb_3.sheet_by_index(0)

        self.wb_3 = copy(self.rb_3)
        self.wb_sheet_of_3_group = self.wb_3.get_sheet(0)
        self.wb_sheet_of_3_group.col(0).width = 4 * 256
        self.wb_sheet_of_3_group.col(1).width = 28 * 256

    def screen_excel_files(self):
        try:
            excel2img.export_img('Result\\Checked4.xls', 'Result\\Checked4.png', 'Sheet1', None)
        except IOError:
            pass
        try:
            excel2img.export_img('Result\\Checked3.xls', 'Result\\Checked3.png', 'Sheet1', None)
        except IOError:
            pass

    # - Фамилии и имена в списках (ColledgeGroups) и в Exel-таблицах...
    # ... со списком студентов обязаны оканчиваться на букву 'й' или 'ё'.
    # - Все буквы 'й' и 'ё' в списках (ColledgeGroups) и в Exel-таблицах...
    # ... должны быть заменены на 'и' и 'е' соответстенно, если они...
    # ... не стоят последней буквой. К примеру, фамилия...
    # ... 'Зулёхайрий' должна быть записана как 'Зулехаирий'.

    def write_and_check_names(self):
        def formalize_name(name):
            name = name.split()
            name[2] = name[2][0] + '.'
            for word_number in range(2):
                name[word_number] = name[word_number].replace('ё', 'е').replace('й', 'и')
                if name[word_number][-1] == 'и':
                    name[word_number] = name[word_number][0:-1] + 'й'
                if name[word_number][-1] == 'е':
                    name[word_number] = name[word_number][0:-1] + 'ё'
            formalized_name = ' '.join(name)
            return formalized_name

        for image_number in range(1, self.files_number + 1):
            image_data = pytesseract.image_to_string(
                Image.open('Photos\\HighQuality\\' + str(image_number) + '-screen.png'), lang='rus')
            print(formalize_name(image_data))
            if formalize_name(image_data) in teachers:
                continue

            if formalize_name(image_data) in isp_19_4:
                for currentRow in range(25):
                    if self.rb_sheet_of_4_group.row_values(currentRow, 1, 2)[0] == formalize_name(image_data):
                        self.wb_sheet_of_4_group.write(currentRow, 2, '+')
                        continue
                self.wb_4.save('Result\\Checked4.xls')

            if formalize_name(image_data) in isp_19_3:
                for currentRow in range(27):
                    if self.rb_sheet_of_3_group.row_values(currentRow, 1, 2)[0] == formalize_name(image_data):
                        self.wb_sheet_of_3_group.write(currentRow, 2, '+')
                        continue
                self.wb_3.save('Result\\Checked3.xls')
