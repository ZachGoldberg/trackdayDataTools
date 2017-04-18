import requests
import neighbourhood
import os
import zipfile

DATA_DIR = "data"


def discoverPhone():
    # First phase, try and use ARP to find a phone hosting some useful data.
    devices = neighbourhood.find_neighbors()
    for device in devices:
        try:
            response = requests.head("http://%s:9999" % device, timeout=1)
            print response
            return device
        except:
            print "Not %s" % device

def downloadFromPhone(device):
    response = requests.get("http://%s:9999/" % device, timeout=2)
    filename = response.url.split("/")[-1]
    content = response.content
    zippath = os.path.join(DATA_DIR, filename)
    f = open(zippath, 'wb')
    f.write(content)
    f.close()
    with zipfile.ZipFile(zippath) as zipdata:
        print zipdata.namelist()
        # Find the vbo file
        # extract the vbo file


if __name__ == '__main__':
    phoneIP = discoverPhone()
    files = downloadFromPhone(phoneIP)
