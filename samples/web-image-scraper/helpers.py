import re
from urllib import request
import http.client

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def find_image_src(url='http://www.lazada.com.my/highlights-top-sellers/', limit=10):
    req = request.Request(url)

    doc = request.urlopen(req)
    assert isinstance(doc, http.client.HTTPResponse)

    text = doc.read()

    count = 0
    for a in re.finditer(r'<\s*(.*)?>', text.decode()):
        if re.match(r'img', a.group(1)):
            m = re.search(r'src="(.*?)"', a.group(1))
            if m is not None:
                # print(count, m.group(1))
                yield m.group(1)
                count += 1
                if count >= limit:
                    break

def tail(fname):
    return fname[fname.rfind('/') + 1:]

def startDownloadingFile(url):
    outfile = "/tmp/download_{}".format(tail(url))
    # print("downloading {} to {}".format(self.url, outfile))
    req = request.Request(url)
    assert isinstance(req, request.Request)

    response = request.urlopen(req)
    assert isinstance(response, http.client.HTTPResponse)

    with open(outfile, 'wb') as out:
        bytes_read = 0
        buffer = bytearray(16384)
        while True:
            nbytes = response.readinto(buffer)
            if nbytes == 0:
                break
            out.write(buffer)
            bytes_read += nbytes
            # print('{} {}'.format(outfile, bytes_read))

