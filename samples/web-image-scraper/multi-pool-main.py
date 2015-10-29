

import multiprocessing
from helpers import *

def download(url):
    name = multiprocessing.current_process().name
    try:
        print("{}: downloading {}".format(name, url))
        startDownloadingFile(url)
        print(bcolors.OKGREEN, "{}: {} download finished".format(name, tail(url)), bcolors.ENDC)
    except OSError as e:
        print(bcolors.FAIL, 'caught exception:', e, bcolors.ENDC)
        pass


with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    pool.map(download, find_image_src(), chunksize=2)

    pool.close()
    pool.join()
