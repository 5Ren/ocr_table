import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# CSVファイルの読み込み
data = np.loadtxt('Book1.csv', delimiter=',', encoding='utf-8_sig')

# データをxとyに分割
x = np.array(data[0, :])
print(f'{x=}')
y = np.array(data[1, :])
print(f'{y=}')


def nonlinear_fit(x, a, b, c):
    return b * x ** a + c


# 最適なパラメータをフィット
param, cov = curve_fit(nonlinear_fit, x, y)

# フィッティングされたパラメータを取得
a, b, c = param

# プロット
plt.scatter(x, y, label='data')
plt.plot(x, nonlinear_fit(x, a, b, c), 'r-', label=f'fit: y = {b:.2f} x ^ {a:.2f} + {c:.2f}))')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()
