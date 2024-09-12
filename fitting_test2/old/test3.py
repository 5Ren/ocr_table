import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class PlotSettings:
    def __init__(self):
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams["figure.dpi"] = 300
        plt.rcParams["font.size"] = 11
        plt.rcParams['figure.figsize'] = (5, 3.5)


class DataAnalysis:
    def __init__(self, data, surface_tension_list):
        self.data = data
        self.surface_tension_list = surface_tension_list

    def nonlinear_fit(self, x, a, b):
        seppen = self.current_y_data[-1]
        return -a * ((b * self.surface_tension) ** -x - 1) + seppen

    def analyze(self):
        x = np.array(self.data[0, :])
        row_numbers = len(self.data)

        for i in range(row_numbers - 1):
            print('=' * 40)
            print(f'Analyze {i + 1}')
            self.current_y_data = np.array(self.data[i + 1, :])
            new_x = np.linspace(min(x), max(x), 100)
            self.surface_tension = self.surface_tension_list[i]
            params, cov = curve_fit(self.nonlinear_fit, x, self.current_y_data)
            residuals = self.current_y_data - self.nonlinear_fit(x, *params)
            rss = np.sum(residuals ** 2)
            tss = np.sum((self.current_y_data - np.mean(self.current_y_data)) ** 2)
            r_squared = 1 - (rss / tss)
            print(f'{r_squared=: .3f}')
            new_y = self.nonlinear_fit(new_x, *params)
            return new_x, new_y, params, r_squared


class PlotData:
    def __init__(self, color_list, marker_list):
        self.color_list = color_list
        self.marker_list = marker_list

    def plot(self, x, y, params, r_squared):
        for i in range(len(y)):
            if self.marker_list[i] == 'o':
                plt.scatter(x[i], y[i],
                            facecolor='None',
                            color=self.color_list[i],
                            marker=self.marker_list[i],
                            clip_on=False)
            elif self.marker_list[i] == 'x':
                plt.scatter(x[i], y[i],
                            color=self.color_list[i],
                            marker=self.marker_list[i],
                            clip_on=False)

            a, b = params[i]
            plt.plot(x[i], y[i],
                     label=f'fit: y =  {-a:.2f} * (({b: .3f} * γ)^-x - 1) + {y[-1]: .2f}, R2: {r_squared: .3f}',
                     lw=1,
                     color=self.color_list[i],
                     clip_on=False,
                     linestyle="dotted")


def main():
    PlotSettings()
    data = np.loadtxt('Book1 (1).csv', delimiter=',', encoding='utf-8_sig')
    surface_tension_list = [72, 70.9, 70.1, 67.2, 66.5, 54.5, 53.6]
    analysis = DataAnalysis(data, surface_tension_list)
    x_new, y_new, params_new, r_squared_new = analysis.analyze()

    color_list = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#7030A0']
    marker_list = ['o', 'o', 'o', 'o', 'o', 'o', 'x']
    plotter = PlotData(color_list=color_list,
                       marker_list=marker_list)

    plotter.plot(x_new,
                 y_new,
                 params_new,
                 r_squared_new)


if __name__ == "__main__":
    main()
