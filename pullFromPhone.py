import gzip
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

    if devices:
        firstthree = ".".join(devices[0].split(".")[0:3])
        return "%s.%s" % (firstthree, raw_input("Couldn't auto discover device IP.  Type in last octect: "))
    else:
        return raw_input("Couldn't auto discover device IP.  Type in full IP: ")

def downloadFromPhone(device):
    response = requests.get("http://%s:9999/" % device, timeout=2)
    filename = response.url.split("/")[-1]
    content = response.content
    zippath = os.path.join(DATA_DIR, filename)
    f = open(zippath, 'wb')
    f.write(content)
    f.close()
    return zippath

def extract(zipdata, fname):
    zfile = zipdata.open(fname)
    nfile_path = os.path.join(DATA_DIR, fname)
    nfile = open(nfile_path, 'wb')
    nfile.write(zfile.read())
    nfile.close()
    return nfile_path

def extract_gz(zipdata, fname):
    nfile_path = extract(zipdata, fname)
    with gzip.open(nfile_path, 'rb') as f:
        content = f.read()
        nfile2_p = nfile_path.replace(".gz", "")
        nfile2 = open(nfile2_p, 'wb')
        nfile2.write(content)
        nfile2.close()
        return nfile2_p

def extractVbo(zippath):
    with zipfile.ZipFile(zippath) as zipdata:
        files = zipdata.namelist()
        for fname in files:
            if ".vbo.gz" in fname:
                return extract_gz(zipdata, fname)
            elif ".vbo" in fname:
                return extract(zipdata, fname)


if __name__ == '__main__':
    phoneIP = discoverPhone()
    zipfile_path = downloadFromPhone(phoneIP)
    print "Zipfile from phone: %s" % zipfile_path
    vbofile = extractVbo(zipfile_path)
