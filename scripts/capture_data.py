import subprocess
import sys
import os
import time

def rtlPowerFFTW(baseline=None, bins=None, buffers=None, continuous=False, device=None, \
                elapsed=None, freq=[30e6, 100e6], gain=None, linear=False, matrix='capture', \
                n=None, overlap=None, ppm=None, quiet=False, rate=None, buffer_size=None, \
                strict_time=None, time=None, window=None, ignore_rest=False):
    '''
    This is a wrapper function for submitting fftw_power in python.  This will just submit the code
    from https://github.com/AD-Vega/rtl-power-fftw.

    Note that I have not actually setup ALL of the kwargs below as I have not used them and didn't
    spend the time to figure out what they do. 

    Parameters
    ----------
    baseline : int, optional
        Subtract baseline, read baseline data from a file or from standard input. See BASELINE AND 
        WINDOW FUNCTION DATA below for format and further considerations.
        Will append command with -B <file|->, --baseline <file|->
        Default is None.
    bins : int, optional
        Number of bins in the FFT spectrum (must be an even number).  Will append command with
        -b <bins in FFT spectrum>
        Default is None.
    buffers : int, optional
        Number of read buffers: don't touch unless running out of memory.  Default is None.
    continuous : bool, optional
        Repeat the same measurement endlessly. The spectra are written sequentially to the output 
        and a header is appended before each measurement (as usual).  Default is False.
    device : ?, optional 
        RTL-SDR device index of the device used for the measurement.  Default is None.
    elapsed : str, optional
        Allows to specify the recording duration in hours, sec, mins.  This will be appended to the
        command.  Formatting should resemble '5m' for 5 minutes.  Default is None.
    freq : list of ints, optional
        Center frequency of the receiver or the frequency range to scan. Given in Hz. Frequency 
        range consists of lower and upper bound, with the smaller frequency being used as the lower 
        bound and the larger as the upper.  Default is [30e6, 100e6].
    gain : int, optional
        Receiver gain, expressed in tenths of a decibel (e.g., 100 means 10 dB).  Default is None.
    linear : bool, optional
        Calculate linear power values instead of logarithmic.  Default is False.
    matrix : str, optional
        Specify a file name (no extension) and use it to store the power values in binary format 
        within a .bin file plus a metadata text file with .met extension.  Default is 'capture'.
    n : int
        Number of spectra to average (incompatible with -t).  Default is None.
    overlap : int
        Define lower boundary for overlap when frequency hopping (otherwise meaningless).  This sets
        the desired lower bound for overlap in percentage of bandwidth.  Default is None.
    ppm : int, optional
        Correct for the oscillator error of RTL-SDR device. The correction should be given in ppm.
        Default is None.
    quiet : bool
        Limit verbosity. Allows the various printouts to happen only the first time and not on every 
        scan.  Default is False
    rate : int, optional
        Sample rate of the receiver in Hz.  Default is None.
    buffer_size : int, optional
        Size of the read buffers (leave it as it is unless you know what you are doing).  Default is
        None.
    strict_time : bool, optional
        End measurement when the time set with time option is up, regardless of the number of 
        gathered samples.  Default is False. 
    time : str, optional
        Integration time (incompatible with -n). This is an effective integration time; see 
        INTEGRATION TIME below for more info (in short, the measurement might take longer than 
        that).  Same timing as elapsed.  Default is None.
    window : ?, optional
        Use a window function, read data from a file or from standard input. See BASELINE AND WINDOW 
        FUNCTION DATA below for format and further considerations.  Default is None.
    ignore_rest : bool, optional
        Ignore the rest of the labeled arguments following this flag.  Default is False.

    Returns
    -------
    output : str
        The std output value from running the command.
    error : str
        The std error output value from running the command.

    See Also
    --------
    https://github.com/AD-Vega/rtl-power-fftw/blob/master/doc/rtl_power_fftw.1.md
    '''
    command = 'rtl_power_fftw'
    if baseline is not None:
        command += ' --baseline %i'%int(baseline)
    if bins is not None:
        command += ' --bins %i'%int(bins)
    if buffers is not None:
        command += ' --bins %i'%int(bins)
    if continuous == True:
        command += ' --continue'
    if device is not None:
        command += ' --device %i'%int(device)
    if elapsed is not None:
        command += ' --elapsed %s'%elapsed
    if type(freq) is not list:
        print('freq must be a list.  Breaking.')
        return
    elif len(freq) == 1:
        command += ' --freq %i'%int(freq[0])
    elif len(freq) == 2:
        command += ' --freq %i:%i'%(int(min(freq)),int(max(freq)))
    else:
        print('freq must be a list of size 1 or 2.  Breaking.')
        return
    if gain is not None:
        command += ' --gain %i'%int(gain)
    if linear == True:
        command += ' --linear'
    if matrix is not None:
        command += ' --matrix %s'%str(matrix)
    if n is not None:
        command += ' --n %i'%int(n)
    if overlap is not None:
        command += ' --overlap %i'%int(overlap)
    if ppm is not None:
        command += ' --ppm %i'%int(ppm)
    if quiet == True:
        command += ' --quiet'
    if rate is not None:
        command += ' --rate %i'%int(rate)
    if buffer_size is not None:
        command += ' --buffer-size %i'%int(buffer_size)
    if strict_time is not None:
        command += ' --strict-time %i'%int(strict_time)
    if time is not None:
        command += ' --time %s'%str(time)
    if window is not None:
        command += ' --window %i'%int(window)
    if ignore_rest == True:
        command += ' --ignore_rest'

    print(command)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error


if __name__ == "__main__":
    #Should append the unix time here so that it doesn't overwrite. 
    if len(sys.argv) > 1:
        outfile = sys.argv[1]
    else:
        outfile = '/home/nuphase/BEACON-SDR/captures/capture'

    break_time = time.time() + 3600*2

    while True:
        call_time = time.time()

        print('Submitting rtl_power_fftw')

        outfile_new = outfile + '_' + str(call_time).replace('.','p')


        output, error = rtlPowerFFTW(baseline=None, \
                        bins=512, \
                        buffers=None, \
                        continuous=False, \
                        device=None, \
                        elapsed='30m', \
                        freq=[70e6, 100e6], \
                        gain=350, \
                        linear=False, \
                        matrix=outfile_new, \
                        n=None, \
                        overlap=None, \
                        ppm=None, \
                        quiet=True, \
                        rate=None, \
                        buffer_size=None, \
                        strict_time=None, \
                        time='1s', \
                        window=None, \
                        ignore_rest=False)


        os.system('touch %s.ready'%(outfile_new))
        print('Finished rtl_power_fftw and created .ready file.')
        print(output)
        print(error)
        if time.time() > break_time:
            break
