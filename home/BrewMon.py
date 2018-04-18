#!/usr/bin/python
import os
import time
import simplejson
import json
import sys
import datetime
import mysql.connector

SLAVES_FILE = '/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves'
BUS_ROOT = '/sys/bus/w1/devices/'
TEMP_PRECISION = 1 # number of decimal places

config = {
	'user': 'brewmonuser',
	'password': 'beerbeerbeer',
	'host': '127.0.0.1',
	'database': 'brewDB',
	'raise_on_warnings': True
}

# Read the device IDs of the probes
with open(SLAVES_FILE) as f:
    devices = f.readlines()
devices = [x.strip() for x in devices]
devices.sort()

# Build the list of paths to the sensor devices
temp_sensor = [os.path.join(BUS_ROOT, device) for device in devices]
temp_sensor = [os.path.join(sensor, 'w1_slave') for sensor in temp_sensor]

def temp_raw(sensor):
	try:
	   f = open(sensor,'r')
	   lines = f.readlines()
	   f.close
	except:
	   lines = ['YES', 't=-9999000']
	return lines

def read_temp(sensor):
	lines = temp_raw(sensor)
	while lines[0].strip()[-3:]!='YES':
		time.sleep(0.2)
		lines = temp_raw(sensor)
	temp_output = lines[1].find('t=')

	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return round(temp_c, TEMP_PRECISION)

s = [read_temp(x) for x in temp_sensor]

cnx = mysql.connector.connect(**config)

clear_active_probes = "update BrewMon set probe_active=0"
cursor=cnx.cursor()
cursor.execute(clear_active_probes)
cnx.commit

update_table = ("INSERT INTO BrewMon "
		"(probe_id, probe_name, last_temp, probe_active) "
		"VALUES (%s, %s, %s, 1) "
		"ON DUPLICATE KEY UPDATE "
		"last_temp=%s, probe_active=1")

for index, device in enumerate(devices):
   sql_data = (device, '-', s[index], s[index])
   # print update_table
   # print sql_data
   try:
      cursor = cnx.cursor()
      cursor.execute(update_table, sql_data)
      cnx.commit()
   except:
      # print(cursor.statement)
      raise

cursor.close
cnx.close
