from datetime import datetime
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import random

rcParams['font.family'] = 'Times New Roman', 'Arial', 'Tahoma'
rcParams['font.fantasy'] = 'Tahoma'

# Изменение параметров рисования (смена чёрного по белому на белое по чёрному)
# facecolor = 'k'

rcParams['figure.edgecolor'] = '#e8e1d4'
rcParams['figure.facecolor'] = '#e8e1d4'
rcParams['axes.facecolor'] = '#e8e1d4'
rcParams['axes.labelcolor'] = '#302e2b'
rcParams['grid.color'] = '#d8d1c3'
rcParams['xtick.color'] = '#615d56'
rcParams['ytick.color'] = '#615d56'

# Dataset
dates = [
    datetime(2022, 9, 2, 4),
    datetime(2022, 9, 3, 8),
    datetime(2022, 9, 4, 13),
    datetime(2022, 9, 5, 15),
    datetime(2022, 9, 6, 9),
    datetime(2022, 9, 7, 11),
    datetime(2022, 9, 8, 8),
    datetime(2022, 9, 9, 18)
]
dates_large = [
    datetime(2022, 9, 2, 4),
    datetime(2022, 9, 2, 6),
    datetime(2022, 9, 3, 8),
    datetime(2022, 9, 3, 9),
    datetime(2022, 9, 3, 10),
    datetime(2022, 9, 3, 11),
    datetime(2022, 9, 3, 12),
    datetime(2022, 9, 3, 13),
    datetime(2022, 9, 3, 14),
    datetime(2022, 9, 3, 15),
    datetime(2022, 9, 4, 13),
    datetime(2022, 9, 4, 17),
    datetime(2022, 9, 4, 19),
    datetime(2022, 9, 5, 15),
    datetime(2022, 9, 5, 18),
    datetime(2022, 9, 5, 21),
    datetime(2022, 9, 6, 9),
    datetime(2022, 9, 6, 13),
    datetime(2022, 9, 7, 11),
    datetime(2022, 9, 7, 12),
    datetime(2022, 9, 7, 16),
    datetime(2022, 9, 8, 8),
    datetime(2022, 9, 8, 11),
    datetime(2022, 9, 9, 18),
    datetime(2022, 9, 9, 19)
]
p_upper = []
w_temp = []
w_humidity = []
pulse = []

for i in range(len(dates)):
    p_upper.append(random.randint(84, 153))


for i in range(len(dates_large)):
    pulse.append(random.randint(62, 143))
    w_temp.append(random.randint(14, 27))
    w_humidity.append(random.randint(43, 78))

plt.figure(figsize=(9, 16), dpi=200)
plt.scatter(dates, p_upper, label=u'Давление (верхнее)')
plt.scatter(dates_large, pulse, label=u'Пульс')
plt.plot(dates_large, w_temp, label=u'Температура воздуха по цельсию')
plt.plot(dates_large, w_humidity, label=u'Влажность воздуха %')
plt.title("Зависимость давления от погодных условий", fontsize=17)
plt.xlabel(u'Дата', fontsize=17)
plt.ylabel(u'Показатели', fontsize=17)
plt.legend(fontsize=13)
plt.grid(True)

# for i in range(len(pulse)):
#     plt.annotate(
#         f'  {pulse[i]}', (dates_large[i],
#                           pulse[i] + 2),
#         fontsize=13)

# for i in range(len(p_upper)):
#     plt.annotate(f'  {p_upper[i]}', (dates_large[i], p_upper[i] + 2), fontsize=13)

# for i in range(len(w_temp)):
#     plt.annotate(f'  {w_temp[i]} °C', (dates_large[i], w_temp[i] + 2), fontsize=13)

# for i in range(len(w_humidity)):
#     plt.annotate(f'  {w_humidity[i]}%',
#                  (dates_large[i], w_humidity[i] + 2), fontsize=13)


def save_img(id: int, time_data: float) -> str:
    plot_name = f'{id}_{time_data}.png'
    plt.savefig(plot_name)
    return plot_name
