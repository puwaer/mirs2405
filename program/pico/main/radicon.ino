const int run_speed     = 50; //(pwm)50-255
const int joint1_speed  = 50;  
const int joint2_speed  = 50;
const int joint3_angle  = 0;

// limitをまだ作ってない

void radicon_run(bool _r, bool _l, bool _f, bool _b){
  if(_r){
    motor_run_l(run_speed);
    motor_run_r(-run_speed);
  }
  else if(_l){
    motor_run_l(-run_speed);
    motor_run_r(run_speed);
  }
  else if(_f){
    motor_run_l(run_speed);
    motor_run_r(run_speed);
  }
  else if(_b){
    motor_run_l(-run_speed);
    motor_run_r(-run_speed);
  }
  else{
    motor_run_l(0);
    motor_run_r(0); 
  }
}

// _joint n:第n関節
void radicon_arm(bool _up, bool _down, int _joint){
  if(_joint = 1){
    if(_up){
      joint1_L_run(-joint1_speed);
      joint1_R_run(joint1_speed);
    }
    else if(_down){
      joint1_L_run(joint1_speed);
      joint1_R_run(-joint1_speed);
    }
    else{
      joint1_L_run(0);
      joint1_R_run(0);
    }
  }
  
  if(_joint = 2){
    if(_up){
      joint2_run(joint2_speed);
    }
    else if(_down){
      joint2_run(-joint2_speed);
    }
    else{
      joint2_run(0);
    }
  }
  
  if(_joint = 3){
    if(_up){
      joint3_angle += 1;
      joint3_4(joint3ID, joint3_angle);
    }
    else if(_down){
      joint3_angle -= 1;
      joint3_4(joint3ID, joint3_angle);
    }
  }
  
  if(_joint = 4){
    if(_up){
      joint4_angle += 1;
      joint3_4(joint4ID, joint4_angle);
    }
    else if(_down){
      joint4_angle -= 1;
      joint3_4(joint4ID, joint4_angle);
    }
  }
  delay(10);
}
