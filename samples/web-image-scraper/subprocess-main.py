
import subprocess

from helpers import *

def startDownloadingProcess(link):
    p1 = subprocess.Popen(['curl', link], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # start writing to file out1 from data arriving on input pipe p1 
    outfile = "/tmp/download_{}".format(tail(link))
    print("downloading to {}".format(outfile))
    with open(outfile, 'wb') as f:
        f.write(p1.stdout.read())

for link in find_image_src():
    try:
        startDownloadingProcess(link)
    except OSError as e:
        print(bcolors.FAIL, 'caught exception:', e, bcolors.ENDC)
        pass

