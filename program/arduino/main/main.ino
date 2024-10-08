#include "define.h"
//#include <MsTimer2.h>
#include <stdio.h>
#include <math.h>

static float check = 0;
static float handcheck = 0;

static float x_coordinate = 0; //[m]
static float y_coordinate = 0; //[m]

static float arm_angle1 = 0;
static float arm_angle2 = 0;
static float arm_angle3 = 0;
static float arm_angle4 = 0;
static float arm_gripper = 0;

static int T = 0;

static enum {WAIT,GIVE,REFILL} state = WAIT;

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

  /*
  while(1){
    switch(state){
      case WAIT:
        wait();
        break;
        
      case GIVE:
        give();
        break;
        
      case REFILL:
        refill();
        break;
        
      default:
        break;
    }
    delay(control_period);
  }
  */
  motor_stop();
  exit(0);
}
