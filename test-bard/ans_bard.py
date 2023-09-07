import pdfplumber
import pytesseract

def extract_table(pdf):
    """
    手書きの日本語の表を二次元のリストに起こす関数

    Args:
    pdf: PDFファイルのオブジェクト

    Returns:
    二次元のリスト
    """

    # 表の境界を検出する
    page = pdf.pages[0]
    boxes = pytesseract.image_to_boxes(page.image, config='--psm 7')

    # 表の行と列を取得する
    rows = []
    for box in boxes:
    rd(box)

    cols = [box.left for box in rows]
    cols = list(set(cols))
    cols.sort()

    # 表の各セルのテキストを取得する
    cells = []
    for row in rows:
    cell = []
    for col in cols:
      cell.append(row.text[row.left <= col < row.right])
    cells.append(cell)

    return cells


if __name__ == '__main__':
    # PDFファイルの読み込み
    pdf = pdfplumber.open('example.pdf')

    # 表の抽出
    cells = extract_table(pdf)

    # 表の表示
    for row in cells:
    print(row)