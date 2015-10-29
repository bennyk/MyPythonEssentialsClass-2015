
import os
from helpers import *

def startDownloadingProcess(link):
    print("[{}] start downloading to {}".format(os.getpid(), tail(link)))
    try:
        startDownloadingFile(link)
        print(bcolors.OKGREEN, "{} download finished".format(tail(link)), bcolors.ENDC)
    except OSError as e:
        print(bcolors.FAIL, 'caught exception:', e, bcolors.ENDC)
        os._exit(1)
    os._exit(0)

processes = []
for link in find_image_src(limit=99):
    newpid = os.fork()
    if newpid == 0:
        startDownloadingProcess(link)
    else:
        processes.append(newpid)

        if False:
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d" % pids)

            print('waiting for child to finish')
            os.waitpid(newpid, 0)

print(bcolors.BOLD, "waiting for all child process to complete", bcolors.ENDC)
for cpid in processes:
    pid, status = os.waitpid(cpid, 0)
    if status != 0:
        print(bcolors.FAIL, "pid [{}] has error: {}".format(pid, status), bcolors.ENDC)
    else:
        print(bcolors.OKGREEN, "pid [{}] is good.".format(pid), bcolors.ENDC)
print("parent finishing")

