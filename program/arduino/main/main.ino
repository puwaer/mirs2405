#include "define.h"
#include <Servo.h>
#include <Wire.h>

Servo grip;
Servo airchuck1;
Servo airchuck2;

void setup(){
  arm_init();
  turntable_init();
  Wire.begin();   
  Serial.begin(115200);
  raspi_open();
  delay(100);
}

void loop(){
  /*while(1){
    raspi_receive();
  }*/
  
  while(1){
    ultrasonic();
  }

  //turntable_debug();
  //grip_debug();
  exit(0);
}

/*
void gripper(bool check)
    check:true  → 開く
          false → 閉じる

airchuck(bool check)
    check:true  → 開く
          false → 閉じる

PUMP(bool check)
    check:true  
          false
  
turntable(int angle);
    angle: 相対角度 -180-180度
    
*/
