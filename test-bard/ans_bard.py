import pdfplumber
import pytesseract


def extract_table(pdf):
    """
    PDFで用意された表を、2次元のリストに変換する関数

    Args:
    pdf: PDFファイルのオブジェクト

    Returns:
    2次元のリスト
    """

    # 表のテキストを抽出する
    text = pdf.pages[0].extract_text()

    # 表の境界を検出する
    boxes = pytesseract.image_to_boxes(text, config='--psm 7')

    # 表の行と列を取得する
    rows = []
    for box in boxes:
        if box.left < box.right and box.top < box.bottom:
            rows.append(box)

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
    pdf = pdfplumber.open('tets2.pdf')

    # 表の抽出
    cells = extract_table(pdf)

    # 表の表示
    for row in cells:
        print(row)
