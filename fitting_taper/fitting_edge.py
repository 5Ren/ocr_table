import cv2
import numpy as np
import csv

# 画像を読み込む
image_path = r'C:\Users\YamaLab-38\PycharmProjects\ocr_table\fitting_taper\taper_sanple.jpeg'
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found or unable to open.")
    exit()
# オリジナル画像のコピーを作成
original_image = image.copy()

# グレースケール変換と二値化
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 輪郭を検出
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# マウス操作の初期化
drawing = False
ix, iy = -1, -1

# CSVファイルと画像の保存先を指定
csv_file = r'C:\Users\YamaLab-38\PycharmProjects\ocr_table\fitting_taper\contours.csv'
image_save_path = r'C:\Users\YamaLab-38\PycharmProjects\ocr_table\fitting_taper\result_image.jpeg'


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, image, contours

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            image = original_image.copy()
            cv2.rectangle(image, (ix, iy), (x, y), (255, 0, 0), 2)
            for contour in contours:
                cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(image, (ix, iy), (x, y), (255, 0, 0), 2)

        # 選択された領域内の輪郭を削除
        rect = (ix, iy, x, y)
        new_contours = []
        for contour in contours:
            inside = True
            for point in contour:
                px, py = point[0]
                if not (min(ix, x) <= px <= max(ix, x) and min(iy, y) <= py <= max(iy, y)):
                    inside = False
                    break
            if not inside:
                new_contours.append(contour)

        # 新しい輪郭リストに更新
        contours = new_contours
        image = original_image.copy()
        for contour in contours:
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)


# マウスイベントを設定
cv2.namedWindow('Contours')
cv2.setMouseCallback('Contours', draw_rectangle)

while True:
    cv2.imshow('Contours', image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # 'q'を押すと終了
        break

# 最終的に残った輪郭をCSVに保存
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    for contour_index, contour in enumerate(contours):
        writer.writerow([f"Contour {contour_index + 1}"])
        for point in contour:
            writer.writerow(point[0])
        writer.writerow([])  # 空行で区切る

# 最終画像を保存
cv2.imwrite(image_save_path, image)
print(f"Resulting image saved to {image_save_path}")
print(f"Contours saved to {csv_file}")

cv2.destroyAllWindows()