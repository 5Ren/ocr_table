import datetime

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# プロット初期設定
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 11
plt.rcParams['figure.figsize'] = (5, 3.5)


# はね飛び高さの近似計算
# Hw = -a (b^(-f2/f1)) + H0
# 損失正接，表面張力をばねと見立て， a, bの中に入れていく

# の関数に近似




color_list = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#7030A0']
sample_name = ['Water', 'CNF0.05wt%', '0.1wt%', '0.2wt%', '0.3wt%', '0.4wt%', 'Plasma']
surface_tension_list = [72, 70.9, 70.1, 67.2, 66.5, 54.5, 53.6]

marker_list = ['o', 'o', 'o', 'o', 'o', 'o', 'x']

# CSVファイルの読み込み
data = np.loadtxt('Book1 (1).csv', delimiter=',', encoding='utf-8_sig')

# 行数取得
row_numbers = len(data)

# データをxとyに分割
x = np.array(data[0, :])
y_data_list = np.array(data[1:, :])

for i in range(len(y_data_list)):
    print('=' * 40)
    print(f'Analyze {i + 1}')
    y = np.array(data[i + 1, :])

    # 新しいx軸の範囲を作成
    new_x = np.linspace(min(x), max(x), 100)  # 100個の等間隔なx値を生成

    surface_tension = surface_tension_list[i]
    seppen = y[-1]

    def nonlinear_fit(x, a, b):
        # return -a ** -x + y[-1] + 1
        return -a * ((b * surface_tension) ** -x - 1) + seppen

    # 最適なパラメータをフィット
    params, cov = curve_fit(nonlinear_fit, x, y)


    # R2求める
    residuals = y - nonlinear_fit(x, *params)
    rss = np.sum(residuals ** 2)
    tss = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (rss / tss)
    print(f'{r_squared=: .3f}')

    # プロット
    if marker_list[i] == 'o':
        plt.scatter(x, y,
                    # label=sample_name[i],
                    facecolor='None',
                    color=color_list[i],
                    marker=marker_list[i],
                    clip_on=False)
    elif marker_list[i] == 'x':
        plt.scatter(x, y,
                    # label=sample_name[i],
                    color=color_list[i],
                    marker=marker_list[i],
                    clip_on=False)

    # フィッティングされたパラメータを取得
    print(f'{params=}')
    a, b = params
    # 新しいx軸の範囲に対応するy値を予測
    fitted_y = nonlinear_fit(new_x, *params)
    # プロット
    plt.plot(new_x, fitted_y,
             label=f'fit: y =  {-a:.2f} * (({b: .3f} * γ)^-x - 1) + {y[-1]: .2f}, R2: {r_squared: .3f}',
             lw=1,
             color=color_list[i],
             clip_on=False,
             linestyle="dotted")

plt.xlabel(r'Groove width / tooth width ratio, $f_{2}$/ $f_{1}$')
plt.ylabel(r'$1^\mathrm{st}$ bounce height, ${H}_\mathrm{1st}$ (mm)')
plt.grid(False)
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.legend()
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
# plt.legend(loc='lower center', bbox_to_anchor=(.5, 1.1), ncol=4, borderaxespad=0)
now = datetime.datetime.now()
formatted_now = now.strftime('%y-%m-%d_%H%M%S')
plt.savefig(f'log/{formatted_now}.svg', bbox_inches='tight')
plt.show(bbox_inches='tight')
