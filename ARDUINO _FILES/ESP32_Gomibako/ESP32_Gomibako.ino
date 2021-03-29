
/* ******************************************************************
 * Anthony Sakamoto - 00008614                                      *
 * PUCMM STI, RD - Degree Project - Telematic Engineering           *
 * TITLE: GOMIBAKO - SMART DUSTBIN, SMART GARBAGE MONITORING SYSTEM *
 * **************************************************************** */

/********** Libraries **********/
#include <HardwareSerial.h>
#include "DHT.h"
#include "RAK811.h"
#include <math.h>       
#include "ESP32Time.h"


/********** Defines Constants Sensors **********/
#define TRIG_PIN_0   18          // HC-SR04 trigger pin
#define ECHO_PIN_0   19          // HC-SR04 echo pin

#define TRIG_PIN_1   25          // HC-SR04 trigger pin
#define ECHO_PIN_1   26          // HC-SR04 echo pin

#define TRIG_PIN_2   32          // HC-SR04 trigger pin
#define ECHO_PIN_2   33          // HC-SR04 echo pin

#define DHT_PIN   5 // DHT-22 Temperature Sensor data pin
#define DHTTYPE DHT22

#define DebugSerial Serial

#define H  19// Altura del basurero en pulgadas.
#define h  15 // Altura del basurero en pulgadas.

/********** Defines Constants LoRa/LoRaWAN **********/
#define TX_TO_LORA_PIN 17
#define RX_TO_LORA_PIN 16
#define BAUD_RATE_LORA 115200
#define WORK_MODE LoRaWAN // LoRaWAN or LoRaP2P
#define JOIN_MODE OTAA  // OTAA or ABP

String const DevEui = "60c5a8fffe798f68"; // This values are unique for each node.
String const AppEui = "f3460654a76d7a36"; // This value isn't necessary for chirpstack lora server, but if for this end node.
String const AppKey = "ac3c4d337abf61032a1e6cbc616b6e04"; // This values are unique for each lora app. This appkey must be the same for all end node on gomibako app


/********** Aux Library Objects **********/
DHT tempSensor(DHT_PIN, DHTTYPE);
HardwareSerial uartRak(2);
RAK811 rak811LoRa(uartRak,DebugSerial);

/********** Function Prototypes **********/
bool InitLoRaWAN(void);
void setupRAK811Node(void);

/***** Global Variables ******/
char buffer[242];
String dataBackup[8];
int count=0;
int flag_count = 0;
int flag_data_to_send = 0;
ESP32Time rtc;

/********** BEGIN SETUP **********/
void setup()
{
  DebugSerial.begin(115200);
  uartRak.begin(BAUD_RATE_LORA, SERIAL_8N1, RX_TO_LORA_PIN, TX_TO_LORA_PIN);
  tempSensor.begin(); // Init Temperature Sensor DHT-22

  pinMode(TRIG_PIN_0, OUTPUT); //Trigger pin as output
  pinMode(ECHO_PIN_0, INPUT); //Echo pin as input
  pinMode(TRIG_PIN_1, OUTPUT); //Trigger pin as output
  pinMode(ECHO_PIN_1, INPUT); //Echo pin as input
  pinMode(TRIG_PIN_2, OUTPUT); //Trigger pin as output
  pinMode(ECHO_PIN_2, INPUT); //Echo pin as input

  setupRAK811Node();

  rtc.setTime(0, 16, 18, 26, 3, 2021);
  
 
  delay(2000); //Time to init the system
}

void loop()
{  
    float temperature = tempSensor.readTemperature(); // in Celsius
    float humidity = tempSensor.readHumidity(); // in percentage
    
    double lvlPlastic,lvlMetal,lvlPaperCarton = 0;
    int statusPlastic,statusMetal,statusPaperCarton,statusGeneral= 0;
    
    modf(read_level_median(TRIG_PIN_0,ECHO_PIN_0),&lvlPlastic); //inches int part
    delayMicroseconds(20);
    modf(read_level_median(TRIG_PIN_1,ECHO_PIN_1),&lvlMetal); //inches int part
    delayMicroseconds(20);
    modf(read_level_median(TRIG_PIN_2,ECHO_PIN_2),&lvlPaperCarton); //inches int part
    delayMicroseconds(20);

    //Conditions para evitar valores incoherentes negativos por medida mayor a la altura maxima.
    if(lvlPlastic > 19){
      lvlPlastic = 19;
    }
    if(lvlPlastic < 4){
      lvlPlastic = 4;
    }
    if(lvlMetal > 19){
      lvlMetal = 19;
    }
    if(lvlMetal < 4){
      lvlMetal = 4;
    }
    if(lvlPaperCarton > 19){
      lvlPaperCarton = 19;
    } 
    if(lvlPaperCarton < 4){
      lvlPaperCarton = 4;
    }      

    //Calculate percent of level
    int lvl_percent_Plastic = int(((H - lvlPlastic)/h)*100); 
    int lvl_percent_Metal = int(((H - lvlMetal)/h)*100);
    int lvl_percent_PaperCarton = int(((H - lvlPaperCarton)/h)*100);

    float volumen = (float)(((lvl_percent_Plastic/100.00)*14.90)*(18.11)*(9.45)) + (float)(((lvl_percent_Metal/100.00)*14.90)*(18.11)*(9.45)) + (float)(((lvl_percent_PaperCarton/100.00)*14.90)*(18.11)*(9.45));
    

    //Conditions to update status
    if (lvl_percent_Plastic >= 80 && lvl_percent_Plastic <= 95){
      statusPlastic = 1; //Full
    } else if (lvl_percent_Plastic > 95) {
      statusPlastic = 2; //Overflow
    } else {
      statusPlastic = 0; //Normal
    }

    if (lvl_percent_Metal >= 80 && lvl_percent_Metal <= 95){
      statusMetal = 1; //Full
    } else if (lvl_percent_Metal > 95) {
      statusMetal = 2; //Overflow
    } else {
      statusMetal = 0; //Normal
    }

    if (lvl_percent_PaperCarton >= 80 && lvl_percent_PaperCarton <= 95){
      statusPaperCarton = 1; //Full
    } else if (lvl_percent_PaperCarton > 95) {
      statusPaperCarton = 2; //Overflow
    } else {
      statusPaperCarton = 0; //Normal
    }

    if (statusPlastic == 2 || statusMetal == 2 || statusPaperCarton == 2){
      statusGeneral = 2;
    }
    if(statusPlastic == 1 || statusMetal == 1 || statusPaperCarton == 1){
      statusGeneral = 1;
    }

    
    DebugSerial.println(statusPlastic);
    DebugSerial.println(lvl_percent_Plastic);
    DebugSerial.println(statusMetal);
    DebugSerial.println(lvl_percent_Metal);
    DebugSerial.println(statusPaperCarton);
    DebugSerial.println(lvl_percent_PaperCarton);
    DebugSerial.println(statusGeneral);
    
    DebugSerial.println(temperature);
    DebugSerial.println(humidity);
    DebugSerial.println(volumen);
    DebugSerial.println("--------------\n");
    char dateS[30];
    rtc.getTimeDate().toCharArray(dateS,30);
    DebugSerial.println(dateS);

    //Load on variable buffer formatted sensor data(Strings)
    sprintf(buffer,"%04d%04d%02d%02d%02d%01d%01d%01d%01d%06d",(int)(temperature*100),(int)(humidity*100),lvl_percent_Plastic,lvl_percent_Metal,lvl_percent_PaperCarton,statusPlastic,statusMetal,statusPaperCarton,statusGeneral,(int)(volumen*100));
      strcat(buffer,dateS);
    //Encode Buffer in HexString
    int len = strlen(buffer);
  
    char hex_str[(len*2)+1];
    convert_hexa(buffer, hex_str);
  
   
    printf("UTF-8: %s\n", buffer);
    printf("Hexadecimal: %s\n", hex_str);
   


    //Send Data to LoRa Gateway  
    if (rak811LoRa.rk_sendData(1, hex_str)){  
        delay(500);
        String ret = rak811LoRa.rk_recvData();
        if(ret != NULL){ 
          DebugSerial.println(ret);
          DebugSerial.println("ACK RECIBIDO!");

          if (flag_data_to_send == 1) {
           
              if(dataBackup[flag_count] != NULL){
                 char aux[(len*2)+7];
                 dataBackup[flag_count].toCharArray(aux,(len*2)+7);
                 
                 if(rak811LoRa.rk_sendData(2, aux)){
                    delay(500);
                     DebugSerial.println("TRYING SEND LOG DATA");
                    String ret = rak811LoRa.rk_recvData();
                    
                    if(ret != NULL){ 
                      DebugSerial.println(ret);
                      printf("ACK RECIBIDO! - DATA LOG [%d] OK!\n",flag_count);
                      printf("LOG DATA: %s\n\n", aux);
                    }
                 }
              }
              flag_count++;
              
              if(flag_count == count){
                 flag_data_to_send = 0; 
                 count=0;
                 flag_count=0;
            } 
         
          }
        } else {
          DebugSerial.println("ACK NO RECIBIDO!");
          DebugSerial.println("SAVING DATA TO SEND LATER");
          char x [] = {"4C4F47"};
          strcat(hex_str,x);
          dataBackup[count]= hex_str;
          DebugSerial.println(dataBackup[count]);
          count++;
          DebugSerial.println("DATA SAVED TO SEND LATER");
          flag_data_to_send = 1;          
        }
    }

  delay(30000);
  
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

  if(!rak811LoRa.rk_isConfirm(1))  //set LoRa data send package type:0->unconfirm, 1->confirm
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
float readDistance(int TRIG_PIN, int ECHO_PIN){
    float duration = 0.00;
    digitalWrite(ECHO_PIN, LOW);   // set the echo pin LOW
    digitalWrite(TRIG_PIN, HIGH);  // set the trigger pin HIGH for 10μs
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW); // set the trigger pin LOW
    duration = pulseIn(ECHO_PIN, HIGH);  // measure the echo time (μs)
    return float(duration/2/74);   // convert echo time to distance (inches)
}

float read_level_median(int TRIG_PIN, int ECHO_PIN){
  float sum_measure = 0.00;
  for (int i = 0; i<20; i++){
      sum_measure += readDistance(TRIG_PIN,ECHO_PIN); // in Inches  
      delay(10);
    }
    return (sum_measure/20);
}

// Use to test serial communication between esp32 and lora module.
/*
   if(uartRak.available()){
    DebugSerial.write(uartRak.read());
   }
   if(DebugSerial.available()){
    uartRak.write(DebugSerial.read());
  }
*/

  
