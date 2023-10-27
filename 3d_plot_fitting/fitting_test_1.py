import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

data = np.loadtxt('all_H2.csv', delimiter=',', encoding='utf-8_sig')

# データの用意
x = data[0]  # x軸のデータ
y = data[1]  # y軸のデータ
z = data[2]  # z軸のデータ

# データ点のプロット
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r', marker='o', label='生データ')

# 近似曲面を描画
x_range = np.linspace(min(x), max(x), 50)
y_range = np.linspace(min(y), max(y), 50)
X, Y = np.meshgrid(x_range, y_range)

# 3Dデータの近似
Z = griddata((x, y), z, (X, Y), method='cubic')

ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, label='近似曲面')

# 軸ラベルの設定
ax.set_xlabel('X軸')
ax.set_ylabel('Y軸')
ax.set_zlabel('Z軸')

# グラフの表示
plt.legend()
plt.show()
