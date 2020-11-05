
#! ################################################################# # 
#! Anthony Sakamoto - 00008614                                       #
#! PUCMM STI, RD - Degree Project - Telematic Engineering            #
#! TITLE: GOMIBAKO - SMART DUSTBIN, SMART GARBAGE MONITORING SYSTEM  #
#! ################################################################# # 

#! System Web Application
 
from flask import Flask, jsonify, json
from flask_mqtt import Mqtt
from flask_cors import CORS
import base64

import string
from decimal import Decimal
import time
from .connectiondb import Connectiondb
from .methods import MethodsDatabase


app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "Access-Control-Allow-Origin": "*"
    }
})

#! MQTT Configurations
app.config['MQTT_BROKER_URL'] = '10.0.0.12'  # Ip addres of broker server
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

time.sleep(2)
mqtt = Mqtt(app)

if(mqtt):
    print("[*] MQTT Connected OK!")
    mqtt.subscribe('application/10/device/+/rx')
    print("[*] MQTT Suscribed to application/10/device/+/rx OK!\n\n")


#! MQTT Callback Function. When a new message arrives, this
#! data is stored in the database table (public.dustbinData)
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    dict_data=json.loads(message.payload)

    device_eui = str(dict_data['devEUI'])
    device_name = str(dict_data['deviceName'])
    json_sensor_data = json.dumps(dict_data['object'],indent=4)

    if(MethodsDatabase.save_sensor_data(device_eui,device_name,json_sensor_data)):
        print("[*] Sensor Data Saved OK!\n")
    else:
        print("[*] Sensor Data Saved ERROR!\n")


#! ***************************************************
    