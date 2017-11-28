#!/usr/bin/python

import smbus
import math
import time
import web
import datetime
import time
import os
import re
import sys
import argparse
import subprocess
from pprint import pprint


def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

class index:
  def GET(self):
    time.sleep(0.1)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    time.sleep(0.5)

    x_rot = float(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    y_rot = float(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    return "%f %f" % (x_rot, y_rot)

if __name__ == "__main__":
  # Variables
  base_path = os.path.expanduser('~')

  # Load Configuration
  config_file = base_path + "/capture.conf"  

  # log Variables
  log_file = base_path + "/" + datetime.date.today().__format__("%y%m%d") + ".dat"


  # Power management registers
  power_mgmt_1 = 0x6b
  power_mgmt_2 = 0x6c

  bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
  address = 0x68       # This is the address value read via the i2cdetect command
  urls = ('/', 'index')
  server = False
  #server = True

  # Now wake the 6050 up as it starts in sleep mode
  bus.write_byte_data(address, power_mgmt_1, 0)

  if server is True:
      app = web.application(urls, globals())
      app.run()
  else:
      #fhandler = open(log_file, "w")
      while True:
          fhandler = open(log_file, "a")
          time.sleep(0.1)
          gyro_xout = read_word_2c(0x43)
          gyro_yout = read_word_2c(0x45)
          gyro_zout = read_word_2c(0x47)
  
          accel_xout = read_word_2c(0x3b)
          accel_yout = read_word_2c(0x3d)
          accel_zout = read_word_2c(0x3f)

          accel_xout_scaled = accel_xout / 16384.0
          accel_yout_scaled = accel_yout / 16384.0
          accel_zout_scaled = accel_zout / 16384.0

          xrot = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
          yrot = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

	  fhandler.write("%f,%f,%f,%f\n" % (time.time(), xrot, yrot, 0.0))

          time.sleep(0.5)
          fhandler.close()
