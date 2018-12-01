import sqlite3


conn = sqlite3.connect('daq.db', timeout=5)
print("Opened database successfully")

cursor = conn.cursor()


cursor.execute('''CREATE TABLE CHANNELS
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
		channel_name TEXT,
		pmax FLOAT,
		pmin FLOAT,
		high_limit FLOAT,
		low_limit FLOAT,
		unit TEXT);''')


cursor.execute('''CREATE TABLE DAQS
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
	    channel_id INTEGER,
	    daq_value FLOAT,
		daq_time INTEGER,
	    FOREIGN KEY (channel_id)  
	    REFERENCES channels(id)
);''')


cursor.execute('''CREATE TABLE ALARM
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
	    channel_id INTEGER,
	    alarm_status INTEGER,
	    alarm_msg_type INTEGER,
		alarm_time INTEGER,
	    FOREIGN KEY (channel_id)  
	    REFERENCES channels(id)
);''')

print("Table created successfully")

conn.commit()
conn.close()