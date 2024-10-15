#include "define.h"
#include <stdio.h>
#include <math.h>
#include <arduino.h>
#include <Servo.h>

Servo scs_1;
Servo scs_2;

static float x_coordinate = 0; //[m]
static float y_coordinate = 0; //[m]

void setup() {
  confirmation_device();
  io_open();
  encoder_open();
  motor_open();
  arm_open();
  raspi_open();
  Serial.begin(115200);
}

void loop() {
  check_raspy();
  motor_stop();
  exit(0);
}
