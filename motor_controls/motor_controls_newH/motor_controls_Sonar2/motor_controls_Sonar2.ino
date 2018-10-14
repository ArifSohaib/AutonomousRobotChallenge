//#include <Wire.h> 
//#include <Servo.h>
//#include <LiquidCrystal_I2C.h>
//LiquidCrystal_I2C lcd(0x27,2,1,0,4,5,6,7);  // Set the LCD I2C address
// Analog Pin A4 SDA - Data UltraSonicDistanceSensor
// Analog Pin A5 SCL - Clock (Edge Pin)
/*
 * Filename: Bluetooth.ino
 * Source: https://www.youtube.com/watch?v=fJvtMszk2G4
 * Date: March 2, 2017
*/
#include <NewPing.h>
#define trig_front 13
#define echo_front 12
#define trig_back 4
#define echo_back 2
char c;
char recievedChar;
boolean newData = false;
//SoftwareSerial mySerial(10,11);
// Reading 4x4 Keypad with ONE Arduino Pin
// by Hari Wiguna, 2016
// Source: https://www.youtube.com/watch?v=G14tREsVqz0&t=325s
// Check schematics and resistors placement.

//int Xdir = 0;
//int Ydir = 0;
//(ADC pin 14);

int LEFT_FORWARD = 6;
int LEFT_REVERSE = 5;
int RIGHT_FORWARD = 10;
int RIGHT_REVERSE = 9;
int spd = 150;
int spdT = 150;
int dly = 100;
int dlyP = 40;
int dlyT = 80;
int READ_RF = A1;
int READ_RR = A2;
int READ_LF = A4;
int READ_LR = A5;
int thresh = 60;
NewPing sonar_front(trig_front, echo_front,250);
NewPing sonar_back(trig_back, echo_back,250);

//define sonar distance variables
long duration;
int distance;
float dist_front;
float dist_back;

// Information on L298N and PWM control
// PWM ranges from 0 to 255. Pins D6 & D9 are used here.  Use analogWrite(6,255) for PWM.
//http://tronixstuff.com/2014/11/25/tutorial-l298n-dual-motor-controller-modules-and-arduino/
void setup()
{ 
  
  pinMode(LEFT_FORWARD,OUTPUT); 
  pinMode(LEFT_REVERSE,OUTPUT); 
  pinMode(RIGHT_FORWARD,OUTPUT);
  pinMode(RIGHT_REVERSE,OUTPUT);
  pinMode(READ_RF, INPUT);
  pinMode(READ_RR, INPUT);
  pinMode(READ_LF, INPUT);
  pinMode(READ_LR, INPUT);
  Serial.begin(9600);
  
//  mySerial.begin(9600);
  //Serial.println("Testing Bluetooth.  Sync with Android Bluetooth now.");
}

unsigned long timestamp1;
unsigned long timestamp2;
bool movingForward = false;
bool movingReverse = false;
void loop()
{ 
  timestamp1=millis();
  dist_front = sonar_front.ping_cm();
  dist_back = sonar_back.ping_cm();
  timestamp2=millis();

  Serial.print("dist_front "); Serial.print(dist_front); Serial.print(", dist_back: "); Serial.print(dist_back);
  Serial.print(" Total time: "); Serial.print( (timestamp2-timestamp1) );
  Serial.println("");
  
  if((((dist_front != 0) ||  (dist_front < thresh)) & movingForward) || (((dist_back != 0) ||  (dist_back < thresh)) & movingReverse)){
      
    PAUSE(spd, dlyP);
    Serial.print("distance:  "); Serial.print(dist_front); Serial.print(" "); Serial.print(dist_back);
    Serial.println(" stopping");
    recvInfo();
    moveUsingInput();
  }
  else{
  
      recvInfo();
      moveUsingInput();
  }

  
  //  PAUSE(spd,dlyP);
}


void readValues(){
        
      Serial.println(analogRead(READ_RF));
      Serial.println(analogRead(READ_RR));
      Serial.println(analogRead(READ_LF));
      Serial.println(analogRead(READ_LR));
}
void moveUsingInput(){
  int control = (recievedChar - '0');

  if(newData == true){  

    Serial.print("control value   is:");
    Serial.print(control);
//    Serial.print(", ");
//    Serial.print("control value 2 is:");
//    Serial.println(control2);
//    
    if(control == 1){
      
      //dist_front = sonar_front.ping_cm();
      Serial.print("Distance ");
      Serial.println(dist_front);
      if((dist_front == 0) || (dist_front > thresh)){
        FORWARD(spd, dly);
        Serial.println("moving forward");
        movingForward = true;
        movingReverse = false;
      }
      else{
        Serial.print("too close ");
        Serial.println(sonar_front.ping_cm());
        PAUSE(spd, dlyP);
      }

    }
    else if (control == 2){
      //dist_back = sonar_back.ping_cm();
      Serial.print("Distance ");
      Serial.println(dist_back);
      if((dist_back == 0) || (dist_back > thresh)){
        REVERSE(spd, dly);
        Serial.println("moving reverse");
        movingForward = false;
        movingReverse = true;
      }
      else{
        Serial.print("too close ");
        Serial.println(dist_back);
        PAUSE(spd, dlyP);
      }
      //readValues();
      //delay(dly*3);
      //PAUSE(spd, dlyP);
    }
    else if (control == 3){
      
      LEFT(spdT, dlyT);
      Serial.println("moving left");
      //readValues();
      //delay(dly*3);
      //PAUSE(spd, dlyP);
    }
    else if (control == 4){
      RIGHT(spdT, dlyT);
      Serial.println("moving right");
      //readValues();
      //delay(dly*);
      //PAUSE(spd, dlyP);
    }
    else if(control == 5){
      PAUSE(spd, dlyP);
      Serial.println("paused");
    }
    else if(control == 6){
      spd = spd + 20;
      spdT = spdT + 20;
      Serial.println("increasing speed");
      Serial.println(spd);
    }
    else if(control == 7){
      spd = spd - 20;
      spdT = spdT - 20;
      Serial.println("decreasing speed");
      Serial.println(spd);
    }
    else{
      Serial.println("unknown input");
      PAUSE(spd,dlyP);
      //Serial.println(READ_RR);
      //Serial.println(READ_RF);
    }
    Serial.println("");
    
  }
  newData = false;
  recvInfo();  
}

void FORWARD(int spd, int dly)
{ 

  for(int i=0; i<=spd;i+=20){
    analogWrite(LEFT_FORWARD,0);
    analogWrite(RIGHT_FORWARD, 0);
    analogWrite(LEFT_REVERSE,i);
    analogWrite(RIGHT_REVERSE,i);
    delay(dly);
  }
}
void REVERSE(int spd, int dly)
{           

  for(int i=0; i<=spd; i+=20){  
    analogWrite(LEFT_FORWARD,i);
    analogWrite(RIGHT_FORWARD, i);
    analogWrite(LEFT_REVERSE,0);
    analogWrite(RIGHT_REVERSE,0);
    delay(dly);
  }
}
void LEFT(int spd, int dly)
{           
  movingForward = false;
  movingReverse = false;
  for(int i=0;i<=spd;i+=20){
    
    analogWrite(LEFT_FORWARD,0);
    analogWrite(RIGHT_FORWARD, 0);
    analogWrite(LEFT_REVERSE,i);
    analogWrite(RIGHT_REVERSE,i/2);
    delay(dly);
  } 
}
void RIGHT(int spd, int dly)
{ 
  //int spdR = spd*2;
  movingForward = false;
  movingReverse = false;
  for(int i=0;i<=spd;i+=20){
    analogWrite(LEFT_FORWARD,0);
    analogWrite(RIGHT_FORWARD,0);
    analogWrite(LEFT_REVERSE,i/2);
    analogWrite(RIGHT_REVERSE,i);
    delay(dly);
  }
}

void PAUSE(int spd, int dly)
{ 
  movingForward = false;
  movingReverse = false;
  for(int i=spd; i>=0;i-=10){
    analogWrite(LEFT_FORWARD,i);
    analogWrite(RIGHT_FORWARD, i);
    analogWrite(LEFT_REVERSE,i);
    analogWrite(RIGHT_REVERSE,i);
    delay(dly);
  }
}  


void recvInfo(){
  if(Serial.available() > 0){
    recievedChar = Serial.read();
    newData = true;
  }
}
 

  
