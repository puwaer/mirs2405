static int run_speed     = 200; //(pwm)200-1023
static int joint1_speed  = 200;  
static int joint2_speed  = 200;
static int joint3_angle  = joint3_ang_center;
static int joint3_angle2  = joint3_angle*2;
static int joint3_speed  = 1; //度/sec
static int joint4_angle  = joint4_ang_center;
static int joint4_angle2  = joint4_angle*2;
static int joint4_speed  = 1; //度/sec

static bool front_l = false;
static bool back_l = false;
static bool front_r = false;
static bool back_r = false;
static bool left_l = false;
static bool right_l = false;
static bool left_r = false;
static bool right_r = false;

static int var = 0;
static int old_var = 0; 

//chA 1100 - 1900 1200以下:前進 1700以上:後退
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
  int _angle = analogRead(PIN_JOINT_1_R_POT);
  _angle     = mapf(_angle, POT_READ_MIN_1_R, POT_READ_MAX_1_R, POT_ANGLE_MIN_1_R, POT_ANGLE_MAX_1_R);
  if((_angle <= joint1_ang_limitter_L) || (joint1_ang_limitter_H <= _angle)){
    joint1_L_run(0);
    joint1_R_run(0);
  }
  else{
    if(_up){
      joint1_L_run(joint1_speed);
      joint1_R_run(joint1_speed);
    }
    else if(_down){
      joint1_L_run(-joint1_speed);
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
  _angle     = mapf(_angle, POT_READ_MIN_2, POT_READ_MAX_2, POT_ANGLE_MIN_2, POT_ANGLE_MAX_2);
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
    joint3_angle2 += 1;
  }
  else if(_down){
    joint3_angle2 -= 1;
  }

  if(joint3_ang_limitter_H*2 <= joint3_angle2){
    joint3_angle2 = joint3_ang_limitter_H*2;
  } 
  else if(joint3_angle2 <= joint3_ang_limitter_L*2){
    joint3_angle2 = joint3_ang_limitter_L*2;
  }

  joint3_angle = joint3_angle2 / 2;
  joint3_angle -= joint3_ang_center;

  //joint3_ang_limitter(joint3_angle, &joint3_angle);
  //joint3_angle -= joint3_ang_center;

  joint3(joint3ID, joint3_angle, joint3_speed);
  
}
  
void radicon_joint4(bool _up, bool _down){
  if(_up){
    joint4_angle2 += 1;
  }
  else if(_down){
    joint4_angle2 -= 1;
  }

  if(joint4_ang_limitter_H*2 <= joint4_angle2){
    joint4_angle2 = joint4_ang_limitter_H*2;
  } 
  else if(joint4_angle2 <= joint4_ang_limitter_L*2){
    joint4_angle2 = joint4_ang_limitter_L*2;
  }

  joint4_angle = joint4_angle2 / 2;
  joint4_angle -= joint4_ang_center;
  
  //joint4_ang_limitter(joint4_angle, &joint4_angle);
  joint4(joint4ID, joint4_angle, joint4_speed);
  Serial.println(joint4_angle);
  Serial.println(joint4_angle2);

}

void radicon_run(int A, int B, int C, int D, int E, int state){
  if(A < 1200){
    front_l = true;
    back_l = false;
  }
  else if(1700 < A){
    front_l = false;
    back_l = true;
  }
  else{
    front_l = false;
    back_l = false;
  }

  if(B < 1200){
    left_l = true;
    right_l = false;
  }
  else if(1700 < B){
    left_l = false;
    right_l = true;
  }
  else{
    left_l = false;
    right_l = false;
  }

  if(C < 1200){
    front_r = true;
    back_r = false;
  }
  else if(1700 < C){
    front_r = false;
    back_r = true;
  } 
  else{
    front_r = false;
    back_r = false;
  }

  if(D < 1200){
    left_r = true;
    right_r = false;
  }
  else if(1700 < D){
    left_r = false;
    right_r = true;
  }
  else{
    left_r = false;
    right_r = false;
  }

  /*if(1800 < F)   F = 1;
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
  Serial.print("state = ");
  Serial.println(state);*/

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
    radicon_joint1(front_l, back_l);
    radicon_joint2(front_r, back_r);
    radicon_joint3(false, false);
    radicon_joint4(left_r, right_r); 
  }
  else if(state == 2){
    radicon_run_l(false, false);
    radicon_run_r(false, false);
    radicon_joint1(false, false);
    radicon_joint2(false, false);
    radicon_joint3(front_l, back_l);
    radicon_joint4(false, false); 
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

void radicon(int MR8_A, int MR8_B, int MR8_C, int MR8_D, int MR8_E, int state){
  Serial.print("MR8_A = ");
  Serial.print(MR8_A);
  Serial.print("  MR8_B = ");
  Serial.print(MR8_B);
  Serial.print("  MR8_C = ");
  Serial.print(MR8_C);
  Serial.print("  MR8_D = ");
  Serial.print(MR8_D);
  Serial.print("  MR8_E = ");
  Serial.print(MR8_E);
  Serial.print("  state = ");
  Serial.print(state);
  Serial.println();

  //Serial.println(analogRead(PIN_JOINT_1_R_POT));

  radicon_run(MR8_A, MR8_B, MR8_C, MR8_D, MR8_E, state);
    
  delay(10);
  
}
