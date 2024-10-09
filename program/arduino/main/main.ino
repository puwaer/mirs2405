#include "define.h"
#include <stdio.h>
#include <math.h>

static float x_coordinate = 0; //[m]
static float y_coordinate = 0; //[m]

void setup(){
  confirmation_device();
  io_open();
  encoder_open();
  motor_open();
  arm_open();
  raspi_open();
  //MsTimer2::set(1000, timer_cnt);
}

void loop(){
  
  run_debug();
  motor_stop();
  exit(0);
}
