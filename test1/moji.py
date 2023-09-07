from PIL import Image
import pyocr

# pyocr.tesseract.TESSERACT_CMD = r'C:\Users\cocac\PycharmProjects\ocr_table\venv\Lib\site-packages\pyocr\tesseract.py'

# OCR Engine 取得
engines = pyocr.get_available_tools()
print(engines)
engines = engines[0]
print(engines)

# 画像読み込み
txt = engines.image_to_string(Image.open('moji_en.png'), lang='eng')
# print(txt)
