#include "define.h"



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
