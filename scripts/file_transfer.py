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
    extensions = ['*.ready'] #Only want it to transfer files once the .met file has been made, i.e. once it is complete.
    call_time = time.time()
    
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect('sundog.uchicago.edu',username='dsouthall')
    
    loading_string = ''
    while True:
        files = []
        for ext in extensions:
            files.extend(glob.glob(input_dir + ext))
        for f in files:
            f = f.replace('\\','/') # To handle windows paths.
            t = os.path.getmtime(f)
            if t >= call_time:
                loading_string = '.'
                # SCPCLient takes a paramiko transport and progress callback as its arguments.
                # Might want to look into a keep alive if I only want to ssh once and not every call.
                with SCPClient(ssh.get_transport(), progress=progress) as scp:
                    #ready file
                    f_new = output_dir + f.split('/')[-1]
                    try:
                        print('Removing %s'%f)
                        os.remove(f)
                    except Exception as e:
                        print('Failed deleting %s.'%f)
                        print(e)
                    #met file
                    try:
                        f = f.replace('.ready','.met')
                        f_new = f_new.replace('.ready','.met')
                        print('Transferring met file modified since last call')
                        scp.put(f, f_new)
                        print('\n')
                        os.remove(f)
                        print('%s removed from local storage.\n'%f)
                    except Exception as e:
                        print('Failed copying/deleting %s.'%f)
                        print(e)

                    #bin file
                    try:
                        f = f.replace('.met','.bin')
                        f_new = f_new.replace('.met','.bin')
                        print('Transferring bin file modified since last call')
                        scp.put(f, f_new)
                        print('\n')
                        os.remove(f)
                        print('%s removed from local storage.\n'%f)
                    except Exception as e:
                        print('Failed copying/deleting %s.'%f)
                        print(e)

                scp.close()
            else:
                if loading_string == '...':
                    loading_string = ''
                    sys.stdout.write('   ' + '\r')
                    sys.stdout.flush()    
                loading_string = loading_string + '.'
                sys.stdout.write(loading_string + '\r')
                sys.stdout.flush()

        call_time = time.time()
        time.sleep(wait_time)
