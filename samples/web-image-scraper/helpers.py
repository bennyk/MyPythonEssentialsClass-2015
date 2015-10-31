"""
Provides helper functions for the demo.
"""

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
    """
    Scrape a given URL for a list of potential URL images based on HTML's image markup '<img ...>'.
    find_image_src() is a generator function.
    :param url: any website URL.
    :param limit: Yield to a limited number of image markup
    """
    req = request.Request(url)

    doc = request.urlopen(req)
    assert isinstance(doc, http.client.HTTPResponse)

    text = doc.read()

    count = 0

    # scan the doc for any HTML markup <...>
    for a in re.finditer(r'<\s*(.*)?>', text.decode()):

        # we are interested on markup with the keyword 'img' which indicates a potential image URL resource
        if re.match(r'img', a.group(1)):

            # extract the URL out from the markup src=... and yield it to the parent
            m = re.search(r'src="(.*?)"', a.group(1))
            if m is not None:
                # print(count, m.group(1))
                yield m.group(1)
                count += 1
                if count >= limit:
                    break

def tail(fname):
    """
    parse a slash delimited path for tail
    :param fname: any slash delimited string.
    :return: tail
    """
    return fname[fname.rfind('/') + 1:]

def startDownloadingFile(url):
    """
    Routine to download a given URL resource to a file remotely.
    :param url: Any remote URL resource
    """
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

