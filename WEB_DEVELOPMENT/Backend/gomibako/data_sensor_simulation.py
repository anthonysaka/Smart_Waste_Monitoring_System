from server_app.connectiondb import Connectiondb
from server_app.methods import MethodsDatabase
import json, random
from datetime import datetime

def generated_data():
    Connectiondb.getConnectionToPostgre()

    device_eui = ['a84041000181eaec','a84041000181eaff','b84041000181eaff','b84041000181eaaa','b84041000181ebbb','b84041000181ebbc','60c5a8fffe798f87']
    device_name = ['BA000002',          'BA000003',          'BA000004',         'BA000005',    'BA000008',     'BA000009','BA000010']
    lim = 5.50
    code = 0
    for x in range(5):
        for i in range(len(device_name)):
            random.seed(datetime.now())
            temperature = round(random.uniform(32.00,40.00),2)
            humidity= round(random.uniform(40.00,70.00),2)
            lvlsingle = round(random.uniform(lim,95.00),2)
            volumen = round((((lvlsingle/100)*14.90)*(18.11)*(9.45)),2)
            lim = lvlsingle
            generated_date = datetime.now()
            if lvlsingle > 95:
                code = 2
            elif (lvlsingle >= 80 and lvlsingle <= 95):
                code = 1
            else:
                code = 0

            random_sensor_data = {'temperature':temperature,'humidity':humidity,'lvlsingle':lvlsingle,'volumen':volumen,'codeStatus':code}
            json_sensor_data = json.dumps(random_sensor_data,indent=4)

            if(MethodsDatabase.save_sensor_data(device_eui[i],device_name[i],json_sensor_data,datetime.now(),generated_date)):
                print("[*] Simulation Sensor Data Saved OK!\n")
            else:
                print("[*] Simulation Sensor Data Saved ERROR!\n")

if __name__ == "__main__":
    generated_data()