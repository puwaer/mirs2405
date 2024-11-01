#include "define.h"
#include <stdio.h>
#include <math.h>
#include <arduino.h>

void setup() {
  confirmation_device();
  encoder_open();
  motor_open();
  arm_open();
  Serial.begin(115200);
  delay(100);

  raspi_open();
}

void loop() {
  //run_debug();
  //arm_debug();
  radicon(100,100,100);

  check_raspi();
  motor_stop();
  exit(0);
}

/*  run(x, y)  (x,y)へ移動
    arm(ang1, ang2, ang3, ang4) アームを指定角度へ　すべて絶対角度
      ang3,4: 0~300[°]

*/
