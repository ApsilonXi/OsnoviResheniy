import numpy as np

def generate_matrix(num_tasks, num_processors, min_val, max_val):
    # Генерация случайной матрицы с заданным количеством задач и процессоров
    return np.random.randint(min_val, max_val + 1, size=(num_tasks, num_processors))

def schedule_with_arbitrary_load(matrix):
    # Шаг 1: Упорядочим строки матрицы по убыванию сумм всех элементов
    sorted_matrix = matrix[np.argsort(-matrix.sum(axis=1))]

    # Массив для хранения нагрузки на процессоры
    load = np.zeros(sorted_matrix.shape[1])

    # Шаг 2 и Шаг 3: Пробегаем по строкам и выбираем минимальный элемент
    for row in sorted_matrix:
        min_index = np.argmin(load + row)
        load[min_index] += row[min_index]

    # Возвращаем итоговую максимальную загрузку
    return load, np.max(load)

# Ввод данных
print("-------Lab 2----------")
num_tasks = int(input("M: "))
num_processors = int(input("N: "))
min_val = int(input("Min: "))
max_val = int(input("Max: "))

# Генерация матрицы
matrix = generate_matrix(num_tasks, num_processors, min_val, max_val)

# Выполнение алгоритма
load, max_load = schedule_with_arbitrary_load(matrix)

# Вывод результатов
print("Матрица задач:")
print(matrix)
print(f"\nНагрузка на процессоры: {load}")
print(f"Максимальная загрузка: {max_load}")
