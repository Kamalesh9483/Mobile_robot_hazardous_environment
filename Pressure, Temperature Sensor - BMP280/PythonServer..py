
import json
import socket
import sqlite3

# sql object
con = sqlite3.connect('C:\Projects\Mobile robot in hazardous environment\Pressure, Temperature Sensor - BMP280\Temperature_Pressure.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE sensorValues
               (temp REAL, pres REAL);''')

# Ax = 0.0
UDP_IP = "0.0.0.0"
UDP_PORT = 8090

sock = socket.socket(socket.AF_INET, # Interne
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


while True:
    data , addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data = json.loads(data)
    print(data["temperature"],data["pressure"])
    cur.execute("INSERT INTO sensorValues VALUES (?,?)", (data["temperature"],data["pressure"]))
    #   Save (commit) the changes
    con.commit()
   
con.close()
    