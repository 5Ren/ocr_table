from pdf2image import convert_from_path
import pytesseract


# PDFからテキストを抽出する関数を定義
def ocr_from_pdf(file_path):
    # convert_from_path関数を使ってPDFファイルを画像に変換
    images = convert_from_path(file_path)

    # 抽出したテキストを保存するための空の文字列を作成
    text = ''

    # 画像リストの各画像について
    for i in range(len(images)):
        # pytesseractのimage_to_string関数を使って画像からテキストを抽出し、
        # text変数に追加。langパラメータに'jpn'を指定して日本語のテキストを認識
        text += pytesseract.image_to_string(images[i], lang='jpn')

    # 全ての画像から抽出したテキストを返す
    return text

# 対象となるPDFファイルのパスを指定
file_path = 'test.pdf'

# ocr_from_pdf関数を使ってPDFからテキストを抽出
text = ocr_from_pdf(file_path)

# 抽出したテキストを表示
print(text)
