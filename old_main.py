# Импорт библиотеки pandas и numpy
import pandas as pd
import numpy as np

# Чтение данных из файлов
file_path_1 = 'NavSystemData_20231028_14h_59m_22s.txt'
file_path_2 = 'NavSystemData_20231028_15h_15m_22s.txt'
file_path_3 = 'NavSystemData_20231028_14h_53m_06s.txt'

data_1 = pd.read_csv(file_path_1, delim_whitespace=True, header=None)
data_2 = pd.read_csv(file_path_2, delim_whitespace=True, header=None)
data_3 = pd.read_csv(file_path_3, delim_whitespace=True, header=None)

# Истинные значения для сравнения
true_values = pd.Series([0, 0, 0, 0, 0, 9.8])

# Функция для вычисления статического отклонения
def calculate_static_deviation(data, true_values):
    return ((data - true_values)**2).mean()

# Вычисление всех метрик
static_deviation_1 = calculate_static_deviation(data_1, true_values)
static_deviation_2 = calculate_static_deviation(data_2, true_values)
static_deviation_3 = calculate_static_deviation(data_3, true_values)
static_deviation_average = (static_deviation_1 + static_deviation_2 + static_deviation_3) / 3


# Функция для вычисления In Run Deviation с учетом истинных значений
def calculate_in_run_deviation(data, true_values):
    batches = np.array_split(data, 10)
    deviation_per_batch = [(batch - true_values).std() for batch in batches]
    average_deviation = pd.concat(deviation_per_batch, axis=1).mean(axis=1)
    return average_deviation

# Функция для вычисления R to R Deviation с учетом истинных значений
def calculate_r_to_r_deviation(data1, data2, data3, true_values):
    deviation_per_file = [(data1 - true_values).std(), (data2 - true_values).std(), (data3 - true_values).std()]
    average_deviation = pd.concat(deviation_per_file, axis=1).mean(axis=1)
    return average_deviation

# Вычисление In Run и R to R Deviation для каждого из шести показателей
in_run_deviation = calculate_in_run_deviation(pd.concat([data_1, data_2, data_3]), true_values)
r_to_r_deviation = calculate_r_to_r_deviation(data_1, data_2, data_3, true_values)

# Создание таблицы с результатами
result_table = pd.DataFrame({
    'Static': static_deviation_average,
    'In Run': in_run_deviation,
    'R to R': r_to_r_deviation
})

print(result_table)