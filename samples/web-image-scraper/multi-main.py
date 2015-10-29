
import multiprocessing

from helpers import *

class MyDownloadTask(multiprocessing.Process):
    def __init__(self, url):
        super(multiprocessing.Process, self).__init__()
        self.url = url

    def __str__(self):
        return "MyDownloadTask({})".format(self.url)

    def run(self):
        try:
            startDownloadingFile(self.url)
            print(bcolors.OKGREEN, "{} download finished".format(tail(self.url)), bcolors.ENDC)
        except OSError as e:
            print(bcolors.FAIL, 'caught exception:', e, bcolors.ENDC)
            pass

pendingTasks = []
for url in find_image_src(limit=5):
    task = MyDownloadTask(url)
    task.start()

    pendingTasks.append(task)

for t in pendingTasks:
    assert isinstance(t, MyDownloadTask)
    t.join()
    print("{} finished".format(t))

