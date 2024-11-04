static int run_speed     = 50; //(pwm)50-255
static int joint1_speed  = 50;  
static int joint2_speed  = 50;
static int joint3_angle  = 0;
static int joint3_speed  = 1; //度/sec
static int joint4_angle  = 0;
static int joint4_speed  = 1; //度/sec

static bool front_l = false;
static bool back_l = false;
static bool front_r = false;
static bool back_r = false;


static int var = 0;
static int old_var = 0;
static int state = 0;   //0:走行 1:グリッパー、ターンテーブル 2:一、二関節 3:三、四関節
static int maxState = 3; 

//chA 1100 - 1900 1200以下:バック 1700以上:前進
//押し込み　1500以下:通常 1900以上:押し込み

void radicon_run_r(bool _f, bool _b){
  if(_f){
    motor_run_r(run_speed);
  }
  else if(_b){
    motor_run_r(-run_speed);
  }
  else{
    motor_run_r(0); 
  }
}

void radicon_run_l(bool _f, bool _b){
  if(_f){
    motor_run_l(run_speed);
  }
  else if(_b){
    motor_run_l(-run_speed);
  }
  else{
    motor_run_l(0); 
  }
}

void radicon_joint1(bool _up, bool _down){
  int _angle = analogRead(PIN_JOINT_1_POT);
  _angle     = map(_angle, 0, 1023, POT_MIN, POT_MAX);
  if((_angle <= joint1_ang_limitter_L) || (joint1_ang_limitter_H <= _angle)){
    joint1_L_run(0);
    joint1_R_run(0);
  }
  else{
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
}

void radicon_joint2(bool _up, bool _down){
  int _angle = analogRead(PIN_JOINT_2_POT);
  _angle     = map(_angle, 0, 1023, POT_MIN, POT_MAX);
  if((_angle <= joint2_ang_limitter_L) || (joint2_ang_limitter_H <= _angle)){
    joint2_run(0);
  }
  else{
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
  
}

void radicon_joint3(bool _up, bool _down){
  if(_up){
    joint3_angle += 1;
    
    joint3(joint3ID, joint3_angle, joint3_vel);
  }
  else if(_down){
    joint3_angle -= 1;
    joint3(joint3ID, joint3_angle, joint3_vel);
  }
  delay(1000);
}
  
  
void radicon_joint4(bool _up, bool _down){
  if(_up){
    joint4_angle += 1;
    joint4(joint4ID, joint4_angle, joint4_vel);
  }
  else if(_down){
    joint4_angle -= 1;
    joint4(joint4ID, joint4_angle, joint4_vel);
  }
  delay(1000);
}

void radicon(int A, int C, int F){
  if(A < 1200){
    front_l = false;
    back_l = true;
  }
  else if(1700 < A){
    front_l = true;
    back_l = false;
  } 
  else{
    front_l = false;
    back_l = false;
  }

  if(C < 1200){
    front_l = false;
    back_l = true;
  }
  else if(1700 < C){
    front_l = true;
    back_l = false;
  } 
  else{
    front_l = false;
    back_l = false;
  }

  if(1800 < F)   F = 1;
  else           F = 0;

  var =  F;
  var = !(var);

    //スイッチが離された瞬間を読み取る
  if(var == LOW && old_var == HIGH){
    state++;
    if (state > maxState){
      state = 0;
    }
  }
  
  old_var = var; //varのをold_varに保存

  if(state == 0){
    radicon_run_l(front_l, back_l);
    radicon_run_r(front_r, back_r);
    radicon_joint1(false, false);
    radicon_joint2(false, false);
    radicon_joint3(false, false);
    radicon_joint4(false, false);
  }
  else if(state == 1){
    radicon_run_l(false, false);
    radicon_run_r(false, false);
    radicon_joint1(false, false);
    radicon_joint2(false, false);
    radicon_joint3(false, false);
    radicon_joint4(false, false); 
  }
  else if(state == 2){
    radicon_run_l(false, false);
    radicon_run_r(false, false);
    radicon_joint1(front_l, back_l);
    radicon_joint2(front_r, back_r);
    radicon_joint3(false, false);
    radicon_joint4(false, false); 
  }
  else if(state == 3){
    radicon_run_l(false, false);
    radicon_run_r(false, false);
    radicon_joint1(false, false);
    radicon_joint2(false, false);
    radicon_joint3(front_l, back_l);
    radicon_joint4(front_r, back_r); 
  }
  else{
    radicon_run_l(false, false);
    radicon_run_r(false, false);
    radicon_joint1(false, false);
    radicon_joint2(false, false);
    radicon_joint3(false, false);
    radicon_joint4(false, false); 
  }
}
