#! /usr/bin/env python3
#force unbuffered stdout output for piping to another program
####! /usr/bin/env -S python3 -u

# pe11_xy-md02_01.py
# 202107101252

# read from XY-MD02 temperature and humidity modbus sensor via pe11 ethernet modbus rs-485 to ethernet bridge
#

PROGRAM_NAME = "pe11_xy-md02_01"
VERSION_MAJOR = "1"
VERSION_MINOR = "0"
WORKING_DIRECTORY = ""
# 
#

import sys

# check version of python
if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
    print("This script requires Python 3.8 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)
#print("{} {} is using Python {}.{}.".format(PROGRAM_NAME, VERSION_MAJOR + "." + VERSION_MINOR, sys.version_info.major, sys.version_info.minor))


import logging
import logging.handlers

# https://pymodbustcp.readthedocs.io/en/latest/
# https://pymodbustcp.readthedocs.io/en/latest/package/class_ModbusClient.html#class-pymodbustcp-client-modbusclient

from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.2.37"
SERVER_PORT = 8899

c = ModbusClient()

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(1)
c.timeout(2)
c.debug(False)

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():

        reg = c.read_input_registers(1, 1)
        if c.last_error() == 0 :
            temp_c = reg[0] / 10.0
            temp_f = (temp_c * 9.0/5.0) + 32
            print(f"Temp ℉        : {temp_f:.1f}")
            # print("reg ad #1: "+ str(reg))
        else :
            print(c.last_error(), c.last_error_txt())

        reg = c.read_input_registers(2, 1)
        if c.last_error() == 0 :
            hum_p = reg[0] / 10.0
            print(f"Humidity %    : {hum_p:.1f}")
            # print("reg ad #2: "+ str(reg))
        else :
            print(c.last_error(), c.last_error_txt())


    # sleep 2s before next polling
    time.sleep(2)

# EOF
