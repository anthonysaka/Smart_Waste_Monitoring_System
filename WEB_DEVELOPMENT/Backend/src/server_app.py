# Anthony Sakamoto - 00008614                                      
# PUCMM STI, RD - Degree Project - Telematic Engineering           
# TITLE: GOMIBAKO - SMART DUSTBIN, SMART GARBAGE MONITORING SYSTEM

from flask import Flask, jsonify, json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
import base64
import string
from decimal import Decimal
import time


app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "Access-Control-Allow-Origin": "*"
    }
})
app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app,cors_allowed_origins="*")

app.config['MQTT_BROKER_URL'] = '10.0.0.12'  # URL
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)

temp = 00.00
hum = 00.00
dist = 00.00

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('application/10/device/60c5a8fffe798f68/rx')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    me=json.loads(message.payload)
    me=me['data']
    base64_bytes = me.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    mes = message_bytes.decode('utf-8')
    temperature = round((Decimal(float(mes[0:4])/100.00)),2)
    humidity= round((Decimal(float(mes[4:8])/100.00)),2)
    distance1 = round(((Decimal(float(mes[8:12])/100.00))/24)*100,2)
    global temp, hum, dist
    temp = str(temperature)
    hum = str(humidity)
    dist = str(distance1)

    print("Temperature received " ,temperature)
    print("Humidity received " ,humidity)
    print("Distance1 received " ,distance1)
    print("*---------------*")
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
   # te = {'temperatura':temperature}
   #socketio.emit('mqtt_message', data=jsonify(te))


@app.route("/data")
def hello_world():
    d = {"temp":temp,"hum":hum,"dist":dist}
    print(d)
    return jsonify(d)


    

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
