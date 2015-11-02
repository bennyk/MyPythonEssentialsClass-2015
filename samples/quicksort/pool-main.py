
import multiprocessing
import random

workId = 0

class Work:
    def __init__(self, part, startIndex, debug=False, depth=0):
        global workId
        self.startIndex = startIndex
        self.part = part
        self.pivot = None
        self.works = []

        # for debugging only
        self.debug = debug
        self.depth = depth
        self.prefix = "   " * self.depth

    def startPartitioning(self):
        if self.debug:
            print("{}{}: start partitioning list: {}".format(self.prefix, multiprocessing.current_process().name, self.part))

        pivot = self.part[0]
        lessPart = []
        morePart = []
        for x in self.part:
            if x < pivot:
                lessPart.append(x)
            elif x > pivot:
                morePart.append(x)
            else:
                pass

        if len(lessPart) > 0:
            w = Work(lessPart, self.startIndex, debug=self.debug, depth=self.depth + 1)
            self.works.append(w)

        if len(morePart) > 0:
            w = Work(morePart, self.startIndex + len(lessPart) + 1, debug=self.debug, depth=self.depth + 1)
            self.works.append(w)

        self.pivot = (pivot, self.startIndex + len(lessPart))

    def __str__(self):
        s = "{}startIndex {} pivot {} works [".format(self.prefix, self.startIndex, self.pivot)
        for w in self.works:
            assert isinstance(w, Work)
            s += "{"
            s += "startIndex {} part {}".format(w.startIndex, w.part)
            s += "}"
            if w is not self.works[-1]:
                s += ", "

        s += "]"
        return s

def f(w):
    assert isinstance(w, Work)
    w.startPartitioning()
    return w

def qsort(items, debug=False):

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    w = Work(items, 0, debug=debug)
    pendingWorks = [w]

    result = [-1] * len(items)
    while len(pendingWorks) > 0:
        worksDone = pool.map(f, pendingWorks, chunksize=5)
        pendingWorks.clear()

        for w in worksDone:
            assert isinstance(w, Work)

            if debug:
                print(w)

            value, index = w.pivot
            result[index] = value

            # Alternatively we can also choose to optimize away trivial works with single item.
            pendingWorks.extend(w.works)

    return result

sample = random.sample(range(100), 10)
print("->", sample)

print("sorted list:", qsort(sample, debug=True))
