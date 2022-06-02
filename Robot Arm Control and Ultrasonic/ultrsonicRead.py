# create http get endpoint to get distance from ultrasonic sensor using flask
from flask import Flask
from flask import request
import sys
import csv
import sqlite3

# create sqlite3 database
db = sqlite3.connect('./ultrasonicRead.db')

# create table name as UltrasonicData with columns for distance and time and Date
db.execute('''CREATE TABLE IF NOT EXISTS UltrasonicData
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            distance INTEGER,
            time TEXT)''')







# create flask app
app=Flask(__name__)
#create get end point
@app.route('/update_distance')
def update_distance():
    #get ultrasonic distance argument 
    ultrasonicDistance=request.args.get('ultrasonicDistance')
    
    dataBase = sqlite3.connect('./ultrasonicRead.db')
    #write to db
    dataBase.execute('INSERT INTO UltrasonicData (distance, time) VALUES (?, datetime("now"))', (ultrasonicDistance,))
    dataBase.commit()
    dataBase.close()
    
     
        
        
    return "200"
        
        

if __name__ == '__main__':
   
    app.run(host='0.0.0.0', debug = True, port=1880)
    