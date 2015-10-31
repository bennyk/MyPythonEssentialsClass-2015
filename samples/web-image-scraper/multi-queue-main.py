"""
Demonstrate the use of multiprocessing.Queue to manage a list of URL downloading task. A list of workers are
pre-spawned to handle the downloading workload independently.
"""
import multiprocessing
from helpers import *

class MyDownloadWorker(multiprocessing.Process):
    def  __init__(self, q):
        super(multiprocessing.Process, self).__init__()

        assert isinstance(q, multiprocessing.queues.Queue)
        self.q = q

    def run(self):
        name = multiprocessing.current_process().name
        print(bcolors.OKGREEN, name, "started.", bcolors.ENDC)
        while True:
            link = self.q.get()
            if link is None:
                print(bcolors.WARNING, name, "terminated.", bcolors.ENDC)
                break
            print(name, "received", link)

            try:
                startDownloadingFile(link)
            except OSError as e:
                print(bcolors.FAIL, e, bcolors.ENDC)

number_of_workers = multiprocessing.cpu_count()
def spawn_workers(q, n = number_of_workers):
    print("spawning %d workers" % n)
    workers = []
    for i in range(n):
        worker = MyDownloadWorker(q)
        worker.start()
        workers.append(worker)
    return workers

q = multiprocessing.JoinableQueue()
workers = spawn_workers(q)
for link in find_image_src():
    q.put(link)

for i in range(number_of_workers):
    q.put(None)

q.close()
q.join_thread()

print("waiting for workers to finish")
for w in workers:
    isinstance(w, multiprocessing.Process)
    w.join()

print("completed.")
