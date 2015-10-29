
import threading
import random

class F(threading.Thread):
    def __init__(self, items, depth=0):
        super().__init__()
        self.items = items
        self.result = None
        self.depth = depth
        self.verbose = True

    def run(self):
        indent = '  ' * self.depth
        prefix = "{}{}:".format(indent, threading.current_thread().name)
        print(prefix, "sorting {}".format(self.items))

        if len(self.items) <= 1:
            self.result = [ self.items[0] ]
            return

        pivot = self.items[0]
        less = []
        pivotList = []
        more = []
        for x in self.items:
            if x < pivot:
                less.append(x)
            elif x > pivot:
                more.append(x)
            else:
                pivotList.append(x)

        print(prefix, "less", less)
        print(prefix, "pivot", pivotList)
        print(prefix, "more", more)

        # sometime we have a worst case pivot

        sortedLess = []
        t1 = None
        if len(less) > 0:
            t1 = F(less, depth=self.depth + 1)
            t1.start()

        sortedMore = []
        t2 = None
        if len(more) > 0:
            t2 = F(more, depth=self.depth + 1)
            t2.start()

        if t1 is not None:
            sortedLess = t1.join()

        if t2 is not None:
            sortedMore = t2.join()

        print(prefix, "sorted:", sortedLess, pivotList, sortedMore)

        self.result = sortedLess + pivotList + sortedMore

    def join(self, timeout=None):
        super().join(timeout)
        return self.result


sample = random.sample(range(100), 10)
print("->", sample)

t = F(sample)
t.start()
x = t.join()
print(x)
