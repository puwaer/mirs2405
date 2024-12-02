#include "define.h"
#include <Servo.h>

Servo grip;
Servo airchuck1;
Servo airchuck2;

void setup(){
  arm_init();
  raspi_open();
}

void loop(){
  turntable_debug();
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
