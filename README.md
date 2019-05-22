# RTL-SDR
The code used for the rtl-sdr for BEACON.

A BBB is hooked up to an SDR.  The goal is to turn this into a small
spectrum analyzer for the BEACON experiment.

The scripts in this git may also be clone to the BBB, however not all of
them should be run onboard (as this is a limited device).  Some will be
designed to be run remotely on Midway.


# Dependencies
- I will be writing code from >python 3.5 to start.
- rtl-sdr 
- gnuradio


# People 

Dan Southall
dsouthall@uchicago.edu

Useful Links:
https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr

https://github.com/anitaNeutrino/anitaFlightSoft/tree/master/programs/RTLd

https://www.instructables.com/id/rtl-sdr-on-Ubuntu/
