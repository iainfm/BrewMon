#!/usr/bin/python
import smtplib
import mysql.connector

server = smtplib.SMTP('{SMTP_SERVER}', 587)
sender = "{SMTP_SENDER}"
passwd = "{SMTP_PASSWORD}"
recipient = "{SMTP_RECIPIENT}"
subject = "BrewMon temperature alert"
min_temp=20
max_temp=22

config = {
        'user': 'brewmonuser',
        'password': 'beerbeerbeer',
        'host': '127.0.0.1',
        'database': 'brewDB',
        'raise_on_warnings': True
}

sql = "SELECT probe_name, last_temp FROM BrewMon WHERE probe_name='.Ambient.'"

cnx = mysql.connector.connect(**config)
cursor =cnx.cursor()
cursor.execute(sql)
cursor.close

for (probe_name, last_temp) in cursor:
   if ((last_temp < min_temp) or (last_temp > max_temp)):
      server.starttls()
      server.login(sender, passwd)
      msg = ("From: %s\r\n" % sender)
      msg = msg + ("To: %s\r\n" % recipient)
      msg = msg + ("Subject: %s\r\n\r\n" % subject)
      msg = msg + "Ambient temperature exceeded monitoring limits.\r\n\r\n"
      msg = msg + "Min: " + str(min_temp) + "\r\n"
      msg = msg + "Max: " + str(max_temp) + "\r\n"
      msg = msg + "Actual: " + str(last_temp) + "\r\n\r\n"
      server.sendmail(sender, recipient, msg)
      server.quit()
