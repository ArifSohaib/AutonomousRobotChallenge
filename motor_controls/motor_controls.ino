#include <Wire.h> 
//#include <LiquidCrystal_I2C.h>
//LiquidCrystal_I2C lcd(0x27,2,1,0,4,5,6,7);  // Set the LCD I2C address
// Analog Pin A4 SDA - Data 
// Analog Pin A5 SCL - Clock (Edge Pin)
/*
 * Filename: Bluetooth.ino
 * Source: https://www.youtube.com/watch?v=fJvtMszk2G4
 * Date: March 2, 2017
*/

char c;
char recievedChar;
boolean newData = false;
//SoftwareSerial mySerial(10,11);
// Reading 4x4 Keypad with ONE Arduino Pin
// by Hari Wiguna, 2016
// Source: https://www.youtube.com/watch?v=G14tREsVqz0&t=325s
// Check schematics and resistors placement.

int speed = 0;
float dX = 0;
float dY = 0;
float dly = 0;
int Xdir = 0;
int Ydir = 0;
// Information on L298N and PWM control
// PWM ranges from 0 to 255. Pins D6 & D9 are used here.  Use analogWrite(6,255) for PWM.
//http://tronixstuff.com/2014/11/25/tutorial-l298n-dual-motor-controller-modules-and-arduino/
void setup()
{ // FORWARD(100); delay(500);  REVERSE(100); delay(500); // Wake up Jerk.
  // IR obstacle sensors: 3 units. 45-deg configuration. ~5-inch range 
  pinMode(A0,INPUT); // receive signal from the sensor 45-deg Left
  pinMode(A1,INPUT); // receive signal from the sensor Center Forward
  pinMode(A2,INPUT); // receive signal from the sensor 45-deg Right
  int Xstart = 0; int Ystart = 0.0; //meter TechShop Hub Post
  int Xdir = 1 ; int Ydir = 0; // Initial direction.
  int dX = 0 ; int dY = 0; // Target dX to Xdest & dY to Ydest

  pinMode(4,OUTPUT); // Right Motor Direction
  pinMode(5,OUTPUT); // Right Motor Direction
  pinMode(6,OUTPUT); // Right Motor Speed
  
  pinMode(7,OUTPUT); // Left Motor Direction
  pinMode(8,OUTPUT); // Left Motor Direction
  pinMode(9,OUTPUT); // Left Motor Speed
  Serial.begin(9600);
  
//  mySerial.begin(9600);
  //Serial.println("Testing Bluetooth.  Sync with Android Bluetooth now.");
}
void loop()
{ 
  recvInfo();
  moveUsingInput();
  //Test1();
}

void moveUsingInput(){
  int control = (recievedChar - '0');
  if(newData){
    Serial.print(control);
  }
  int dly = 1000;
  while(newData == true){
    
    if(control == 1){
      FORWARD(dly);
      Serial.println("moving forward");
    }
    else if (control == 2){
      REVERSE(dly);
      Serial.println("moving reverse");
    }
    else if (control == 3){
      LEFT(dly);
      Serial.println("moving left");
    }
    else if (control == 4){
      RIGHT(dly);
      Serial.println("moving right");
    }
    else if(control == 5){
      PAUSE(dly);
      Serial.println("paused");
    }
    else{
      Serial.println("unknown input");
    }
    newData = false;
  }
}
// Forward and Reverse 1 meter and 1 meter circle
void Test1() 
{ 
//  lcd.clear ();    lcd.home ();
//  lcd.setCursor (0,0); lcd.print (" Fwd & Bwd 1 meter."); 
// // lcd.setCursor (0,1); lcd.print (" Circles & Rotates."); 
  float dly = 3500.0;
   FORWARD(dly); PAUSE(2000); 
   REVERSE(dly); PAUSE(2000);
   SQUARE();
}

void FORWARD(int dly)
{ 
// lcd.setCursor ( 0, 0 );   lcd.print ("^");      
////  lcd.setCursor ( 0, 1 ); lcd.print ("                ");      
  digitalWrite(4,LOW);  digitalWrite(5,HIGH);  analogWrite(6,250);
  digitalWrite(7,LOW);  digitalWrite(8,HIGH);  analogWrite(9,250);
  delay(dly); 
}
void REVERSE(int dly)
{ 
//  lcd.setCursor ( 0, 0 ); lcd.print ("v");      
////  lcd.setCursor ( 0, 1 ); lcd.print ("                ");      
  digitalWrite(4,HIGH);  digitalWrite(5,LOW);  analogWrite(6,250);
  digitalWrite(7,HIGH);  digitalWrite(8,LOW);  analogWrite(9,250);
  delay(dly);
}
void LEFT(int dly)
{ // dly =450 for 90-deg
//  lcd.setCursor ( 0, 0 ); lcd.print ("<");      
//  lcd.setCursor ( 0, 1 ); lcd.print ("                ");      
  digitalWrite(4,LOW);   digitalWrite(5,HIGH); analogWrite(6,125);
  digitalWrite(7,HIGH);  digitalWrite(8,LOW);  analogWrite(9,250);
  delay(dly); PAUSE(1);
}
void RIGHT(int dly)
{ // dly = 450 for 90-deg
//  lcd.setCursor ( 0, 0 ); lcd.print (">");      
//  lcd.setCursor ( 0, 1 ); lcd.print ("                ");      
  digitalWrite(4,HIGH); digitalWrite(5,LOW);   analogWrite(6,250);
  digitalWrite(7,LOW);  digitalWrite(8,HIGH);  analogWrite(9,125);
  delay(dly); PAUSE(1);
}
void PAUSE(int dly)
{ 
//  lcd.setCursor (0,0); lcd.print ("x");      
//  lcd.setCursor ( 0, 1 ); lcd.print ("                 ");      
  digitalWrite(4,LOW);  digitalWrite(5,LOW);  analogWrite(6,0);
  digitalWrite(7,LOW);  digitalWrite(8,LOW);  analogWrite(9,0);
  delay(dly);
  exit;
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
