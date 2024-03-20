from stupidArtnet import StupidArtnetServer
import signal 
import time
import argparse

import sys
import hid

usage_page    = 0xFF60
usage         = 0x61
report_length = 32


def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

def hsv_qmk_range(h, s, v):
    """Convert HSV to QMK range."""
    return int(h/360*255), int((s/100)*255), int((v/100)*255)

# create a callback to handle data when received
def artnet_callback(rdata):
    """Test function to receive callback data."""
    # the received data is an array
    # of the channels value (no headers)
    # print('Received new data \n', rdata)
    #data = rdata[0:3]

    #print(rdata)

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    #request_data[1:len(data) + 1] = data
    request_data[1] = 1 #HSV

    device_interfaces = hid.enumerate(0, 0)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]
    raw_hid_interfaces_sorted = sorted(raw_hid_interfaces, key=lambda k: int(k['path'][len('/dev/hidraw'):]))
    keynum = 0
    for raw_hid in raw_hid_interfaces_sorted:
        try:
            interface = hid.Device(path=raw_hid['path'])
            addr = int(((keynum + 1) * 128) / (len(raw_hid_interfaces) + 1))
            h, s ,v = rgb_to_hsv(rdata[0+(addr*3)], rdata[1+(addr*3)], rdata[2+(addr*3)])
            request_data[2:5] = hsv_qmk_range(h, s, v)
            request_report = bytes(request_data)
            interface.write(request_report)
            keynum += 1
        except Exception as e:
            print(e)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit(0)


parser = argparse.ArgumentParser(description='artnet to hid') 
parser.add_argument('-u', type=int, help='universe to listen to', default=1)
universe = parser.parse_args().u

artnetserver = StupidArtnetServer()

signal.signal(signal.SIGINT, signal_handler)

# add a new listener with a optional callback
# the return is an id for the listener
u1_listener = artnetserver.register_listener(
    universe, callback_function=artnet_callback)

# giving it some time for the demo
while True:
    time.sleep(3)



