import numpy


if __name__ == "__main__":
    data = numpy.fromfile("capture.bin",numpy.uint8)
    cpx = data[0::2] + 1j*data[1::2]