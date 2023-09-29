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
# Hw = -a ((b * γ)^(-f2/f1)) + H0
# の関数に近似




color_list = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#7030A0']
sample_name = ['Water', 'CNF0.05wt%', '0.1wt%', '0.2wt%', '0.3wt%', '0.4wt%', 'Plasma']
surface_tension_list = [72, 70.9, 70.1, 67.2, 66.5, 54.5, 53.6]
marker_list = ['o', 'o', 'o', 'o', 'o', 'o', 'x']
tan_delta_list = [0, 1.584, 2.647, 5.459, 2.649, 1.499, 4.77]

# CSVファイルの読み込み
data = np.loadtxt('Book1 (1).csv', delimiter=',', encoding='utf-8_sig')

# 行数取得
row_numbers = len(data)

# データをxとyに分割
x = np.array(data[0, :])
print(f'{x=}')

# 最適なパラメータをフィット


for i in range(row_numbers - 1):
    print('=' * 40)
    print(f'Analyze {i + 1}')
    current_y_data = np.array(data[i + 1, :])

    # 新しいx軸の範囲を作成
    new_x = np.linspace(min(x), max(x), 100)  # 100個の等間隔なx値を生成

    surface_tension = surface_tension_list[i]
    seppen = current_y_data[-1]
    tan_delta = tan_delta_list[i]

    def nonlinear_fit(x, a, b):
        # return -a ** -x + y[-1] + 1
        return -(a / (surface_tension*-1)) * ((b * surface_tension) ** -x - 1) + seppen


    # 最適なパラメータをフィット
    params, cov = curve_fit(nonlinear_fit, x, current_y_data, maxfev=20000)


    # R2求める
    residuals = current_y_data - nonlinear_fit(x, *params)
    rss = np.sum(residuals ** 2)
    tss = np.sum((current_y_data - np.mean(current_y_data)) ** 2)
    r_squared = 1 - (rss / tss)
    print(f'{r_squared=: .3f}')

    # 新しいx軸の範囲に対応するy値を予測
    new_y = nonlinear_fit(new_x, *params)

    # プロット
    if marker_list[i] == 'o':
        plt.scatter(x, current_y_data,
                    # label=sample_name[i],
                    facecolor='None',
                    color=color_list[i],
                    marker=marker_list[i],
                    clip_on=False)
    elif marker_list[i] == 'x':
        plt.scatter(x, current_y_data,
                    # label=sample_name[i],
                    color=color_list[i],
                    marker=marker_list[i],
                    clip_on=False)

    print(f'{params=}')
    # フィッティングされたパラメータを取得
    a, b = params

    plt.plot(new_x, new_y,
             label=f'fit: y =  -({a * 100: .2f} / -(surface_tension * 100)) * (({b * 100: .3f} * γ / 100)^-x - 1) + {current_y_data[-1]: .2f}, R2: {r_squared: .3f}',
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
