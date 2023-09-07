import pdfplumber
import csv

# スキャンしたPDFファイルのパス
pdf_file_path = 'Sample_table.pdf'

# 出力CSVファイルのパス
csv_file_path = 'output.csv'

# PDFファイルを開く
with pdfplumber.open(pdf_file_path) as pdf:
    # CSVファイルを書き込みモードで開く
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # ページごとにテキストを抽出
        for page in pdf.pages:
            text = page.extract_text()

            # ページのテキストを行ごとに分割
            lines = text.split('\n')

            # 各行をCSVファイルに書き込む
            for line in lines:
                csv_writer.writerow([line])

print(f'PDFからテキストをCSVファイルに変換しました: {csv_file_path}')
