import sqlite3
from sqlite3 import Error
from DatabaseConnection.dbParams import *
from NRF24L01.IdentifierFrame import Group

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def getLastCurrentData(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM IoT_Serwer_currentstatedata ORDER BY id DESC LIMIT 1")
    rows = cur.fetchone()

    return CurrentData(rows[1], rows[2], rows[3], rows[4], rows[5], rows[6])

#def getLastSensor(conn,group: Group):

#def updateSensors(conn,deviceID,date,measure):

# TODO: ErrorLOG


# database = 'H:\\PycharmProjects\\Projekt_Zespolowy\\db.sqlite3'
# conn = create_connection(database)
# with conn:
#     a = getLastSensor()
#     print(a)




''' Databases:
IoT_Serwer_color
IoT_Serwer_currentstatedata
IoT_Serwer_device
Iot_Serwer_errordata
IoT_Serwer_sensor
'''