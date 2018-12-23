from socket import *
import time
import binascii
import datetime
# from bitstring import BitArray
import sqlite3
import struct


conn = sqlite3.connect('daq.db', timeout=5)
print("Opened database successfully")

cursor = conn.cursor()


select_sql = '''SELECT * FROM channels;'''
results = cursor.execute(select_sql)
all_channels = results.fetchall()

print("Table selected successfully")
ai_range_list= []

for channel in all_channels:
    ai_range_list.append({'channel_name':channel[1], 'pmax':channel[2],'pmin':channel[3],'high_limit':channel[4],'low_limit':channel[5],'unit':channel[6]})

print(ai_range_list)


# update_sql = "update channels set high_limit = 50, low_limit=10, unit=c where id =1"

# cursor.execute(update_sql)
conn.close()