#!/usr/local/bin/python3
import numpy as np
import h5py
import time, sys, getopt, os, io

def generate_data(x,y,n,t):
    value = (x/10)**2*(y/10) + (y/10)**2*(x/10)+t/n
    value = value %1 # Keep number between 0 and 1
    return value

def write_data(X,Y,output,nFiles,i,hf):

    filename=("output/%s%05d" %(output,i))
    Z = generate_data(X,Y,nFiles,i)

    # Use old "filename" as dataset name
    t=time.time()
    hf.create_dataset(filename,data=Z)
    hf.flush()
    elapsed = time.time()-t

    return elapsed

def set_params(argv):
    nFiles=15
    size=100
    output="data"

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

    hf = h5py.File('output/data.h5', 'w')
    # Set XY coords
    x_origin=0
    y_origin=500
    x = np.arange(x_origin-size/2,x_origin+size/2,1)
    y = np.arange(y_origin-size/2,y_origin+size/2,1)
    X,Y = np.meshgrid(x,y)

    # Set benchmark vars
    time=np.zeros(nFiles)


    for i in range(0,nFiles):
        time[i] = write_data(X,Y,output,nFiles,i,hf)

    stats=time*1000

    print("------ Summary statistics ------")
    print("   Average write time = %1.3f ms" %stats.mean())
    print("   Std Dev            = %1.3f ms" %stats.std())
    print("   Min write time     = %1.3f ms" %stats.min())
    print("   Max write time     = %1.3f ms" %stats.max())
    print("   Number of writes   = %06d" %nFiles)

main(sys.argv[1:])
