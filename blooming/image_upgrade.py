"""image_upgrade.py -- upgrade image on test bed
Usage:
    will upgrade the image on every device within test bed
"""
import sys
import json
import getopt
import threading

from dev_parser import Dev_Entry


def file_parser():

    # parser the file name
    # the file is assgined by command line "-f *.tgz"
    inputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf", ["image file="])
    except getopt.error:
        print('test.py -f < image file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -f <image file>')
            sys.exit()
        elif opt in ("-f", "--image file"):
            inputfile = sys.argv[2]

    return inputfile


# upgrade in parallel for multiple devices at the same time
def imageupgrade(filename):
    with open('dev.json', 'r') as f:
        data = json.load(f)
        # create thread for each device to upgrade in parallel
        for entry in data:
            dev = Dev_Entry(entry)
            name = 'Thread-' + entry
            t = threading.Thread(target=dev.image_upgrade, name=name,
                                 args=(filename,), daemon=False)
            t.start()
        # make sure all child thread finished before main thread go ahead
        for t in threading.enumerate():
            if t is not threading.main_thread():
                t.join()

