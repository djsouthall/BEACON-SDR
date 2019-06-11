import matplotlib.pyplot as plt, mpld3
import numpy
import glob

if __name__ == "__main__":
    capture_location = '/home/dsouthall/BEACON-SDR/captures/'
    
    capture_files = glob.glob(capture_location + '*bin')
    
    f = capture_files[-1]
    with open(f.replace('.bin','.met')) as m:
        meta = m.readlines()
        bins = int(meta[0].split(' # ')[0]) #columns
        scans = int(meta[1].split(' # ')[0]) #rows
        f_start = int(meta[2].split(' # ')[0]) #Hz
        f_end = int(meta[3].split(' # ')[0]) #Hz
        f_step = int(meta[4].split(' # ')[0]) #Hz
        integration_eff = float(meta[5].split(' # ')[0]) #s
        scan_dur = float(meta[5].split(' # ')[0]) #s
        t_start_utc = meta[6].split(' # ')[0]
        t_end_utc = meta[7].split(' # ')[0]

    data = numpy.fromfile(f,numpy.float32) 
    # = numpy.reshape(data,(bins,-1)).T #Should read from .met
    
    plt.imshow(data)
    #plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
    #mpld3.show()
