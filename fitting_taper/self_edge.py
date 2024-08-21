import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import csv

# 変換係数
conversion_factor = 643.01 / 1024  # ピクセルからμmへの変換係数

# Load the image using OpenCV
image = cv2.imread(r'C:\Users\YamaLab-38\PycharmProjects\ocr_table\fitting_taper\taper_sanple.jpeg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for matplotlib

# `clone` を定義して、画像のコピーを作成
clone = image.copy()
height, width = image.shape[:2]  # 画像の縦幅と横幅を取得

# グローバル変数
elements = []  # 各要素を保存するリスト
current_element = []
mode = 'line'  # 初期モードは通常の線描画モード
element_id = 1  # 要素のIDを管理する
average_pitch = None  # 平均ピッチを保存する

def calculate_length(points):
    total_distance = 0
    for i in range(1, len(points)):
        total_distance += math.sqrt((points[i][0] - points[i - 1][0]) ** 2 + (points[i][1] - points[i - 1][1]) ** 2)
    return total_distance

def transform_coordinates(points):
    # y座標を変換して直交座標系に合わせ、ピクセルをμmに変換
    return [(x * conversion_factor, (height - y) * conversion_factor) for x, y in points]

def click_event(event, x, y, flags, param):
    global current_element, clone, mode, average_pitch

    if event == cv2.EVENT_LBUTTONDOWN:
        if mode == 'line':
            current_element.append((x, y))
            cv2.circle(clone, (x, y), 5, (0, 0, 255), -1)  # 点を描画
            if len(current_element) > 1:
                cv2.line(clone, current_element[-2], current_element[-1], (255, 0, 0), 2)  # 線を描画
            cv2.imshow("Image", clone)

        elif mode == 'arc':
            current_element.append((x, y))
            cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)  # 緑色の点を描画
            if len(current_element) == 3:
                draw_arc(current_element[0], current_element[1], current_element[2])
                if average_pitch is not None:
                    interpolated_points = interpolate_arc_points(current_element[0], current_element[1],
                                                                 current_element[2], average_pitch)
                    elements.append(('arc', interpolated_points))  # 補間された円弧の点を保存
                current_element = []  # 次の円弧のためにリセット
            cv2.imshow("Image", clone)

def draw_arc(start, end, intermediate):
    global clone
    center, radius = find_circle_center_radius(start, end, intermediate)
    angle1 = math.degrees(math.atan2(start[1] - center[1], start[0] - center[0]))
    angle2 = math.degrees(math.atan2(end[1] - center[1], end[0] - center[0]))
    angle_intermediate = math.degrees(math.atan2(intermediate[1] - center[1], intermediate[0] - center[0]))

    if angle1 < angle_intermediate < angle2 or angle2 < angle_intermediate < angle1:
        cv2.ellipse(clone, center, (radius, radius), 0, angle1, angle2, (0, 255, 255), 2)
    else:
        cv2.ellipse(clone, center, (radius, radius), 0, angle2, angle1, (0, 255, 255), 2)

def interpolate_arc_points(start, end, intermediate, pitch):
    center, radius = find_circle_center_radius(start, end, intermediate)

    angle1 = math.atan2(start[1] - center[1], start[0] - center[0])
    angle2 = math.atan2(end[1] - center[1], end[0] - center[0])

    if angle1 > angle2:
        angle1, angle2 = angle2, angle1

    arc_length = abs(angle2 - angle1) * radius
    num_points = int(math.ceil(arc_length / pitch))
    interpolated_points = []

    for i in range(num_points + 1):
        theta = angle1 + (angle2 - angle1) * i / num_points
        x = int(center[0] + radius * math.cos(theta))
        y = int(center[1] + radius * math.sin(theta))
        interpolated_points.append((x, y))
        cv2.circle(clone, (x, y), 3, (255, 0, 0), -1)  # 補完された点をプロット

    return interpolated_points

def find_circle_center_radius(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    mid_ab = ((ax + bx) / 2, (ay + by) / 2)
    mid_bc = ((bx + cx) / 2, (by + cy) / 2)

    slope_ab = -(bx - ax) / (by - ay + 1e-10)
    slope_bc = -(cx - bx) / (cy - by + 1e-10)

    center_x = (mid_bc[1] - mid_ab[1] + slope_ab * mid_ab[0] - slope_bc * mid_bc[0]) / (slope_ab - slope_bc)
    center_y = mid_ab[1] + slope_ab * (center_x - mid_ab[0])

    radius = int(math.sqrt((ax - center_x) ** 2 + (ay - center_y) ** 2))

    return (int(center_x), int(center_y)), radius

def reset_current_element():
    global current_element, clone
    if current_element:
        current_element.pop()
        clone = image.copy()
        redraw_points_and_lines()
        cv2.imshow("Image", clone)

def redraw_points_and_lines():
    for element in elements:
        if element[0] == 'line':
            for i in range(1, len(element[1])):
                cv2.circle(clone, element[1][i - 1], 5, (0, 0, 255), -1)
                cv2.line(clone, element[1][i - 1], element[1][i], (255, 0, 0), 2)
        elif element[0] == 'arc':
            for pt in element[1]:
                cv2.circle(clone, pt, 3, (255, 0, 0), -1)

def save_elements_to_csv(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Element_ID", "Type", "Point_X (μm)", "Point_Y (μm)"])

        for element_id, element in enumerate(elements, start=1):
            transformed_points = transform_coordinates(element[1])
            if element[0] == 'line':
                for point in transformed_points:
                    writer.writerow([element_id, "Line", point[0], point[1]])
            elif element[0] == 'arc':
                for point in transformed_points:
                    writer.writerow([element_id, "Arc", point[0], point[1]])

def plot_traced_elements(elements):
    fig, ax = plt.subplots()

    for element_id, element in enumerate(elements, start=1):
        transformed_points = transform_coordinates(element[1])
        xs = [pt[0] for pt in transformed_points]
        ys = [pt[1] for pt in transformed_points]
        if element[0] == "line":
            ax.scatter(xs, ys, c='blue', label=f'Line {element_id}' if element_id == 1 else "")
        elif element[0] == "arc":
            ax.scatter(xs, ys, c='red', label=f'Arc {element_id}' if element_id == 1 else "")

    ax.set_aspect('equal')
    plt.xlabel('X (μm)')
    plt.ylabel('Y (μm)')
    plt.title('Traced Elements in μm')
    plt.legend()
    plt.grid(True)
    plt.show()

cv2.imshow("Image", clone)
cv2.setMouseCallback("Image", click_event)

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('m'):  # 'm'キーでモードを切り替え
        if mode == 'line':
            mode = 'arc'
            print("モード：円弧描画")
        else:
            mode = 'line'
            print("モード：線描画")
    elif key == 13:  # Enterキーで現在の要素のトレースを終了
        if current_element:
            if mode == 'line' and len(current_element) > 1:
                total_length = calculate_length(current_element)
                average_pitch = total_length / (len(current_element) - 1)
            elements.append((mode, current_element.copy()))  # 現在の要素を保存
            current_element = []
    elif key == 8:  # Backspaceキーで最後の点を取り消し
        reset_current_element()
    elif key == 27:  # Escキーで終了
        break

# 要素をCSVに保存
save_elements_to_csv("C:/Users/YamaLab-38/PycharmProjects/ocr_table/traced_elements_um.csv")

# Matplotlibで散布図をプロット
plot_traced_elements(elements)

cv2.destroyAllWindows()
