#! /usr/bin/env python3
#force unbuffered stdout output for piping to another program
####! /usr/bin/env -S python3 -u

# dataq_DI-903MB-0900.py
# 202106111440  

# interact with dataq DI-903MB-900
#
# www.dataq.com
#

PROGRAM_NAME = "dataq_DI-903MB-0900"
VERSION_MAJOR = "1"
VERSION_MINOR = "0"
WORKING_DIRECTORY = ""
# 
#

import time
import sys

# check version of python
if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
    print("This script requires Python 3.8 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)
#print("{} {} is using Python {}.{}.".format(PROGRAM_NAME, VERSION_MAJOR + "." + VERSION_MINOR, sys.version_info.major, sys.version_info.minor))


import logging
import logging.handlers

import serial
import minimalmodbus


# Logging setup

# select logging level
LOGGING_LEVEL_FILE_NAME = 'INFO'
LOGGING_LEVEL_RSYSLOG_NAME = 'INFO'

# nueric logging value
logging_level_file = logging.getLevelName(LOGGING_LEVEL_FILE_NAME)
logging_level_rsyslog = logging.getLevelName(LOGGING_LEVEL_RSYSLOG_NAME)

# log to both a local file and to a rsyslog server
LOG_FILENAME = PROGRAM_NAME + '.log'
LOG_RSYSLOG = ('192.168.2.5', 514)

root_logger = logging.getLogger()

#set loggers

# file logger
handler_file = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=5)
handler_file.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-8s ' + PROGRAM_NAME + ' ' + '%(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
handler_file.setLevel(logging_level_file)

root_logger.addHandler(handler_file)

# Roll over file logs on application start
handler_file.doRollover()

# rsyslog handler
handler_rsyslog = logging.handlers.SysLogHandler(address = LOG_RSYSLOG)
handler_rsyslog.setFormatter(logging.Formatter(fmt=PROGRAM_NAME + ' ' + '%(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
handler_rsyslog.setLevel(logging_level_rsyslog)

root_logger.addHandler(handler_rsyslog)

my_logger = logging.getLogger(PROGRAM_NAME)
my_logger.setLevel(logging_level_file)

def main():

    my_logger.info("Program start : " + PROGRAM_NAME + " Version : " + VERSION_MAJOR + "." + VERSION_MINOR)


    slave_address = 247
    # slave_address = 15
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slave_address)  # port name, slave address (in decimal)

    # instrument.serial.port                     # this is the serial port name
    instrument.serial.baudrate = 9600         # Baud
    # instrument.serial.baudrate = 38400         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.05          # seconds

    # instrument.address                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True
    instrument.close_port_after_each_call = True

    print(instrument)

    print("-----")

    # register = 0

    # return_value = instrument.read_register(register, 0, 3)

    # print(f"Address {register} : {return_value:#02}")
    # print(f"Address {register} : {return_value:#02x}")
    # print(f"Address {register} : {return_value:>08b}")

    # register = 1

    # return_value = instrument.read_register(register, 0, 3)

    # print(f"Address {register} : {return_value:#02}")
    # print(f"Address {register} : {return_value:#02x}")
    # print(f"Address {register} : {return_value:>08b}")

    # register = 2

    # return_value = instrument.read_register(register, 0, 3)

    # print(f"Address {register} : {return_value:#02}")
    # print(f"Address {register} : {return_value:#02x}")
    # print(f"Address {register} : {return_value:>08b}")

    # register = 3

    # return_value = instrument.read_register(register, 0, 3)

    # print(f"Address {register} : {return_value:#02}")
    # print(f"Address {register} : {return_value:#02x}")
    # print(f"Address {register} : {return_value:>08b}")


    # reset address and baud rate to default values
    print("-----")


    # register = 0

    # return_value = instrument.write_register(register, 247, 0, 6)

    # return_value = instrument.read_register(register, 0, 3)

    # print(f"Address {register} : {return_value:#02}")
    # print(f"Address {register} : {return_value:#02x}")
    # print(f"Address {register} : {return_value:>08b}")

    # register = 1

    # return_value = instrument.write_register(register, 2, 0, 6)


    # return_value = instrument.read_register(register, 0, 3)

    # print(f"Address {register} : {return_value:#02}")
    # print(f"Address {register} : {return_value:#02x}")
    # print(f"Address {register} : {return_value:>08b}")


    # instrument.debug = True
    # # print(f"Coil 0 : {instrument.read_register(0x0, 0, 4):#02x}")

    # instrument._perform_command(17, '')

    instrument.debug = False

    while (True) :
        print("on")
        instrument._perform_command(5, '\x00\x00\xff\x00')
        time.sleep(1.0)
        instrument._perform_command(5, '\x00\x01\xff\x00')
        time.sleep(1.0)
        instrument._perform_command(5, '\x00\x02\xff\x00')
        time.sleep(1.0)
        instrument._perform_command(5, '\x00\x03\xff\x00')
        time.sleep(1.0)

        print("off")
        instrument._perform_command(5, '\x00\x00\x00\x00')
        time.sleep(1.0)
        instrument._perform_command(5, '\x00\x01\x00\x00')
        time.sleep(1.0)
        instrument._perform_command(5, '\x00\x02\x00\x00')
        time.sleep(1.0)
        instrument._perform_command(5, '\x00\x03\x00\x00')
        time.sleep(1.0)

    sys.exit(0)

    # z_bit = 0

    # for i in range(0, 5) :

    #     print(i)

    #     register = 0

    #     # return_value = instrument.read_bit(register, 2)

    #     # print(f"Address {register} : {return_value:#02}")
    #     # print(f"Address {register} : {return_value:#02x}")
    #     # # print(f"Address {register} : {return_value:>08b}")    

    #     if (z_bit == 0) :
    #         z_bit = 1
    #         print(z_bit)
    #         instrument._perform_command(0x05, '\x00\x09\xff\x00')
    #     else :
    #         z_bit = 0
    #         print(z_bit)
    #         instrument._perform_command(5, '\x00\x09\x00\x00')

    #     # return_value = instrument.write_register(register, z_bit, 0, 6)

    #     time.sleep(2.0)

    # proper exit
    my_logger.info("Program end : " + PROGRAM_NAME + " Version : " + VERSION_MAJOR + "." + VERSION_MINOR)
    sys.exit(0)
 
if __name__ == '__main__':
   main()


# EOF
