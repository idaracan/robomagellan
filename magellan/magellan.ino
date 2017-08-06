#include <SoftwareSerial.h>
#include <NewPing.h>

//motor outputs
#define EA 9
#define EB 10
#define IN1 8
#define IN2 11
#define IN3 12
#define IN4 13
//sensor 
#define TRIGGER_PIN_L  3  
#define ECHO_PIN_L     2  

#define TRIGGER_PIN_R  5 
#define ECHO_PIN_R     4 

#define TRIGGER_PIN_C  7 
#define ECHO_PIN_C     6 

#define MAX_DISTANCE 1000

NewPing sonarl(TRIGGER_PIN_L, ECHO_PIN_L, MAX_DISTANCE);
NewPing sonarc(TRIGGER_PIN_C, ECHO_PIN_C, MAX_DISTANCE);
NewPing sonarr(TRIGGER_PIN_R, ECHO_PIN_R, MAX_DISTANCE);
//velocidad
#define maxspeed 255
#define halfspeed 177
//variables
boolean evasion=true;
boolean movement=false;
const float pi = 3.14;
int vel = maxspeed;

void setup() {
  // initializing motor outputs
  pinMode(EA, OUTPUT);
  pinMode(EB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  // motor enablers
  digitalWrite(EA, HIGH);
  digitalWrite(EB, HIGH);
  //initializing serial ports
  Serial.begin(115200);
  Serial.flush();
  randomSeed(analogRead(0));
}

// the loop routine runs over and over again forever: 
void loop() {
 
  // Dispatch incoming characters
  while (Serial.available() == 0) {
    if (movement==true){
      obstaculo();
      forward();
    }else{}
  }
  String input = Serial.readString();
  Serial.println(input);
  if(input == "u"){
    forward();
  }else if(input == "d"){
    backward();
  }else if(input == "s"){
    halt();
  }else if(input == "g"){
    evasion = false;
  }else{
    float ang  = input.toFloat();
    int secs = (int) (ang*1600)/360;
    if (secs > 0){
      right(secs);
    }else{
      left(secs);
    }
  }
}
//subroutines
void obstaculo(){
  int leftDist = sonarl.ping_cm();
  if (leftDist < 40){
    if (evasion == true){
      right(200);
    }else{
      left(200);
    }
  }
  int rightDist = sonarc.ping_cm();
  if (rightDist < 40){
    if (evasion == true){
      left(200);
    }else{
      right(200);
    }
  }
  int centralDist = sonarr.ping_cm();
  if (centralDist < 40){
    if (evasion == true){
      backward();
      delay(500);
      if (random(1) == 0){
        left(800);
      }else{
        right(800);
      }
    }else{
      if (centralDist < 10){
        delay(100);
        halt();
        while(true){}
      }
    }
  } 
}

void left(int secs){
  halt();
  analogWrite(IN2,maxspeed);
  analogWrite(IN4,maxspeed);
  delay(secs);
  halt();
}
void right(int secs){
  halt();
  analogWrite(IN1,maxspeed);
  analogWrite(IN3,maxspeed);
  delay(secs);
  halt();
}
void forward(){
  halt();
  analogWrite(IN1,vel);
  analogWrite(IN4,vel);
  movement=true;
  //Serial.println("se esta moviendo hacia atras");
}
void backward(){
  halt();
  analogWrite(IN2,vel);
  analogWrite(IN3,vel);
  //Serial.println("se esta moviendo hacia adelante");
}
void halt(){
  analogWrite(IN1,0);
  analogWrite(IN2,0);
  analogWrite(IN3,0);
  analogWrite(IN4,0);
  movement=false;
  //Serial.println("se detuvo");
}
  
