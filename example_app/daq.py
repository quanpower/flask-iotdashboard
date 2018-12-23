from socket import *
import time
import binascii
import datetime
# from bitstring import BitArray
import sqlite3
import struct

host  = '192.168.1.75'
port  = 502
addr = (host,port)
bufsize=1024

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

tcpClient = socket(AF_INET,SOCK_STREAM) # 这里的参数和UDP不一样。
tcpClient.connect(addr) #由于tcp三次握手机制，需要先连接


while True:
    print('\n' * 5)
    print('****************--------new data-------******************')
    print(datetime.datetime.now())

    data  = bytes.fromhex('00 00 00 00 00 06 01 04 00 00 00 08')
    # if not data or data=='exit':
    #     break
    tcpClient.send(data) 
    recv_data = tcpClient.recv(bufsize)
    print(recv_data)
    print(len(recv_data))

    data_hex= str(binascii.b2a_hex(recv_data))
    print('--------data-hex---------')
    print(data_hex)

    ai_int_list = []
    ai_value_list =[]
    print(ai_range_list)

    for i in range(0,len(ai_range_list)):
        ai = recv_data[9+2*i:9+2*i+2]
        ai_int = struct.unpack('>H',ai)[0] 
        ai_int_list.append(ai_int)
        pmax = ai_range_list[i]['pmax']
        pmin = ai_range_list[i]['pmin']
        print(pmax)
        print(pmin)
        ai_value = round(((pmax-pmin)/40000)*(ai_int - 10000) + pmin, 2)


        insert_daq_sql='''INSERT INTO DAQS (id, channel_id,daq_value,daq_time) VALUES(null, {0},{1},{2});'''.format(i+1, ai_value, int(time.time()))
        print(insert_daq_sql)
        cursor.execute(insert_daq_sql)

        high_limit = ai_range_list[i]['high_limit']
        low_limit = ai_range_list[i]['low_limit']


        if ai_value > high_limit:
            insert_alarm_sql='''INSERT INTO ALARM (id, channel_id,alarm_status,alarm_msg_type,alarm_time) VALUES(null, {0},{1},{2},{3});'''.format(i+1, 1, 1, int(time.time()))
            print(insert_alarm_sql)
            cursor.execute(insert_alarm_sql)
        elif ai_value < low_limit:
            insert_alarm_sql='''INSERT INTO ALARM (id, channel_id,alarm_status,alarm_msg_type,alarm_time) VALUES(null, {0},{1},{2},{3});'''.format(i+1, 1, 0, int(time.time()))
            print(insert_alarm_sql)
            cursor.execute(insert_alarm_sql)
        else:
            print('running ok')

        ai_value_list.append(ai_value)
    
    conn.commit()
    print(ai_int_list)
    print(ai_value_list)

    time.sleep(5)

tcpClient.close()
conn.close()