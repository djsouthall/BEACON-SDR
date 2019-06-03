import time
import os
import sys
import glob
from paramiko import SSHClient
from scp import SCPClient

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    if type(filename) == bytes:
        filename = filename.decode()
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )


if __name__ == "__main__":
    input_dir = '/home/nuphase/BEACON-SDR/captures/' #On Beagle (Where the script should be run.
    output_dir = '/home/dsouthall/BEACON-SDR/captures/' #On Sundog
    wait_time = 10 #s
    extensions = ['*.bin','*.met']
    call_time = time.time()
    
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect('sundog.uchicago.edu',username='dsouthall')
    
    # SCPCLient takes a paramiko transport and progress callback as its arguments.
    with SCPClient(ssh.get_transport(), progress=progress) as scp:
        while True:
            files = []
            for ext in extensions:
                files.extend(glob.glob(input_dir + ext))
            for f in files:
                f = f.replace('\\','/') # To handle windows paths.
                t = os.path.getmtime(f)
                if t >= call_time:
                    print('Transferring file modified since last call and appending unix time to name:')
                    f_new = f.replace('.','_' + str(call_time).replace('.','p') + '.')
                    f_new = output_dir + f_new.split('/')[-1]
                    print(f_new)
                    #os.rename(f,f_new) #Might want to do an scp if doing between pcs?
                    scp.put(f, f_new)
                    print('\n')
                    os.remove(f)
                    print('%s removed from local storage.\n'%f)
            call_time = time.time()
            time.sleep(wait_time)
        scp.close()
