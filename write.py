#!/usr/local/bin/python3
import numpy as np
import time, sys, getopt, os, io

def generate_data(x,y,n,t):
    value = (x/10)**2*(y/10) + (y/10)**2*(x/10)+t/n
    value = value %1 # Keep number between 0 and 1
    return value

def write_data(X,Y,output,nFiles,i):

    filename=("output/%s%05d.txt" %(output,i))
    Z = generate_data(X,Y,nFiles,i)

    t=time.time()
    np.savetxt(filename,Z)
    elapsed = time.time()-t

    write_size=os.path.getsize(filename)
    return [elapsed,write_size]

def set_params(argv):
    nFiles=15
    size=100
    output="plot"

    try:
        opts,args=getopt.getopt(argv,"hn:s:0:",["nFiles=","size=", "output="])
    except getopt.GetoptError:
        print("plot.py -n <number_of_files> -s <array_size> -o <outfile>")
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            print("plot.py -n <number_of_files> -s <array_size> -o <outfile>")
            sys.exit()
        elif opt in ("-n", "--nFiles"):
            print("Setting nFiles")
            nFiles = int(float(arg))
        elif opt in ("-s", "--size"):
            print("Setting size")
            size = int(float(arg))
        elif opt in ("-o", "--output"):
            print("Setting output")
            output = arg

# Summarize params
    print('nFiles=%s' %nFiles)
    print('size= %s' %size)
    print('output_template=%s%%06d.png ' %output)

    return nFiles,size,output


def main(argv):

    nFiles,size,output = set_params(argv)

    # Set XY coords
    x_origin=0
    y_origin=500
    x = np.arange(x_origin-size/2,x_origin+size/2,1)
    y = np.arange(y_origin-size/2,y_origin+size/2,1)
    X,Y = np.meshgrid(x,y)

    # Set benchmark vars
    time=np.zeros(nFiles)
    size=np.zeros(nFiles)


    for i in range(0,nFiles):
        time[i],size[i] = write_data(X,Y,output,nFiles,i)

    stats=size/time /1024**2

    print("------ Summary statistics ------")
    print("   Average write speed = %1.3f MB/s" %stats.mean())
    print("   Std Dev             = %1.3f MB/s" %stats.std())
    print("   Min write speed     = %1.3f MB/s" %stats.min())
    print("   Max write speed     = %1.3f MB/s" %stats.max())
    print("   Number of writes     = %06d" %nFiles)

main(sys.argv[1:])
