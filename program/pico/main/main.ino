#include "define.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <arduino.h>

void setup() {
  confirmation_device();
  encoder_open();
  motor_open();
  arm_open();
  analogWriteRange(PWM_MAX);
  Serial.begin(115200);
  delay(100);

  raspi_open();
}

void loop() {
  //run_debug();
  arm_debug();
  //radicon_debug();

  //check_raspi();
  motor_stop();
  exit(0);
}

/*  run(x, y)  (x,y)へ移動
    arm(ang1, ang2, ang3, ang4) アームを指定角度へ　すべて絶対角度
      ang1,2: -150~150[°]
      ang3,4: -150~150[°]

*/
