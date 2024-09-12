import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# CSVファイルから設計データとスキャンデータを読み込む
design_file_path = 'design_points.csv'  # 自身の環境に応じてパスを変更
scan_file_path = 'scan_points.csv'  # 自身の環境に応じてパスを変更

# CSVファイルを読み込み
design_data = pd.read_csv(design_file_path)
scan_data = pd.read_csv(scan_file_path)

# 点群データとしてx, y, zの座標を取得
design_points = design_data[['x', 'y', 'z']].values
scan_points = scan_data[['x', 'y', 'z']].values

# KDTreeで最近傍探索用のツリーを作成
design_tree = KDTree(design_points)

# スキャンデータの各点から設計データの最近傍距離を計算
distances, _ = design_tree.query(scan_points)

# 差分をカラーマップで表示 (赤=大きい差分、青=小さい差分)
colors = plt.cm.jet((distances - distances.min()) / (distances.max() - distances.min()))

# 3Dプロットで点群を表示
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(scan_points[:, 0], scan_points[:, 1], scan_points[:, 2], c=colors, s=1)
ax.set_title('Difference between Scanned and Design Data')
plt.show()

# 一致度の定量化
mean_difference = np.mean(distances)
max_difference = np.max(distances)
min_difference = np.min(distances)

# 許容範囲内の点の割合を計算
tolerance = 0.01  # 例: 10μm
in_tolerance = np.sum(distances < tolerance) / len(distances) * 100

# 結果を表示
result = {
    "Mean difference": mean_difference,
    "Max difference": max_difference,
    "Min difference": min_difference,
    "Percentage within tolerance": in_tolerance
}

print(result)
