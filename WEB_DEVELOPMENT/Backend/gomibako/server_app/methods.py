
from .connectiondb import Connectiondb
import psycopg2
from datetime import datetime

class MethodsDatabase:

    def save_sensor_data(deviceEui,devicename,data):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor()

            cur.execute('CALL saveSensorData(%s, %s, %s, %s)',(deviceEui,devicename,data,datetime.now()))

            conn.commit()
            cur.close()
            conn.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False