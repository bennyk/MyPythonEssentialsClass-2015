
import random
import multiprocessing



class FindMinTask(multiprocessing.Process):

    def __init__(self, items):
        super(multiprocessing.Process, self).__init__()
        self.items = items
        self.min = multiprocessing.Value('i', 999)

    def run(self):
        print(multiprocessing.current_process().name, 'process', self.items)
        for i in self.items:
            if i < self.min.value:
                self.min.value = i

    def join(self, timeout=None):
        super().join()
        return self.min

limit = 12
chunksize = 3

items = random.sample(range(10, 100), 10)
print('->', items)

pendingTasks = []
for start in range(0, limit, chunksize):
    to = start + chunksize
    if to < len(items):
        # print(start, items[start:to])
        chunks = items[start:to]
    else:
        # print(start, items[start:])
        chunks = items[start:]

    if len(chunks) > 0:
        task = FindMinTask(chunks)
        task.start()

        pendingTasks.append(task)

min = None
for t in pendingTasks:
    assert isinstance(t, FindMinTask)

    x = t.join()
    print('received', x.value)

    if min is None or x.value < min:
        min = x.value

print("global min is: {}".format(min))
