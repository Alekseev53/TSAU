import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Чтение данных из файлов
file_path_1 = 'NavSystemData_20231028_14h_59m_22s.txt'
file_path_2 = 'NavSystemData_20231028_15h_15m_22s.txt'
file_path_3 = 'NavSystemData_20231028_14h_53m_06s.txt'

data_1 = pd.read_csv(file_path_1, delim_whitespace=True, header=None)
data_2 = pd.read_csv(file_path_2, delim_whitespace=True, header=None)
data_3 = pd.read_csv(file_path_3, delim_whitespace=True, header=None)

# Истинные значения для сравнения
true_values = pd.Series([0, 0, 0, 0, 0, 9.8])

# Вычисление статического отклонения
def calculate_static(data, true_values):
    return ((data - true_values)).mean()

# Вычисление всех метрик статического отклонения
static_deviation_1 = calculate_static(data_1, true_values)
static_deviation_2 = calculate_static(data_2, true_values)
static_deviation_3 = calculate_static(data_3, true_values)
static_deviation_average = (static_deviation_1 + static_deviation_2 + static_deviation_3) / 3

# Функция для вычисления In Run Deviation с учетом истинных значений (до коррекции)
def calculate_in_run_banch(data, true_values):
    batches = np.array_split(data, 10)
    deviation_per_batch = [(batch - true_values).mean() for batch in batches]
    average_deviation = pd.concat(deviation_per_batch, axis=1).mean(axis=1)
    return average_deviation

# Функция для вычисления In Run Deviation с учетом истинных значений (до коррекции)
def calculate_in_run(data, true_values):
    batch = data[len(data)*9//10:]
    average_deviation = (batch - true_values).mean() 
    return average_deviation

# Функция для вычисления R to R Deviation с учетом истинных значений (до коррекции)
def calculate_r_to_r(data1, data2, data3, true_values):
    deviation_per_file = [(data1 - true_values).mean(), (data2 - true_values).mean(), (data3 - true_values).mean()]
    average_deviation = pd.concat(deviation_per_file, axis=1).mean(axis=1)
    return average_deviation

# Вычисление In Run и R to R Deviation для исходных данных
in_run_deviation_original = calculate_in_run(pd.concat([data_1, data_2, data_3]), true_values)
r_to_r_deviation_original = calculate_r_to_r(data_1, data_2, data_3, true_values)

# Создание таблицы с результатами до коррекции
result_table = pd.DataFrame({
    'Static': static_deviation_average,
    'In Run': in_run_deviation_original,
    'R to R': r_to_r_deviation_original
})

what_to_plot = range(5)

# Вычитание статических ошибок из данных
# Коррекция данных
data_1_corrected = data_1 - static_deviation_1
data_2_corrected = data_2 - static_deviation_2
data_3_corrected = data_3 - static_deviation_3

# Определение индексов столбцов для построения графиков
what_to_plot = range(5)#[5]#[0,1]#[2,3,4]#

# Создание субплотов
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

# Построение графика для data_1
data_2[what_to_plot].plot(ax=axes[0])
axes[0].set_title('Original Data')
axes[0].set_ylabel('Values')

# Построение графика для data_1_corrected
data_2_corrected[what_to_plot].plot(ax=axes[1])
axes[1].set_title('Corrected Data')
axes[1].set_ylabel('Values')

# Настройка отображения графиков
plt.tight_layout()
plt.show()

# Пересчет статического отклонения для скорректированных данных
static_deviation_1_corrected = calculate_static(data_1_corrected, true_values)
static_deviation_2_corrected = calculate_static(data_2_corrected, true_values)
static_deviation_3_corrected = calculate_static(data_3_corrected, true_values)
static_deviation_average_corrected = (static_deviation_1_corrected + static_deviation_2_corrected + static_deviation_3_corrected) / 3

# Вычисление In Run и R to R Deviation для скорректированных данных
in_run_deviation_corrected = calculate_in_run(pd.concat([data_1_corrected, data_2_corrected, data_3_corrected]), true_values)
r_to_r_deviation_corrected = calculate_r_to_r(data_1_corrected, data_2_corrected, data_3_corrected, true_values)

# Создание таблицы с результатами после коррекции
result_table_corrected = pd.DataFrame({
    'Static Corrected': static_deviation_average_corrected,
    'In Run Corrected': in_run_deviation_corrected,
    'R to R Corrected': r_to_r_deviation_corrected
})



result_div = pd.DataFrame({
    'Static div':result_table_corrected['Static Corrected']/result_table['Static'],
    'In Run div':result_table_corrected['In Run Corrected']/result_table['In Run'],
    'R to R div':result_table_corrected['R to R Corrected']/result_table['R to R'],
})

result_div_m1 = pd.DataFrame({
    'Static div': abs(result_table['Static'] / result_table_corrected['Static Corrected']),
    'In Run div': abs(result_table['In Run'] / result_table_corrected['In Run Corrected']),
    'R to R div': abs(result_table['R to R'] / result_table_corrected['R to R Corrected']),
})

pd.set_option('display.float_format', '{:.20f}'.format)

print(result_table)
print(result_table_corrected)
print(result_div)


pd.set_option('display.float_format', '{:.0f}'.format)
print("Во сколько раз стало лучше")
print(result_div_m1)