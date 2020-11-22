
#! ################################################################# # 
#! Anthony Sakamoto - 00008614                                       #
#! PUCMM STI, RD - Degree Project - Telematic Engineering            #
#! TITLE: GOMIBAKO - SMART DUSTBIN, SMART GARBAGE MONITORING SYSTEM  #
#! ################################################################# # 

#! System Web Application
 
from flask import Flask, jsonify, json, request, abort
from flask_mqtt import Mqtt
from flask_cors import CORS
from flask_mail import Mail, Message
import string, time, random, requests
import jwt
import datetime
from .connectiondb import Connectiondb
from .methods import MethodsDatabase
from .smart_routes import *

app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "Access-Control-Allow-Origin": "*"
    }
})
app.config['SECRET_KEY'] = '20f750e72db564f664f2ab90c1df4d5a'
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'anthonysk2017@gmail.com'
app.config['MAIL_PASSWORD'] = 'semeolvido1999'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

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
    mqtt.subscribe('application/11/device/+/rx')
    print("[*] MQTT Suscribed to application/11/device/+/rx OK!\n\n")


#! MQTT Callback Function. When a new message arrives, this
#! data is stored in the database table (public.dustbinData)
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    dict_data=json.loads(message.payload)

    device_eui = str(dict_data['devEUI'])
    device_name = str(dict_data['deviceName'])
    json_sensor_data = json.dumps(dict_data['object'],indent=4)

    if(MethodsDatabase.save_sensor_data(device_eui,device_name,json_sensor_data,datetime.now())):
        print("[*] Sensor Data Saved OK!\n")
    else:
        print("[*] Sensor Data Saved ERROR!\n")


#! ***************************************************


@app.route("/gomibako/internalapi/1.0/clientCompany/<int:loadtype>",methods=['POST','GET'])
def api_client_company(loadtype):
    if request.method == 'POST':
    
        rnc = request.json['rnc']
        name = request.json['name']
        provi = request.json['provincia']
        address = request.json['address']
        coordinates = request.json['coordinates']

        if(MethodsDatabase.add_company(rnc,name,provi,address,coordinates)):
            return jsonify({'code':201,'response':'Registrado con exito'}),201
        else:
            abort(500,description="Error en la base de datos")

    elif request.method == 'GET' and loadtype == 0:

        listcompanies = MethodsDatabase.get_list_company()
        if listcompanies is not None:
            return jsonify(listcompanies),201
        elif listcompanies is None:
            return jsonify({'code':404,'response':'No hay empresas registradas!'}),404
        else:
            abort(500,description="Error en la base de datos")
    
    elif request.method == 'GET' and loadtype == 1:
        rncComp = request.args.get('rncComp')
        companies = MethodsDatabase.get_company(rncComp)
        if companies is not None:
            return jsonify(companies),201
        elif companies is None:
            return jsonify({'code':404,'response':'No hay empresa registrada con este rnc'}),404
        else:
            abort(500,description="Error en la base de datos")
    

def generator_random_default_user_password():
    LETTERS = string.ascii_letters
    NUMBERS = string.digits  
    PUNCTUATION = string.punctuation
    LENGTH = int(12)

    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_password = random.choices(printable, k=LENGTH)
    random_password = ''.join(random_password)
    return random_password

def generator_random_default_username(firstname,lastname):
    LETTERS = firstname+lastname
    NUMBERS = string.digits  
    LENGTH = int(8)

    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_username = random.choices(printable, k=LENGTH)
    random_username = ''.join(random_username)
    return random_username

@app.route("/gomibako/internalapi/1.0/user",methods=['POST','GET'])
def api_user():
    if request.method == 'POST':    
        email = request.json['email']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        typeU = "cliente"
        rncComp = request.json['rncComp']

        username = str(generator_random_default_username(firstname,lastname))
        print(username)
        password = str(generator_random_default_user_password())
        print(password)

        if(MethodsDatabase.add_user(username,email,password,firstname,lastname,typeU,rncComp)):
            msg = Message('GOMIBAKO TEAM - Credentials', sender = 'anthonysk2017@gmail.com', recipients = [str(email)])
            msg.body = "Hey, este es tu usuario y contrasena por defecto:\n     " +"Usuario: "+username+"\n     "+password + "\nCuando inicie sesion por primera vez, tendra que cambiar el usuario y contrasena.\nSaludos,\nGOMIBAKO TEAM"
            mail.send(msg)
            
            return jsonify({'code':201,'response':"Registrado con exito, usuario y contrasena enviado al emai.",'firstname':firstname, 
                            'lastname':lastname,'email':email}),201
        else:
            abort(500,description="Error en la base de datos")

@app.route("/gomibako/internalapi/1.0/dustbin/<int:loadtype>",methods=['POST','GET'])
def api_dustbin(loadtype):
    if request.method == 'POST' and loadtype == 0:
        deviceEui = request.json['deviceEui']
        rncComp = request.json['rncComp']
        typeD = request.json['type']
        descrip = request.json['descrip']
        mWaste = request.json['mWaste']
        coordinates = request.json['coordinates']
        print(request.json)

        if(MethodsDatabase.add_dustbin(deviceEui,typeD,descrip,rncComp,mWaste,coordinates)):

            if typeD == 'Reciclaje - 3 contenedores (plastico/metal/papel-carton)':
                name = MethodsDatabase.get_company_list_dustbin(rncComp)[0]['name']
                url0 = 'http://10.0.0.12:8080/api/devices'
                url1 = 'http://10.0.0.12:8080/api/devices/'+deviceEui+'/keys'
                myobj0 = {"device": {
                                            "applicationID": "11",
                                            "description": descrip,
                                            "devEUI": deviceEui,
                                            "deviceProfileID": "70298761-1bf9-4a6c-bda1-69a0eb04aaaf",
                                            "isDisabled": False,
                                            "name": name,
                                            "referenceAltitude": 0,
                                            "skipFCntCheck": False,
                                            "tags": {"type":typeD,"materialWaste":mWaste,"rncOrg":rncComp},
                                            "variables": {}
                                            }
                                }
                myobj1 = {"deviceKeys": {
                                        "appKey": "ac3c4d337abf61032a1e6cbc616b6e04",
                                        "devEUI": deviceEui,
                                        "genAppKey": "00000000000000000000000000000000",
                                        "nwkKey": "ac3c4d337abf61032a1e6cbc616b6e04"
                                    }
                            }
                x = requests.post(url0, json = myobj0,headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiMThhNzg1MWUtMzc5MC00MmMxLWIzZjktNTlmZGM1MmRlMWMzIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTYwNDc3NDk5MSwic3ViIjoiYXBpX2tleSJ9.W5oHTfHM4yFGyknrzFLqzdDi2piIKX-NJsNfpVOy0Gk'})    
                y = requests.post(url1, json = myobj1,headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiMThhNzg1MWUtMzc5MC00MmMxLWIzZjktNTlmZGM1MmRlMWMzIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTYwNDc3NDk5MSwic3ViIjoiYXBpX2tleSJ9.W5oHTfHM4yFGyknrzFLqzdDi2piIKX-NJsNfpVOy0Gk'})
                
            return jsonify({'code':201,'response':"Registrado con exito",'deviceEui':deviceEui}),201
        else:
            abort(500,description="Error en la base de datos")
    elif request.method == 'GET' and loadtype == 1:
        rncComp = request.args.get('rncComp')
        listbinscompany = MethodsDatabase.get_company_list_dustbin(rncComp)
        
        if listbinscompany is not None:
            return jsonify(listbinscompany),200
        elif listbinscompany is None:
            return jsonify({'code':404,'response':'No hay basureros registrados!'}),404
        else:
            abort(500,description="Error en la base de datos")

@app.route("/gomibako/internalapi/1.0/bindata/<int:typeget>",methods=['GET'])
def api_dustbin_data(typeget):
    if request.method == 'GET' and typeget == 0:
        namebin = request.args.get('namebin')
        data = MethodsDatabase.get_specific_last_dustbin_data(namebin)

        if data is not None:
            return jsonify(data),200
        elif data is None:
            return jsonify({'code':404,'response':'No hay datos registrados!'}),404
        else:
            abort(500,description="Error en la base de datos")
    elif request.method == 'GET' and typeget == 1:
        namebin = request.args.get('namebin')
        print(namebin)
        data_all = MethodsDatabase.get_specific_all_dustbin_data(namebin)
        #print(data_all)

        if data_all is not None:
            return jsonify(data_all),200
        elif data_all is None:
            return jsonify({'code':404,'response':'No hay datos registrados!'}),404
        else:
            abort(500,description="Error en la base de datos")        

@app.route("/gomibako/internalapi/1.0/login",methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        userObject = MethodsDatabase.check_login(username,password)

        if(userObject is not None):
            token = jwt.encode({'user':username,'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=28800)},app.config['SECRET_KEY'])
            return jsonify({'code':200,'response':"Autentificacion con exito",'token':token.decode('utf-8'),'user':userObject}),200
        elif userObject is None:
            print("ENTRE")
            return jsonify({'code':404,'response':'Username or password incorrect!'}),404
        else:
            abort(500,description="Error en la base de datos")

@app.route("/gomibako/internalapi/1.0/changecredentials",methods=['PUT'])
def modify_default_credentials():

    if request.method == 'PUT':
        uid = request.json['id']
        newusername = request.json['newusername']
        newpassword = request.json['newpassword']

        dbResponse = MethodsDatabase.get_specific_user(newusername)

        if(dbResponse is None):

            if(MethodsDatabase.modidy_default_credentials(uid,newusername,newpassword)):
                userObject = MethodsDatabase.get_specific_user(newusername)
                return jsonify({'code':201,'response':"Modificaciones realizadas con exito",'user':userObject}),201
            else:
                abort(500,description="Error en la base de datos")
        elif dbResponse is not None:
            return jsonify({'code':404,'response':'El usuario ya existe!'}),404
        else:
            abort(500,description="Error en la base de datos")

        
@app.route("/gomibako/internalapi/1.0/truck",methods=['POST','GET'])
def api_truck():
    if request.method == 'POST':
        placa = request.json['placa']
        ano = request.json['ano']
        marca = request.json['marca']
        modelo = request.json['modelo']
        cap_carga_kg = request.json['cap_kg']
        cap_carga_vol = request.json['cap_vol']
        rncCompa = request.json['rncCompa']
        
        if(MethodsDatabase.add_truck(placa,ano,marca,modelo,cap_carga_kg,cap_carga_vol,rncCompa)):
            return jsonify({'code':201,'response':'Registrado con exito'}),201
        else:
            abort(500,description="Error en la base de datos")
    elif request.method == 'GET':
        rncComp = request.args.get('rncComp')
        listtruckcompany = MethodsDatabase.get_company_list_truck(rncComp)
        
        if listtruckcompany is not None:
            return jsonify(listtruckcompany),200
        elif listtruckcompany is None:
            return jsonify({'code':404,'response':'No hay camiones registrados!'}),404
        else:
            abort(500,description="Error en la base de datos")

@app.route("/gomibako/internalapi/1.0/smartroutes",methods=['GET'])
def get_smart_routes():
    if request.method == 'GET':
    
        distance_matrix = json.loads(request.args.get('distanceMatrix'))
        demands = json.loads(request.args.get('volDemands'))
        truck_capacities = json.loads(request.args.get('truckCapacities'))
        cant_truck = request.args.get('cantTruck')

        for x in range(len(demands)):
            demands[x] = int(demands[x])
        for x in range(len(truck_capacities)):
            truck_capacities[x] = int(truck_capacities[x])

        solution = generate_smart_routes(distance_matrix,demands,truck_capacities,cant_truck)
        return jsonify({'code':201,'solution':solution}),201
        

