#!/usr/bin/python
import os
import time
import json
import sys
import datetime
import gspread
import mysql.connector
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

GDOCS_OAUTH_JSON = '/home/pi/TemPiMon.json'
GDOCS_SPREADSHEET_NAME = 'BrewMon'
FREQUENCY_SECONDS = 30

def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds',
		  'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
	sh = gc.open(spreadsheet)
        worksheet = sh.worksheet("BrewMonSQL")
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

config = {
        'user': 'brewmonuser',
        'password': 'beerbeerbeer',
        'host': '127.0.0.1',
        'database': 'brewDB',
        'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
sql = "SELECT probe_name, last_temp FROM BrewMon WHERE probe_active=1 AND probe_name != '-' ORDER BY probe_name"
cursor.execute(sql)

j=0
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
name=[]
temp=[now]
for (probe_name, last_temp) in cursor:
	name.append(probe_name)
	temp.append(last_temp)
cursor.close
cnx.close

worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
worksheet.delete_row(1)
header=['Timestamp']

for index, item in enumerate(name):
	header.extend([item])
worksheet.insert_row(header,1)
worksheet.append_row(temp)
