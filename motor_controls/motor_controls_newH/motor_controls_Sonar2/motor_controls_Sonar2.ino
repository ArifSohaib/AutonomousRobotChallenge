#include <NewPing.h>
#define trig_front 13
#define echo_front 12
#define trig_back 4
#define echo_back 2
char c;
char recievedChar;
boolean newData = false;


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

unsigned long timestamp1;
unsigned long timestamp2;
bool movingForward = false;
bool movingReverse = false;
unsigned int pingSpeed_F = 50;
unsigned int pingSpeed_B = 75;
unsigned long pingTimer;
unsigned long pingTimer_B;

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
  
}


void loop()
{ 
  if(millis() >= pingTimer){
    pingTimer += pingSpeed_F;
    sonar_front.ping_timer(echoCheck);
  }

  
  if(dist_front < thresh){
      
    PAUSE(spd, dlyP);
    Serial.print("distance:  "); Serial.print(dist_front);
    Serial.println(" stopping");
    recvInfo();
    moveUsingInput();
  }
  else{
  
      recvInfo();
      moveUsingInput();
  }

}

void echoCheckBack(){
  if(sonar_back.check_timer()){
    dist_back = (sonar_back.ping_result / US_ROUNDTRIP_CM);
  }
}
void echoCheck() { // Timer2 interrupt calls this function every 24uS where you can check the ping status.
  // Don't do anything here!
  if (sonar_front.check_timer()) { // This is how you check to see if the ping was received.
    // Here's where you can add code.
    //Serial.print("front distance: ");
    dist_front = (sonar_front.ping_result / US_ROUNDTRIP_CM);
    //dist_back = (sonar_back.ping_result / US_ROUNDTRIP_CM);
    //Serial.print(dist_front); // Ping returned, uS result in ping_result, convert to cm with US_ROUNDTRIP_CM.
    //Serial.println("cm");
  }
  // Don't do anything here!
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

    Serial.print("control value   is:"); Serial.print(control);

    if(control == 1){
      FORWARD(spd, dly);
      Serial.println("moving forward");
    }
    else if (control == 2){
      REVERSE(spd, dly);
      Serial.println("moving forward");
    }
    else if (control == 3){
      
      LEFT(spdT, dlyT);
      Serial.println("moving left");

    }
    else if (control == 4){
      RIGHT(spdT, dlyT);
      Serial.println("moving right");

    }
    else if(control == 5){
      PAUSE(spd, dlyP);
      Serial.println("paused");
    }
    else if(control == 6){
      spd = spd + 20;
      spdT = spdT + 20;
      Serial.print("increasing speed to "); Serial.print(spd); Serial.println(" pwm");
    }
    else if(control == 7){
      spd = spd - 20;
      spdT = spdT - 20;
      Serial.print("decreasing speed to "); Serial.print(spd); Serial.println(" pwm");
    }
    else{
      Serial.println("unknown input");
      PAUSE(spd,dlyP);
    }
    Serial.println("");
    
  }
  newData = false;
  recvInfo();  
}

void FORWARD(int spd, int dly)
{           
  movingForward = true;
  movingReverse = false;
  for(int i=0;i<=spd;i+=20){
    
    analogWrite(LEFT_FORWARD,0);
    analogWrite(RIGHT_FORWARD, 0);
    analogWrite(LEFT_REVERSE,i);
    analogWrite(RIGHT_REVERSE,i);
    delay(dly);
  } 
}


void REVERSE(int spd, int dly)
{           
  movingForward = false;
  movingReverse = true;
  for(int i=0;i<=spd;i+=20){
    
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
 

  
