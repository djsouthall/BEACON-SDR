import matplotlib.pyplot as plt, mpld3
import numpy
import glob

if __name__ == "__main__":
    capture_location = '/home/dsouthall/BEACON-SDR/captures/'
    
    capture_files = glob.glob(capture_location + '*bin')
    
    plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
    #mpld3.show()
