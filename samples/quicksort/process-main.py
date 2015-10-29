import multiprocessing
import random


# http://stackoverflow.com/questions/28548414/python-quick-sort-parallel-sort-slower-than-sequential

class F(multiprocessing.Process):

    def __init__(self, items, wconn, depth=0):
        super(F, self).__init__()
        
        self.wconn = wconn
        self.items = items
        self.depth = depth

    def run(self):
        indent = '  ' * self.depth
        prefix = "{}{}:".format(indent, multiprocessing.current_process().name)
        print(prefix, "sorting {}".format(self.items))

        if len(self.items) <= 1:
            self.wconn.send([ self.items[0] ])
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
            t1_conn, wconn = multiprocessing.Pipe()
            t1 = F(less, wconn=wconn, depth=self.depth + 1)
            t1.start()

        sortedMore = []
        t2 = None
        if len(more) > 0:
            t2_conn, wconn = multiprocessing.Pipe()
            t2 = F(more, wconn=wconn, depth=self.depth + 1)
            t2.start()

        if t1 is not None:
            sortedLess = t1_conn.recv()
            t1.join()

        if t2 is not None:
            sortedMore = t2_conn.recv()
            t2.join()

        print(prefix, "sorted:", sortedLess, pivotList, sortedMore)

        self.wconn.send(sortedLess + pivotList + sortedMore)

sample = random.sample(range(100), 10)
print("->", sample)

rconn, wconn = multiprocessing.Pipe()
t = F(sample, wconn)
t.start()

x = rconn.recv()
print(x)

t.join()
