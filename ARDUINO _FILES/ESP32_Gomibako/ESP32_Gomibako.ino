
/* ******************************************************************
 * Anthony Sakamoto - 00008614                                      *
 * PUCMM STI, RD - Degree Project - Telematic Engineering           *
 * TITLE: GOMIBAKO - SMART DUSTBIN, SMART GARBAGE MONITORING SYSTEM *
 * **************************************************************** */

/********** Libraries **********/
#include <HardwareSerial.h>
#include "TinyGPS++.h"
#include "DHT.h"
#include "RAK811.h"
//#include <stdio.h>
//#include <stdint.h>
//#include <stdlib.h>

/********** Defines Constants Sensors **********/
#define TRIG_PIN   18          // HC-SR04 trigger pin
#define ECHO_PIN   19          // HC-SR04 echo pin
/*
#define TX_GPS_PIN 17
#define RX_GPS_PIN 16
#define BAUD_RATE_GPS 115200
*/
#define   DHT_PIN   5 // DHT-22 Temperature Sensor data pin
#define DHTTYPE DHT22
#define DebugSerial Serial

/********** Defines Constants LoRa/LoRaWAN **********/
#define TX_TO_LORA_PIN 17
#define RX_TO_LORA_PIN 16
#define BAUD_RATE_LORA 115200
#define WORK_MODE LoRaWAN // LoRaWAN or LoRaP2P
#define JOIN_MODE OTAA  // OTAA or ABP

String const DevEui = "60c5a8fffe798f68"; // This values are unique for each node.
String const AppEui = "f3460654a76d7a36";
String const AppKey = "ac3c4d337abf61032a1e6cbc616b6e04"; // This values are unique for each lora app.


/********** Aux Library Objects **********/
/*HardwareSerial uartGps(2);
TinyGPSPlus gps; */
DHT tempSensor(DHT_PIN, DHTTYPE);
HardwareSerial uartRak(2);
RAK811 rak811LoRa(uartRak,DebugSerial);

/********** Function Prototypes **********/
bool InitLoRaWAN(void);
void setupRAK811Node(void);

/********** BEGIN SETUP **********/
void setup()
{
  DebugSerial.begin(115200);
  uartRak.begin(BAUD_RATE_LORA, SERIAL_8N1, RX_TO_LORA_PIN, TX_TO_LORA_PIN);
  setupRAK811Node();
  
  tempSensor.begin(); // Init Temperature Sensor DHT-22
  //uartGps.begin(BAUD_RATE_GPS, SERIAL_8N1, RX_GPS_PIN, TX_GPS_PIN); //Init Serial GPS
  
  pinMode(TRIG_PIN, OUTPUT); //Trigger pin as output
  pinMode(ECHO_PIN, INPUT); //Echo pin as input

  delay(2000); //Time to init the system
}

/***** Global Variables ******/
float distance1 = 0.00;
float temperature = 0.00;
float humidity = 0.00;
float heatIndex = 0.00;
char buffer[242];

void loop()
{  
   // readGPS();
   
    distance1 = readDistance(); // in Inches
    temperature = tempSensor.readTemperature(); // in Celsius
    humidity = tempSensor.readHumidity(); // in percentage


    DebugSerial.println(distance1);
    DebugSerial.println(temperature);
    DebugSerial.println(humidity);
    DebugSerial.println("--------------\n");

    //Load on variable buffer formatted sensor data(Strings)
   // sprintf(buffer,"%04d",(int)(distance*100));
   // sprintf(buffer,"%s",":");
    sprintf(buffer,"%04d%04d%04d",(int)(temperature*100),(int)(humidity*100),(int)(distance1*100));
      
    //Encode Buffer in HexString
    int len = strlen(buffer);
    char hex_str[(len*2)+1];
    convert_hexa(buffer, hex_str);
   
    printf("UTF-8: %s\n", buffer);
    printf("Hexadecimal: %s\n", hex_str);

    //Wakeup RAK811 from sleep mode
   // rak811LoRa.rk_sleep(0);  
    //delay(1000);

    //Send Data to LoRa Gateway  
    if (rak811LoRa.rk_sendData(1, hex_str)){    
        String ret = rak811LoRa.rk_recvData();
        if(ret != NULL){ 
          DebugSerial.println(ret);
        }
    //    rak811LoRa.rk_sleep(1);  //Set RAK811 enter sleep mode
        delay(3000);  //10 seconds to repeat  measurements again    
    }
   
} //End Infinity Loop


/****************** FUNCTIONS ***********************/
bool InitLoRaWAN(void)
{
  if(rak811LoRa.rk_setJoinMode(JOIN_MODE))  //set join_mode:OTAA
  {
    if(rak811LoRa.rk_setRegion(8))  //set region EU868
    {
      if (rak811LoRa.rk_initOTAA(DevEui, AppEui, AppKey))
      {
        DebugSerial.println(F("RAK811 init OK!"));  
        return true;    
      }
    }
  }
  return false;
}

void setupRAK811Node(){
  rak811LoRa.rk_getVersion();  //get RAK811 firmware version
  DebugSerial.println(rak811LoRa.rk_recvData());  //print version number

  DebugSerial.println(F("Start init RAK811 parameters..."));
 
  if (!InitLoRaWAN())  //init LoRaWAN
  {
    DebugSerial.println(F("Init error,please reset module.")); 
    while(1);
  }

  DebugSerial.println(F("Start to join LoRaWAN..."));
  while(!rak811LoRa.rk_joinLoRaNetwork(60))  //Joining LoRaNetwork timeout 60s
  {
    DebugSerial.println();
    DebugSerial.println(F("Rejoin again after 5s..."));
    delay(5000);
  }
  DebugSerial.println(F("Join LoRaWAN success"));

  if(!rak811LoRa.rk_isConfirm(0))  //set LoRa data send package type:0->unconfirm, 1->confirm
  {
    DebugSerial.println(F("LoRa data send package set error,please reset module.")); 
    while(1);    
  }
}

//Convert string to hexadecimal(HexString Format)
void convert_hexa(char* input, char* output){
   int loop=0;
   int i=0;
   while(input[loop] != '\0'){
      sprintf((char*)(output+i),"%02X", input[loop]);
      loop+=1;
      i+=2;
   }
   //marking the end of the string
   output[i++] = '\0';
}

//Return distance in Inches
float readDistance(){
    float duration = 0.00;
    digitalWrite(ECHO_PIN, LOW);   // set the echo pin LOW
    digitalWrite(TRIG_PIN, HIGH);  // set the trigger pin HIGH for 10μs
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW); // set the trigger pin LOW
    duration = pulseIn(ECHO_PIN, HIGH);  // measure the echo time (μs)
    return (duration/74/2);   // convert echo time to distance (inches)
}

/*
void readGPS(){
 while (uartGps.available() > 0){
    gps.encode(uartGps.read());
    if (gps.location.isUpdated()){
      Serial.print("Latitude= "); 
      Serial.print(gps.location.lat(), 6);
      Serial.print(" Longitude= "); 
      Serial.println(gps.location.lng(), 6);
      uartGps.flush();
    }
 } 
}    
*/

/*
   if(uartRak.available()){
    DebugSerial.write(uartRak.read());
   }
   if(DebugSerial.available()){
    uartRak.write(DebugSerial.read());
  }
*/

  
