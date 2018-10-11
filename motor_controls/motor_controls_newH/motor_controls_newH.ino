
//#include <Wire.h> 
//#include <Servo.h>
//#include <LiquidCrystal_I2C.h>
//LiquidCrystal_I2C lcd(0x27,2,1,0,4,5,6,7);  // Set the LCD I2C address
// Analog Pin A4 SDA - Data 
// Analog Pin A5 SCL - Clock (Edge Pin)
/*
 * Filename: Bluetooth.ino
 * Source: https://www.youtube.com/watch?v=fJvtMszk2G4
 * Date: March 2, 2017
*/
#include <NewPing.h>

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


int trig_front = 3;
int echo_front = 2;
int trig_back = 13;
int echo_back = 12;
int LEFT_FORWARD = 6;
int LEFT_REVERSE = 5;
int RIGHT_FORWARD = 10;
int RIGHT_REVERSE = 9;
int spd = 150;
int spdT = 150;
int dly =15;
int dlyP = 30;
int dlyT = 30;
int READ_RF = A1;
int READ_RR = A2;
int READ_LF = A4;
int READ_LR = A5;

NewSonar sonar_front(trigger_front, echo_front, 200);

//define sonar distance variables
long duration;
int distance;
int dist_front;
int dist_back;

// Information on L298N and PWM control
// PWM ranges from 0 to 255. Pins D6 & D9 are used here.  Use analogWrite(6,255) for PWM.
//http://tronixstuff.com/2014/11/25/tutorial-l298n-dual-motor-controller-modules-and-arduino/
void setup()
{ 
  
  pinMode(trig_front, OUTPUT);
  pinMode(trig_back, OUTPUT);
  pinMode(echo_front, OUTPUT);
  pinMode(echo_back, OUTPUT);
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
void loop()
{ 
  recvInfo();
  moveUsingInput();
  
  //PAUSE(spd,0);
}

int getDist(int trig, int echo){
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration*0.034/2;
  return distance;
}

void readValues(){
      
      Serial.println(analogRead(READ_RR));
      Serial.println(analogRead(READ_RR));
      Serial.println(analogRead(READ_RR));
      Serial.println(analogRead(READ_RR));
}
void moveUsingInput(){
  int control = (recievedChar - '0');

  if(newData){
    Serial.print(control);
  }

  while(newData == true){
    
    if(control == 1){
      dist_front = getDist(trig_front, echo_front);
      Serial.print("Distance");
      Serial.println(dist_front);
      if(sonar_front.ping_cm() > 10){
        FORWARD(spd, dly);
        Serial.println("moving forward");
      }
      else{
        Serial.println("too close");
      }
      //readValues();
      //delay(dly*3);
      //PAUSE(spd, dlyP);
      
    }
    else if (control == 2){
      REVERSE(spd, dly);
      Serial.println("moving reverse");
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
      Serial.println(READ_RR);
      Serial.println(READ_RF);
    }
    newData = false;
    //readValues();
  }

    

}

void FORWARD(int spd, int dly)
{ 
  for(int i=0; i<=spd;i+=10){
    
    analogWrite(LEFT_FORWARD,i);
    analogWrite(RIGHT_FORWARD, i);
    analogWrite(LEFT_REVERSE,0);
    analogWrite(RIGHT_REVERSE,0);
    delay(dly);
  }
}
void REVERSE(int spd, int dly)
{           
  for(int i=0; i<=spd; i+=10){  
    analogWrite(LEFT_FORWARD,0);
    analogWrite(RIGHT_FORWARD, 0);
    analogWrite(LEFT_REVERSE,i);
    analogWrite(RIGHT_REVERSE,i);
    delay(dly);
  }
}
void LEFT(int spd, int dly)
{           
  int spdR = spd/2;
  for(int i=0;i<=spd;i+=10){
    
    analogWrite(LEFT_FORWARD,i);
    analogWrite(RIGHT_FORWARD, 0);
    analogWrite(LEFT_REVERSE,0);
    analogWrite(RIGHT_REVERSE,i/2);
    delay(dly);
  }
}
void RIGHT(int spd, int dly)
{ 
  int spdR = spd/2;
  for(int i=0;i<=spd;i+=10){
    analogWrite(LEFT_FORWARD,0);
    analogWrite(RIGHT_FORWARD, i);
    analogWrite(LEFT_REVERSE,i/2);
    analogWrite(RIGHT_REVERSE,0);
    delay(dly);
  }
}

void PAUSE(int spd, int dly)
{ 
  for(int i=spd; i>=0;i-=10){
    analogWrite(LEFT_FORWARD,i);
    analogWrite(RIGHT_FORWARD, i);
    analogWrite(LEFT_REVERSE,i);
    analogWrite(RIGHT_REVERSE,i);
    delay(dly);
  }
}  
void SQUARE()
{ 
//  delay(5000); lcd.setCursor ( 0, 0 ); lcd.print ("STOPPED.           ");      
//  lcd.setCursor ( 0, 1 ); lcd.print ("                 ");      
  digitalWrite(4,LOW);    digitalWrite(5,LOW);   analogWrite(6,0);
  digitalWrite(7,LOW);  digitalWrite(8,LOW);  analogWrite(9,0);
  while (1) {};
}

void recvInfo(){
  if(Serial.available() > 0){
    recievedChar = Serial.read();
    newData = true;
  }
}
 
 void CCW(int dly)
{ // dly =450 for 90-deg
//  lcd.setCursor ( 0, 0 ); lcd.print ("<");      
//  lcd.setCursor ( 0, 1 ); lcd.print ("                ");      
  digitalWrite(4,LOW);   digitalWrite(5,HIGH); analogWrite(6,175);
  digitalWrite(7,HIGH);  digitalWrite(8,LOW);  analogWrite(9,175);
  delay(dly);//PAUSE(dly);
}
void CW(int dly)
{ // dly = 450 for 90-deg
//  lcd.setCursor ( 0, 0 ); lcd.print (">");      
//  lcd.setCursor ( 0, 1 ); lcd.print ("                ");      
  digitalWrite(4,HIGH); digitalWrite(5,LOW);   analogWrite(6,175);
  digitalWrite(7,LOW);  digitalWrite(8,HIGH);  analogWrite(9,175);
  delay(dly);//PAUSE(dly);
}
  

