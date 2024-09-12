import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# CSVファイルから2Dデータ (x, z) の座標を読み込む
design_file_path = r"ideal_danmen_G'+D.csv"  # 自身のファイルパスに変更
scan_file_path = r"G'+D_xz_danmen.csv"  # 自身のファイルパスに変更

# CSVファイルを読み込み
design_data = pd.read_csv(design_file_path)
scan_data = pd.read_csv(scan_file_path)

# 2D点群データとしてx, zの座標を取得
design_points_2d = design_data[['x', 'z']].values
scan_points_2d = scan_data[['x', 'z']].values

# KDTreeで最近傍探索用のツリーを作成 (2D座標)
design_tree = KDTree(design_points_2d)

# スキャンデータの各点から設計データの最近傍距離を計算
distances, _ = design_tree.query(scan_points_2d)

# 差分をカラーマップで表示 (赤=大きい差分、青=小さい差分)
fig, ax = plt.subplots()
scatter = ax.scatter(scan_points_2d[:, 0], scan_points_2d[:, 1], c=distances, s=10, cmap='jet')
ax.set_title('Difference between Scanned and Design Data (2D)')
ax.set_xlabel('X coordinate')
ax.set_ylabel('Z coordinate')

# カラーバー（凡例）を追加
cbar = fig.colorbar(scatter, ax=ax)
cbar.set_label('Distance to nearest design point')

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

# 結果をpandasのDataFrameにして表示
df_result = pd.DataFrame([result])
print(df_result)
