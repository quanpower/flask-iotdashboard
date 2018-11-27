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

# conn = sqlite3.connect('d:\shuangye\counter.db', timeout=5)
# print("Opened database successfully")

# cursor = conn.cursor()


# select_sql = '''SELECT id, name, counter FROM counter;'''

# print("Table created successfully")


tcpClient = socket(AF_INET,SOCK_STREAM) # 这里的参数和UDP不一样。
tcpClient.connect(addr) #由于tcp三次握手机制，需要先连接


while True:
    print('\n' * 5)
    print('****************--------new data-------******************')
    print(datetime.datetime.now())

    # counter = []
    # results = cursor.execute(select_sql)

    # all_counter = results.fetchall()

    # for counter_record in all_counter:
    #     counter.append(counter_record[2])

    # print(counter)


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

    # ai1 = recv_data[9:11]
    # ai1_int = struct.unpack('>H',ai1)
    # print(ai1_int)
    # ai2 = recv_data[11:13]
    # ai2_int = struct.unpack('>H',ai2)
    # print(ai2_int)
    ai_range_list= [{'pmax':1000,'pmin':0,'unit':'mm'}] * 8
    ai_int_list = []
    ai_value_list =[]
    print(ai_range_list)

    for i in range(0,8):
        ai = recv_data[9+2*i:9+2*i+2]
        ai_int = struct.unpack('>H',ai)[0] 
        ai_int_list.append(ai_int)
        pmax = ai_range_list[i]['pmax']
        pmin = ai_range_list[i]['pmin']
        print(pmax)
        print(pmin)
        ai_value = ((pmax-pmin)/40000)*(ai_int - 10000) + pmin
        ai_value_list.append(ai_value)
    print(ai_int_list)
    print(ai_value_list)

    
    # di_0_7_str = data_hex[20:22]
    # di_8_16_str = data_hex[22:24]

    # di_0_7 = BitArray(hex=di_0_7_str)
    # di_8_16 = BitArray(hex=di_8_16_str)
    # print('-------bin-------')
    # print(di_0_7.bin)
    # print(di_8_16.bin)

    # di_0_7_reverse = di_0_7[::-1]
    # di_8_16_reverse = di_8_16[::-1]
    # print(di_0_7_reverse)
    # print(di_8_16_reverse)

    # reverse_list = []
    # for di in di_0_7_reverse:
    #     reverse_list.append(di)
    # for di in di_8_16_reverse:
    #     reverse_list.append(di)

    # print(reverse_list)

    # print('----reverse list-----')
    # for i in range(0,len(reverse_list)):
    #     print(i+1, reverse_list[i])
    #     if not reverse_list[i] and reverse_list[i] != status_list[LENGTH - 1][i]:
    #         history_list = []
    #         for j in range(0,len(status_list)):
    #             history_list.append(status_list[j][i])
    #         print('-----history list-----')
    #         print(history_list)
    #         if all(history_list):
    #             counter[i] += 1
    #             value = counter[i]
    #             update_sql = '''UPDATE COUNTER SET counter = {0} WHERE NAME = {1};'''.format(value, i+1)
    #             cursor.execute(update_sql)
    # conn.commit()
    
    # print('------counter-------')
    # print(counter)

    # for i in range(0,len(counter)):
    #     print(i+1,counter[i])

    # if len(status_list) > (LENGTH -1 ):
    #     status_list.pop(0)
    
    # status_list.append(reverse_list)

    # # print('-------status-list---------')
    # # for i in status_list:
    # #     print(i[0:10])
    # print('***' * 20)
    # print('\n' * 5)

    # # print(di_0_7[0])
    # # print(type(di_0_7[0]))

    time.sleep(5)

tcpClient.close()
# conn.close()