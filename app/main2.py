# coding: utf-8

import os
import sys
import cv2
import pytesseract
import configparser

class Main:
    config = configparser.ConfigParser()
    config.read('../conf/config.ini', encoding='utf-8')
    print(config.sections())

    TesseractDirPath = config['DEFAULT']['TesseractDirPath']
    pytesseract.pytesseract.tesseract_cmd = TesseractDirPath

    def main(self):

        path = "C:\\Users\\Yuki\\Downloads\\arubaito1\\seikyuusyo.jpg"

        if os.path.isfile(path):

            # 画像を読み込みます
            print("画像を読み込みます")
            image = cv2.imread(path)

            # 画像をグレースケールに変換します
            print("画像をグレースケールに変換します")
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            print("ファイルはある")
            # 画像内のテキストを抽出します
            print("画像内のテキストを抽出します")
            extracted_text = pytesseract.image_to_string(gray_image, lang='jpn')
        
            # 抽出されたテキストを表示します
            print("抽出されたテキストを表示します")
            print(extracted_text)
        else:
            print("ファイルはない")

        return

if __name__ == "__main__":
    print("start program")
    start = Main()
    start.main()