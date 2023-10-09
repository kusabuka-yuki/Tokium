import sys
import os
import pyocr
from PIL import Image
import configparser

class Main:

    DEBUG_MODE = False
    config = configparser.ConfigParser()
    config.read('../conf/config.ini', encoding='utf-8')

    if DEBUG_MODE:
        print(config.sections())
    #     print(config['DEFAULT']['TesseractDirPath'])
    # TesseractDirPath = config['DEFAULT']['TesseractDirPath']
    TesseractDirPath = "C:\\Users\\Yuki\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
    pyocr.tesseract.TESSERACT_CMD = TesseractDirPath

    # ファイルを読み込む
    def read_file_path(self, target_path):
        if self.DEBUG_MODE:
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
            if self.DEBUG_MODE:
                print("ファイルはない")

        # 取得テキストを返す。
        return text
    
    def main(self):
        if len(sys.argv) > 1: 
            self.read_file_path(sys.argv[1])
        else:
            if self.DEBUG_MODE:
                print(f"引数が足りません。: {sys.argv} / {len(sys.argv)}")
        return

if __name__ == "__main__":
    # print("start program")
    start = Main()
    start.main()
    