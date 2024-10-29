#include "define.h"
#include <stdio.h>
#include <math.h>
#include <arduino.h>

static float x_coordinate = 0; //[m]
static float y_coordinate = 0; //[m]

void setup() {
  confirmation_device();
  encoder_open();
  motor_open();
  arm_open();
  raspi_open();
  Serial.begin(115200);

  delay(1000);
}

void loop() {
  check_raspi();
  motor_stop();
  exit(0);
}

/*  run(x, y)  (x,y)へ移動
    arm(ang1, ang2, ang3, ang4) アームを指定角度へ　すべて絶対角度
      ang3,4: 0~300[°]

*/
