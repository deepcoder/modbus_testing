#! /usr/bin/env python3
#force unbuffered stdout output for piping to another program
####! /usr/bin/env -S python3 -u

# min_mod_01.py
# 202106111336 

# read from XY-MD02 temperature and humidity modbus sensor
#

PROGRAM_NAME = "min_mod_01"
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


    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)

    # instrument.serial.port                     # this is the serial port name
    instrument.serial.baudrate = 9600         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.05          # seconds

    # instrument.address                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True

    print(instrument)

    ## Read temperature (PV = ProcessValue) ##
    temp_c = instrument.read_register(1, 1, 4)  # Registernumber, number of decimals, function code
    temp_f = (temp_c * 9.0/5.0) + 32
    print(f"Temp ℉        : {temp_f:.1f}")

    hum_p = instrument.read_register(2, 1, 4)  # Registernumber, number of decimals, function code
    print(f"Humidity %    : {hum_p:.1f}")

    print(f"Slave address : {instrument.read_register(0x0101, 0, 3)}")
    print(f"Modbus speed  : {instrument.read_register(0x0102, 0, 3)}")

    print(f"Temperature correction  : {instrument.read_register(0x0103, 0, 3)}")
    print(f"Humidity correction     : {instrument.read_register(0x0104, 0, 3)}")

    # ## Change temperature setpoint (SP) ##
    # NEW_TEMPERATURE = 95
    # instrument.write_register(24, NEW_TEMPERATURE, 1)  # Registernumber, value, number of decimals for storage




    # proper exit
    my_logger.info("Program end : " + PROGRAM_NAME + " Version : " + VERSION_MAJOR + "." + VERSION_MINOR)
    sys.exit(0)
 
if __name__ == '__main__':
   main()


# EOF
