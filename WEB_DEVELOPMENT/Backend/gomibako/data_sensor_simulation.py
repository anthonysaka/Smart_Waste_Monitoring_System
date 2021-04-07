from server_app.connectiondb import Connectiondb
from server_app.methods import MethodsDatabase
import json, random
from datetime import datetime
import paho.mqtt.client as mqtt #import the client1
import time

def send_data_mqtt():
    broker_address="10.0.0.12" 
    client = mqtt.Client("P1") #create new instance
  
    #device_eui = ['a84041000181eaec','a84041000181eaff','b84041000181eaff','b84041000181eaaa','b84041000181ebbb','b84041000181ebbc','60c5a8fffe798f87']
    #device_name = ['BA000002',          'BA000003',          'BA000004',         'BA000005',    'BA000008',     'BA000009','BA000010']
    device_eui = ['a84041000181eaec']
    device_name = ['BA000002']
    
    lim = 5.50
    code = 0
    while True:
        client.connect(broker_address) #connect to broker
        for x in range(1):
            for i in range(len(device_name)):
                random.seed(datetime.now())
                temperature = round(random.uniform(32.00,40.00),2)
                humidity= round(random.uniform(40.00,70.00),2)
                batteryLevel = round(100.00,2)
                lvlsingle = round(random.uniform(lim,99.00),2)
                volumen = round((((lvlsingle/100)*14.90)*(18.11)*(9.45)),2)
                lim = lvlsingle
                generated_date = datetime.now()
                if lvlsingle > 95:
                    code = 2
                elif (lvlsingle >= 80 and lvlsingle <= 95):
                    code = 1
                else:
                    code = 0

                random_sensor_data = {'devEUI':device_eui[i],'deviceName':device_name[i],'object':{'temperature':temperature,'humidity':humidity,'batteryLevel':batteryLevel,'lvlsingle':lvlsingle,'volumen':volumen,'codeStatus':code,'nodeDate':generated_date}}
                json_sensor_data = json.dumps(random_sensor_data,indent=4,default=str)

                if(client.publish("application/11/device/"+device_name[i]+"/rx",json_sensor_data)):
                    print("[*] Simulation Sensor Data Saved OK!\n")
                else:
                    print("[*] Simulation Sensor Data Saved ERROR!\n")
        
        client.disconnect()
        time.sleep(30.00)

def generated_data():
    Connectiondb.getConnectionToPostgre()

    device_eui = ['a84041000181eaec','a84041000181eaff','b84041000181eaff','b84041000181eaaa','b84041000181ebbb','b84041000181ebbc','60c5a8fffe798f87']
    device_name = ['BA000002',          'BA000003',          'BA000004',         'BA000005',    'BA000008',     'BA000009','BA000010']
    lim = 5.50
    code = 0
    for x in range(3):
        for i in range(len(device_name)-3):
            random.seed(datetime.now())
            temperature = round(random.uniform(32.00,40.00),2)
            humidity= round(random.uniform(40.00,70.00),2)
            lvlsingle = round(random.uniform(lim,75.00),2)
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
   # generated_data()
   send_data_mqtt()