##フィッティングに使うもの
from scipy.optimize import curve_fit
import numpy as np

## 図示のために使うもの
import matplotlib.pyplot as plt

data = np.loadtxt('Book1.csv', delimiter=',', encoding='utf-8_sig')

x_data = data[:, 0]
y_data = data[:, 1]


print(x_data)
print(y_data)
plt.plot(x=x_data, y=y_data)
plt.show()


def nonlinear_fit(x, a, b):
    return b * np.exp(x / (a + x))


param, cov = curve_fit(nonlinear_fit, x_data, y_data)

# ## フィッティングしたい関数式を関数として定義してやる
# def linear_fit(x, a, b):
#     return a*x + b
#
# params, cov = curve_fit(linear_fit, array_x, array_y)
