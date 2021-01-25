import numpy as np
import time, sys, getopt, re, os
import matplotlib.pyplot as plt


def read_image(image):
    t=time.time()
    plt.imread(image)
    elapsed=time.time()-t
    #print("Read %s in %f s" %(image, elapsed))
    write_size=os.path.getsize(image)
    return [elapsed,write_size]

def main(argv):

    files = os.listdir()
    default_re=re.compile(".*.png")
    imageList=list(filter(default_re.match,files))


    try:
        opts,args=getopt.getopt(argv,"hi:",["images="])
    except getopt.GetoptError:
        print("read.py -i <list_of_images>")
        sys.exit(2)
    print(opts)
    for opt,arg in opts:
        if opt=='-h':
            print("read.py -i <list_of_images>")
            sys.exit()
        elif opt in ("-i", "--images"):
            r = re.compile(arg)
            imageList = list(filter(r.match,files))
            print("Setting image list to ")
            print(imageList)
    time=np.zeros(len(imageList))
    size=np.zeros(len(imageList))
    counter=0
    for image in imageList:
        time[counter],size[counter] =read_image(image)
        counter = counter +1

    stats=size/time /1024**2

    print("------ Summary statistics ------")
    print("   Average read speed = %1.3f MB/s" %stats.mean())
    print("   Std Dev             = %1.3f MB/s" %stats.std())
    print("   Min read speed     = %1.3f MB/s" %stats.min())
    print("   Max read speed     = %1.3f MB/s" %stats.max())
    print("   Number of reads     = %06d" %counter)

main(sys.argv[1:])
