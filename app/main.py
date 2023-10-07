# coding: utf-8

import datetime
import os
import sys
from PIL import Image
import pyocr
import configparser
import glob
import re
from myModule.my_file.file_base import FileBase

class Main:
    
    now = datetime.datetime.now()
    formatted_now = now.strftime('%Y%m%d%H%M%S')
    config = configparser.ConfigParser()
    config.read('../conf/config.ini', encoding='utf-8')

    print(config.sections())
    print(config['DEFAULT']['TesseractDirPath'])
    TesseractDirPath = config['DEFAULT']['TesseractDirPath']
    pyocr.tesseract.TESSERACT_CMD = TesseractDirPath

    tel_pattern = '.*?([0-9]{2,3}[-(][0-9]{2,4}[-)][0-9]{3,4})'
    date_pattern = '.*?([20]*[\/年][0-9]{0,2}[\/月][0-9]{0,2}[\/日]?)'
    # year_pattern = '^([20]*)[\/年]'
    year_pattern = '^([20]?[0-9]+)[\/年]'
    month_pattern = '[\/年]([ 0-9]{0,2})[\/月]'
    day_pattern = '.*[\/月]([ 0-9]{0,2})[\/日]?'
    shop_name_pattern = '.*?(\S+[株式|有限|(株)|(有)]会?社?.+)'
    amount_sum_pattern = '.*?(((([1-9]\d*)(,\d{3})*)|0))'
    tax10_pattern = '.*?(((([1-9]\d*)(,\d{3})*)|0))'
    tax8_pattern = '.*?(((([1-9]\d*)(,\d{3})*)|0))'
    free_pattern = '.*?(((([1-9]\d*)(,\d{3})*)|0))'
    no_pattern = '.*?(T\w{13})'

    # プロパティ 電話
    def __init__(self):
        self._tel = ""
        self._shop_name = ""
        self._year = ""
        self._month = ""
        self._day = ""
        self._amount_sum = ""
        self._tax10 = ""
        self._tax10 = ""
        self._free = ""
        self._no = ""
    @property
    def tel(self):
        return self._tel
    
    @tel.setter
    def tel(self, val):
        self._tel = str(val)
    
    # プロパティ 店名
    @property
    def shop_name(self):
        return self._shop_name
    
    @shop_name.setter
    def shop_name(self, val):
        self._shop_name = str(val)
    
    # プロパティ 日付
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, val):
        self._year = str(val)
    
    @property
    def month(self):
        return self._month
    
    @month.setter
    def month(self, val):
        self._month = str(val)
    
    @property
    def day(self):
        return self._day
    
    @day.setter
    def day(self, val):
        self._day = str(val)
    
    # プロパティ 合計金額
    @property
    def amount_sum(self):
        return self._amount_sum
    
    @amount_sum.setter
    def amount_sum(self, val):
        self._amount_sum = str(val)
    
    # プロパティ 税率10パーセント
    @property
    def tax10(self):
        return self._tax10
    
    @tax10.setter
    def tax10(self, val):
        self._tax10 = str(val)
    
    # プロパティ 税率8パーセント
    @property
    def tax8(self):
        return self._tax8
    
    @tax10.setter
    def tax8(self, val):
        self._tax8 = str(val)
    
    # プロパティ 非課税
    @property
    def free(self):
        return self._free
    
    @free.setter
    def free(self, val):
        self._free = str(val)
    
    # プロパティ 登録番号
    @property
    def no(self):
        return self._no
    
    @no.setter
    def no(self, val):
        self._no = str(val)
    
    # 金額の計算
    def cal_money(self, arry_tax):
        total = 0
        for tax in arry_tax:
            total = total + tax
        return total
    def cal_tax10(self, arry_tax10):
        return self.cal_money(arry_tax10)
    def cal_tax8(self, arry_tax8):
        return self.cal_money(arry_tax8)
    def cal_free(self, arry_free):
        return self.cal_money(arry_free)
    
    def write_file(self, path, content):
        with open(path, "w+", encoding='utf-8') as file:
            file.write(content)
        return
    
    # 結果をファイルに出力
    def output_result(self):
        # ファイル名は日時をつける。拡張子はtxtでよい。
        path = self.config['DEFAULT']['Receipt'] + "result\\"
        result_path = path + self.formatted_now + ".txt"
        if os.path.isdir(path):
            context = f"tel: {self.tel}\n"
            context = context + f"shop_name: {self.shop_name}\n"
            context = context + f"expense_date1: {self.year}\n"
            context = context + f"expense_date2: {self.month}\n"
            context = context + f"expense_date3: {self.day}\n"
            context = context + f"amount_sum: {self.amount_sum}\n"
            context = context + f"tax10: {self.tax10}\n"
            context = context + f"tax8: {self.tax8}\n"
            context = context + f"free: {self.free}\n"
            context = context + f"no: {self.no}\n"
            print(f"result_path: {result_path} \n context: {context}")
            self.write_file(result_path, context)
        else:
            print(f"{path}は見つからないため出力しませんでした。")
            return
    
    # 実行用Javascriptコードの作成
    def craete_javascript_code(self):
        file_base = FileBase()
        text = file_base.read_text("./receipt.js")
        replaced_text = ""
        replaced_text = text.replace('@full_phone_number', self.tel)
        replaced_text = replaced_text.replace('@shop_name_by_tel', self.shop_name)
        replaced_text = replaced_text.replace('@expense_date1', self.year)
        replaced_text = replaced_text.replace('@expense_date2', self.month)
        replaced_text = replaced_text.replace('@expense_date3', self.day)
        replaced_text = replaced_text.replace('@amount_sum', self.amount_sum)
        # これはよくわからないから合計金額を入れる
        replaced_text = replaced_text.replace('@taxable_amount_for_10_percent', self.tax10)
        replaced_text = replaced_text.replace('@tax_amount_for_10_percent', self.tax10)
        # これはよくわからないからとりあえず8%の税額を入れる
        replaced_text = replaced_text.replace('@taxable_amount_for_8_percent', self.tax8)
        replaced_text = replaced_text.replace('@tax_amount_for_8_percent', self.tax8)
        replaced_text = replaced_text.replace('@taxable_amount_for_0_percent', self.free)

        replaced_text = replaced_text.replace('@tax_include_exclude_1', "true")
        replaced_text = replaced_text.replace('@tax_rate_1', "true")

        if(self.no == None):
            replaced_text = replaced_text.replace('@registrated_number_is_null_checked', "true")
        # text.replace('\{no\}', self.no)

        # これもファイルに出力する。
        # ファイル名に日時をつける。
        # 結果と同じフォルダーにする。
        result_path = self.config['DEFAULT']['Receipt'] + "result\\" + self.formatted_now + "receipt.js"
        self.write_file(result_path, replaced_text)
        return
    
    # def read_item(self, item_text, pattern):
    #     result = re.search(pattern, item_text)
    #     print(f"item_text: {item_text} / result: {result}")
    #     if(result == None):
    #         return None
    #     else:
    #         print("result: " + result.group(1))
    #         return result.group(1)
        
    def read_item(self, item_text, pattern):
        return item_text
    
    # 電話を読み込み
    def read_tel(self, tel_text):
        result = self.read_item(tel_text, self.tel_pattern)
        if(result != None):
            self.tel = re.sub('[-ー一 ]', '', result)
        return
    
    # 店名を読み込み
    def read_shop_name(self, shop_name_text):
        result = self.read_item(shop_name_text, self.shop_name_pattern)
        if(result != None):
            self.shop_name = result
        return
    
    # 日付を読み込み
    def read_date(self, date_text):
        # self.read_item(date_text, self.date_pattern)
        print(f"date_text: {date_text}")
        year = re.search(self.year_pattern, date_text)
        month = re.search(self.month_pattern, date_text)
        day = re.search(self.day_pattern, date_text)

        if(year != None):
            self.year = year.group(1)
        if(month != None):
            self.month = month.group(1)
        if(day != None):
            self.day = day.group(1)
        print(f"self.year: {self.year} / self.month: {self.month} / self.day: {self.day}")
        return
    
    # 合計金額を読み込み
    def read_amount_sum(self, read_amount_sum_text):
        print(f"read_amount_sum_text: {read_amount_sum_text}")
        result = self.read_item(read_amount_sum_text, self.amount_sum_pattern)
        if(result != None):
            amount_sum = re.sub('[., ]', '', result)
            self.amount_sum = re.sub('[０OoO]', '0', amount_sum)
        return
    
    # 税率10パーセント課税額を読み込み
    def read_tax10(self, tax10_texts):
        arry = list()
        for tax10 in tax10_texts:
            result = re.match(self.tax10_pattern, tax10)
            if(result != None):
                arry.append(result)
        
        self.tax10 = self.cal_tax10(arry)
        return
    
    # 税率8パーセント課税額を読み込み
    def read_tax8(self, tax8_text):
        arry = list()
        for tax8 in tax8_text:
            result = re.match(self.tax8_pattern, tax8)
            if(result != None):
                arry.append(result)
        
        self.tax8 = self.cal_tax8(arry)
        return
    
    # 非課税額を読み込み
    def read_free(self, free_text):
        arry = list()
        for free in free_text:
            result = re.match(self.free_pattern, free)
            if(result != None):
                arry.append(result)
        
        self.free = self.cal_free(arry)
        return
    
    # 登録番号を読み込み
    def read_no(self, no_text):
        result = self.read_item(no_text, self.no_pattern)
        if(result != None):
            self.no = result
        return
    
    # ファイルを読み込む
    def read_file_path(self, target_path):
        print(f"target_path: {target_path}")
        # 利用可能な OCR エンジンをリストで取得する
        tools = pyocr.get_available_tools()
        tool = tools[0]

        # 読み込みテキスト
        text = ""
        if os.path.isfile(target_path):

            img = Image.open(target_path)
            img_gray = img.convert("L")
            # # 画像のファイル保存
            # img_gray.save("../obj/image_gray.png")
            builder = pyocr.builders.TextBuilder(tesseract_layout=6)
            text = tool.image_to_string(img_gray, lang="jpn", builder=builder)
            
            print(text)
        else:
            print("ファイルはない")

        # 取得テキストを返す。
        return text
    
    # (複数)ファイルを読み込む
    def read_file_paths(self, target_path):
        # globを使う
        texts = list()
        paths = glob.glob(target_path)
        for path in paths:
            text = self.read_file_path(path)
            if(text != ""):
                texts.append(text)
        print(f"texts: {texts}")
        return texts
    
    # 領収書
    def receipt(self):
        receipt_file_path = self.config['DEFAULT']['Receipt']
        tel_file_path = receipt_file_path + "tel.png"
        tel_text = self.read_file_path(tel_file_path)
        self.read_tel(tel_text)

        shop_name_file_path = receipt_file_path + "shop_name.png"
        shop_name_text = self.read_file_path(shop_name_file_path)
        self.read_shop_name(shop_name_text)

        date_file_path = receipt_file_path + "date.png"
        date_text = self.read_file_path(date_file_path)
        self.read_date(date_text)

        amount_sun_file_path = receipt_file_path + "amount_sum.png"
        amount_sun_text = self.read_file_path(amount_sun_file_path)
        self.read_amount_sum(amount_sun_text)

        no_file_path = receipt_file_path + "no.png"
        no_text = self.read_file_path(no_file_path)
        self.read_no(no_text)

        tax10_file_path = receipt_file_path + "money\\tax10_*.png"
        # 複数ファイルを読み込むにはglobを使わないとできないかもしれない
        # https://qiita.com/michitaka523/items/2e5452fbd1df61df91ef
        tax10_texts = self.read_file_paths(tax10_file_path)
        self.read_tax10(tax10_texts)

        tax8_file_path = receipt_file_path + "money\\tax8_*.png"
        tax8_texts = self.read_file_paths(tax8_file_path)
        self.read_tax8(tax8_texts)

        free_file_path = receipt_file_path + "money\\free_*.png"
        free_texts = self.read_file_paths(free_file_path)
        self.read_free(free_texts)

        # 結果を出力
        self.output_result()

        # 実行用javascriptを作成
        self.craete_javascript_code()
        return
    
    def main(self):
        self.receipt()
        return

if __name__ == "__main__":
    print("start program")
    start = Main()
    start.main()