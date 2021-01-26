#!/usr/local/bin/python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import time, sys, getopt, os, io
mpl.use('Agg')

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def color_function(x,y,n,t):
    # From mathematica:
    # colorFunction[x_, y_, t_] := Round[Mod[(x /10)^2 y/10 + ((y)/10)^2 x/10 + t, 1], 3/256]
    value = (x/10)**2*(y/10) + (y/10)**2*(x/10)+t/n
    value = value %1 # Keep number between 0 and 1
    return value
def custom_colormap(filename):
    data=np.genfromtxt(filename,delimiter=',',dtype=None)
    my_cmap=mpl.colors.ListedColormap(data)
    return my_cmap


def write_plot(X,Y,output,nFrames,i,my_cmap):

    plotname=("output/%s%05d.png" %(output,i))
    Z = color_function(X,Y,nFrames,i)

    imSize=5
    fig=plt.figure()
    fig.set_size_inches((imSize,imSize))
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    #ax = plt.Axes()
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(Z,cmap=my_cmap,aspect='equal')
    img = fig2img(fig)
    #ax.imshow(Z,cmap=my_cmap)

    t=time.time()
    img.save(plotname,format="PNG")
    elapsed = time.time()-t
    #print("%s saved in %f s" %(plotname,elapsed))

    plt.close()

    write_size=os.path.getsize(plotname)
    return [elapsed,write_size]

def set_params(argv):
    nFrames=15
    size=100
    output="plot"

    try:
        opts,args=getopt.getopt(argv,"hn:s:0:",["nFrames=","size=", "output="])
    except getopt.GetoptError:
        print("plot.py -n <number_of_frames> -s <array_size> -o <outfile>")
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            print("plot.py -n <number_of_frames> -s <array_size> -o <outfile>")
            sys.exit()
        elif opt in ("-n", "--nFrames"):
            print("Setting nFrames")
            nFrames = int(float(arg))
        elif opt in ("-s", "--size"):
            print("Setting size")
            size = int(float(arg))
        elif opt in ("-o", "--output"):
            print("Setting output")
            output = arg

# Summarize params
    print('nFrames=%s' %nFrames)
    print('size= %s' %size)
    print('output_template=%s%%06d.png ' %output)

    return nFrames,size,output


def main(argv):

    nFrames,size,output = set_params(argv)

    # Set XY coords
    x_origin=0
    y_origin=500
    x = np.arange(x_origin-size/2,x_origin+size/2,1)
    y = np.arange(y_origin-size/2,y_origin+size/2,1)
    X,Y = np.meshgrid(x,y)

    # Set benchmark vars
    time=np.zeros(nFrames)
    size=np.zeros(nFrames)

    # Custom pastel colormap
    pastel=custom_colormap("colors.txt")

    for i in range(0,nFrames):
        time[i],size[i] = write_plot(X,Y,output,nFrames,i,pastel)
        
    stats=size/time /1024**2

    print("------ Summary statistics ------")
    print("   Average write speed = %1.3f MB/s" %stats.mean())
    print("   Std Dev             = %1.3f MB/s" %stats.std())
    print("   Min write speed     = %1.3f MB/s" %stats.min())
    print("   Max write speed     = %1.3f MB/s" %stats.max())
    print("   Number of writes     = %06d" %nFrames)

main(sys.argv[1:])
