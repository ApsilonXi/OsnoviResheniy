import numpy as np

def calculate_barriers(matrix):
    """Рассчитываем барьеры для каждой строки."""
    min_barrier = []
    max_barrier = []

    for row in matrix:
        min_val = min(row)  # Нахождение минимального значения в строке
        max_val = max(row)  # Нахождение максимального значения в строке
        min_barrier.append((min_val // len(row)) + 1)  # Округляем вверх
        max_barrier.append((max_val // len(row)) + 1)  # Округляем вверх

    return min_barrier, max_barrier

def minimal_elements_selection(matrix):
    """Выбор минимальных элементов из каждой строки."""
    selected_elements = []

    for row in matrix:
        selected_elements.append(min(row))  # Нахождение минимального значения в строке

    return selected_elements

def apply_barriers(matrix, min_barrier, max_barrier):
    """Применение барьеров к матрице."""
    result = []

    for i, row in enumerate(matrix):
        new_row = []
        for value in row:
            if value < min_barrier[i]:
                new_row.append(min_barrier[i])  # Применяем нижний барьер
            elif value > max_barrier[i]:
                new_row.append(max_barrier[i])  # Применяем верхний барьер
            else:
                new_row.append(value)  # Значение в пределах барьеров
        result.append(new_row)

    return result

def plotnikov_zverev_algorithm(matrix):
    """Применение алгоритма Плотникова-Зверева."""
    num_rows = len(matrix)
    selected_rows = [False] * num_rows  # Список для отслеживания выбранных строк
    assigned_resources = [0] * num_rows   # Список для отслеживания распределенных ресурсов

    for step in range(num_rows):
        # Находим минимальные элементы, которые еще не были выбраны
        remaining_elements = [row for index, row in enumerate(matrix) if not selected_rows[index]]
        if not remaining_elements:
            break  # Если все строки выбраны, выходим из цикла

        # Выбор минимального элемента из оставшихся строк
        min_element = float('inf')
        min_row_index = -1

        for i, row in enumerate(remaining_elements):
            current_min = min(row)
            if current_min < min_element:
                min_element = current_min
                min_row_index = i + sum(selected_rows[:i])  # Коррекция индекса

        if min_row_index != -1:
            selected_rows[min_row_index] = True  # Отмечаем строку как выбранную
            assigned_resources[min_row_index] += min_element  # Распределяем ресурсы

    return assigned_resources

def main():
    num_tasks = int(input("M: "))  # количество заданий
    processors = int(input("N: ")) # количество процессоров
    rand_min = int(input("Min: "))
    rand_max = int(input("Max: "))
    '''num_massives = int(input("Кол-во массивов: ")) # количество списков тасков'''
    num_massives = 10

    all_schedule = []
    all_schedule_asc = []
    all_schedule_desc = []

    schedule_rand = 0
    schedule_asc = 0
    schedule_desc = 0
    
    for i in range(num_massives):
        tasks = np.random.randint(rand_min, rand_max, (num_tasks, processors)).tolist()
        for i in tasks:
            i.append(sum(i))
        tasks_asc = sorted(tasks)
        task_desc = sorted(tasks, reverse=True)

        min_barrier, max_barrier = calculate_barriers(tasks)
        print("Минимальные барьеры:", min_barrier)
        print("Максимальные барьеры:", max_barrier)
            
        modified_matrix = apply_barriers(tasks, min_barrier, max_barrier)
        print("Матрица после применения барьеров:")
        print(modified_matrix)

        result = plotnikov_zverev_algorithm(modified_matrix)
        print("Результат алгоритма Плотникова-Зверева:")
        print(result)

if __name__ == "__main__":
    main()