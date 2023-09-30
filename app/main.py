# coding: utf-8

import os
import sys
from PIL import Image
import pyocr
import configparser

class Main:
    
    config = configparser.ConfigParser()
    config.read('../conf/config.ini', encoding='utf-8')

    # プロパティ
    @property
    def tel(self):
        return self.tel
    
    @tel.setter
    def tel(self, tel):
        self.tel = tel
        return

    # ファイルを読み込む
    def read_file_path(self, target_path):

        # ファイルがある場合はtrue、ない場合はfalseを返す。
        return

    # 電話を読み込み
    def read_tel(self):
        # 電話番号をプロパティに入れる。
        self.tel = ""
        return
    
    # 金額の計算
    def cal_money(self):
        return
    def cal_tax10(self):
        return
    def cal_tax8(self):
        return
    def cal_free(self):
        return
    
    # 結果をファイルに出力
    def output_result(self):
        # ファイル名は日時をつける。拡張子はtxtでよい。
        return
    
    # 実行用Javascriptコードの作成
    def craete_javascript_code(self):
        # これもファイルに出力する。
        # ファイル名に日時をつける。
        # 結果と同じフォルダーにする。
        return
    
    # 電話を読み込み
    # 店名を読み込み
    # 日付を読み込み
    # 合計金額を読み込み
    # 税率10パーセント課税額を読み込み
    # 税率8パーセント課税額を読み込み
    # 非課税額を読み込み
    # 登録番号を読み込み

    # 領収書
    def receipt(self):
        receipt_file_path = self.config['DEFAULT']['Receipt']
        tel_file_path = receipt_file_path + "tel.png"
        self.read_file_path()
        shop_name_file_path = receipt_file_path + "shop_name.png"
        self.read_file_path()
        date_file_path = receipt_file_path + "date.png"
        self.read_file_path()
        amount_sun_file_path = receipt_file_path + "amount_sun.png"
        self.read_file_path()
        no_file_path = receipt_file_path + "no.png"
        self.read_file_path()
        tax10_file_path = receipt_file_path + "money\\tax10_*.png"
        # 複数ファイルを読み込むにはglobを使わないとできないかもしれない
        # https://qiita.com/michitaka523/items/2e5452fbd1df61df91ef
        self.read_file_path()
        tax8_file_path = receipt_file_path + "money\\tax8_*.png"
        self.read_file_path()
        free_file_path = receipt_file_path + "money\\free_*.png"
        self.read_file_path()
        
        # それぞれのテキストをプロパティに保持
        # 金額の計算を行う
        self.cal_money
        return
    
    def main(self):

        TesseractDirPath = self.config['DEFAULT']['TesseractDirPath']
        pyocr.tesseract.TESSERACT_CMD = TesseractDirPath
        # 利用可能な OCR エンジンをリストで取得する
        tools = pyocr.get_available_tools()
        tool = tools[0]

        # path = "C:\\Users\\Yuki\\Downloads\\arubaito1\\seikyuusyo.jpg"
        path = "C:\\Users\\Yuki\\Documents\\アルバイト\\pdfimages\\無題.png"

        if os.path.isfile(path):

            img = Image.open(path)
            img_gray = img.convert("L")
            # 画像のファイル保存
            img_gray.save("../obj/image_gray.png")
            builder = pyocr.builders.TextBuilder(tesseract_layout=6)
            text = tool.image_to_string(img_gray, lang="jpn", builder=builder)
            
            print(text)
        else:
            print("ファイルはない")

        return

if __name__ == "__main__":
    print("start program")
    start = Main()
    start.main()