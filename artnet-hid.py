from stupidArtnet import StupidArtnetServer
import signal 
import time

import sys
import hid

vendor_id     = 0x534B
product_id    = 0x1020

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

global interface

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])
    print(f"Manufacturer: {interface.manufacturer}")
    print(f"Product: {interface.product}")

    return interface



# create a callback to handle data when received
def test_callback(rdata):
    """Test function to receive callback data."""
    # the received data is an array
    # of the channels value (no headers)
    print('Received new data \n', rdata)
    data = rdata[0:3]

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_report = bytes(request_data)
    interface.write(request_report)



# a Server object initializes with the following data
# universe 			= DEFAULT 0
# subnet   			= DEFAULT 0
# net      			= DEFAULT 0
# setSimplified     = DEFAULT True
# callback_function = DEFAULT None


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    interface.close()
    global a
    del a
    exit(0)


device_interfaces = hid.enumerate(vendor_id, product_id)
raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]
interface = hid.Device(path=raw_hid_interfaces[0]['path'])

# You can use universe only
universe = 1
a = StupidArtnetServer()

signal.signal(signal.SIGINT, signal_handler)

# For every universe we would like to receive,
# add a new listener with a optional callback
# the return is an id for the listener
u1_listener = a.register_listener(
    universe, callback_function=test_callback)


# or disable simplified mode to use nets and subnets as per spec
# subnet = 1 (would have been universe 17 in simplified mode)
# net = 0
# a.register_listener(universe, sub=subnet, net=net,
#                    setSimplified=False, callback_function=test_callback)


# print object state
print(a)

# giving it some time for the demo
while True:
    time.sleep(3)



