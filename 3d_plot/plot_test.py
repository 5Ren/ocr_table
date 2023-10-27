import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

data = np.loadtxt('all_H2.csv', delimiter=',', encoding='utf-8_sig')

# データの用意
x = data[0]  # x軸のデータ
y = data[1]  # y軸のデータ
z = data[2]  # z軸のデータ

# 3Dグラフの作成
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# データのプロット
ax.scatter(x, y, z, c='r', marker='o')  # データ点をプロット

# 軸ラベルの設定
ax.set_xlabel('Taper degree, $\phi$ ($^\circ$)')
ax.set_ylabel('Groove width / tooth width ratio, $f_2/f_1$')
ax.set_zlabel('Bouncing height, $H_1st$ (mm)')

# x、y、z軸の範囲を指定
ax.set_xlim(0, 120)  # x軸の範囲
ax.set_ylim(0, 10)  # y軸の範囲
ax.set_zlim(0, 12)  # z軸の範囲

# グラフの表示
plt.show()

# グラフをSVGファイルとして保存
plt.savefig('3d_plot.svg', format='svg', bbox_inches='tight')
