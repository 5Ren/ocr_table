import tabula
import numpy as np

# PDFファイルのパス
pdf_file_path ='tets2.pdf'

# PDFファイルから表を抽出し、DataFrameのリストを取得
tables = tabula.read_pdf(pdf_file_path, pages='all', encoding='utf-8')

# 抽出された表をnumpy配列に変換
table_data = []
for table in tables:
    table_data.append(table.values)

# numpy配列を表示
for idx, data in enumerate(table_data):
    print(f'Table {idx + 1}:')
    print(data)

# あるいは、numpy配列を処理することができます
# たとえば、特定の行や列を取得することができます
# print(table_data[0][:, 0])  # 1つ目の表のすべての行の1列目を取得
