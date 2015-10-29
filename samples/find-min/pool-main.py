
import multiprocessing
import random

min = multiprocessing.Value('i', 999)

def findMin(x):
    print(multiprocessing.current_process().name, x)
    if x < min.value:
        min.value = x

items = random.sample(range(10, 100), 10)
print('->', items)

pool = multiprocessing.Pool(multiprocessing.cpu_count())
pool.map(findMin, items, chunksize=5)

print("global min is {}".format(min.value))
