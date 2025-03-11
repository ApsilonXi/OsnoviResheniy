from random import randint
import numpy as np
#N, M = 3, 7
#temp = np.array([[10, 19, 14], [15, 16, 18], [17, 12, 12], [10, 10, 11], [11, 11, 18], [13, 11, 18], [20, 15, 20]])
N, M = int(input("N = ")), int(input("M = "))
print("введите границы диапазона:")
z1, z2 = int(input("z1 = ")), int(input("z2 = "))
temp = np.array([[randint(z1, z2) for j in range(N)] for i in range(M)])
print(temp)
print(temp.tolist(), N, M)


rows_min = temp.min(axis=1)
BARRIER = int(np.ceil(rows_min.sum() / N))
print(rows_min, BARRIER)

load = [0 for _ in range(N)]
def method(load, row):
    load = np.array(load)
    newrow = load + row
    ind = newrow.argmin()
    elem = newrow[ind] 
    return (ind, elem)

for row in temp:
    ind = row.argmin()
    element = row[ind]
    if load[ind] + element > BARRIER:
        print('method 2')
        result = method(load, row)
        load[result[0]] = result[1]
    else:
        load[ind] += element
    print(load)
print(load, max(load))

