from stupidArtnet import StupidArtnetServer
import signal 
import time

import sys
import hid

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

# create a callback to handle data when received
def test_callback(rdata):
    """Test function to receive callback data."""
    # the received data is an array
    # of the channels value (no headers)
    # print('Received new data \n', rdata)
    data = rdata[0:3]

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_report = bytes(request_data)

    device_interfaces = hid.enumerate(0, 0)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]


    for raw_hid in raw_hid_interfaces:
        try:
            interface = hid.Device(path=raw_hid['path'])
            interface.write(request_report)
        except Exception as e:
            print(e)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit(0)

# You can use universe only
universe = 1
a = StupidArtnetServer()

signal.signal(signal.SIGINT, signal_handler)

# For every universe we would like to receive,
# add a new listener with a optional callback
# the return is an id for the listener
u1_listener = a.register_listener(
    universe, callback_function=test_callback)

# giving it some time for the demo
while True:
    time.sleep(3)



