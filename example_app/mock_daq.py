import sqlite3

import datetime
import time

conn = sqlite3.connect('daq.db', timeout=5)
print("Opened database successfully")

cursor = conn.cursor()



# cursor.execute('''
# 		INSERT INTO CHANNELS (id,name,pmax,pmin,high_limit,low_limit,unit) VALUES(NULL,{0},{1},{2},{3},{4},{5});
# 		'''.format('oil_temperature_1',100,0,60,10,'℃'))

# print('insert ok!')
# channel 0-7:oil_temperature_1,oil_level_1,water_level_1,oil_temperature_2,oil_level_2,water_level_2,water_level_3,

# sql1= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'oil_temperature_1',{0},{1},{2},{3},'oc');'''.format(100,0,50,10,)
# print(sql1)
# cursor.execute(sql1)


# sql2= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'oil_level_1',{0},{1},{2},{3},'mm');'''.format(1000,0,800,500,)
# print(sql2)
# cursor.execute(sql2)

# sql3= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'water_level_1',{0},{1},{2},{3},'mm');'''.format(1000,0,200,100,)
# print(sql3)
# cursor.execute(sql3)

# sql4= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'oil_temperature_2',{0},{1},{2},{3},'oc');'''.format(100,0,50,10,)
# print(sql4)
# cursor.execute(sql4)


# sql5= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'oil_level_2',{0},{1},{2},{3},'mm');'''.format(1000,0,800,500,)
# print(sql5)
# cursor.execute(sql5)

# sql6= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'water_level_2',{0},{1},{2},{3},'mm');'''.format(1000,0,200,100,)
# print(sql6)
# cursor.execute(sql6)


# sql7= '''INSERT INTO CHANNELS (id,channel_name,pmax,pmin,high_limit,low_limit,unit) VALUES (NULL,'water_level_3',{0},{1},{2},{3},'mm');'''.format(1000,0,200,100,)
# print(sql7)
# cursor.execute(sql7)

for i in range(1,8):
	insert_sql='''INSERT INTO DAQS (id, channel_id,daq_value,daq_time) VALUES(null, {0},{1},{2});'''.format(i,10.5,int(time.time()))
	print(insert_sql)


	cursor.execute(insert_sql)


print("Table created successfully")

conn.commit()
conn.close()