
from .connectiondb import Connectiondb
import psycopg2
import psycopg2.extras
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

    def add_company(rnc, name, provi, address, coordinates):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor()

            cur.execute('CALL addClientCompany(%s, %s, %s, %s, %s, %s)',(rnc,name,provi,address,coordinates, datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    
    def get_list_company():
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('SELECT * FROM public.clientCompany;')
            result = cur.fetchall()

            if not result:
                result = None
        
            conn.commit()
            cur.close()
            conn.close()
            return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    
    def add_user(username,email,password,firstname,lastname,typeU,rncComp):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor()

            cur.execute('CALL addUser(%s, %s, %s, %s, %s, %s, %s, %s, %s)',(username,email,password,firstname,lastname,typeU,rncComp,True,datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    
    def get_specific_user(username):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('SELECT * FROM public.user WHERE username = %s;',(str(username),))
            result = cur.fetchall()

            if not result:
                result = None
        
            conn.commit()
            cur.close()
            conn.close()
            return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def add_dustbin(deviceEui,typeD,descrip,rncComp,mWaste,coordinates):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor()

            cur.execute('CALL addDustbin(%s, %s, %s, %s, %s,%s, %s)',(deviceEui,typeD,descrip,rncComp,mWaste,coordinates,datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def get_company_list_dustbin(rncComp):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('SELECT * FROM public.dustbin WHERE rnc_org = %s ORDER BY id ASC;',(rncComp,))
            result = cur.fetchall()
            if not result:
                result = None
        
            conn.commit()
            cur.close()
            conn.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def get_specific_last_dustbin_data(namebin):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('SELECT data_sensor, created_date FROM public.dustbindata WHERE device_name = %s ORDER BY created_date DESC;',(namebin,))
            result = cur.fetchone()

            if not result:
                result = None
        
            conn.commit()
            cur.close()
            conn.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def get_specific_all_dustbin_data(namebin):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('SELECT data_sensor, created_date FROM public.dustbindata WHERE device_name = %s ORDER BY created_date ASC',(namebin,))
            result = cur.fetchone()

            if not result:
                result = None
        
            conn.commit()
            cur.close()
            conn.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False



    def check_login(username,password):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('SELECT * FROM public.user WHERE username = %s AND password = crypt(%s,password);',(str(username),str(password)))
           
            result = cur.fetchall()

            if not result:
                result = None
           
            conn.commit()
            cur.close()
            conn.close()
            return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    
    def modidy_default_credentials(uid,username,password):
        try:
            conn = Connectiondb.getConnectionToPostgre()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('UPDATE public.user SET username = %s, password = crypt(%s,password),default_credentials = false WHERE id = %s;',(str(username),str(password),uid))
            
            conn.commit()
            cur.close()
            conn.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        

