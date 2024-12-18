static int run_speed     = 200; //(pwm)200-1023
static int joint1_speed  = 200;  
static int joint2_speed  = 200;
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
  _angle     = map(_angle, 0, 1023, POT_MIN, POT_MAX);
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
  }
  else if(_down){
    joint3_angle -= 1;
  }
  joint3_ang_limitter(joint3_angle, &joint3_angle);
  joint3(joint3ID, joint3_angle, joint3_vel);
  delay(100);
}
  
  
void radicon_joint4(bool _up, bool _down){
  if(_up){
    joint4_angle += 1;
  }
  else if(_down){
    joint4_angle -= 1;
  }
  joint4_ang_limitter(joint4_angle, &joint4_angle);
  joint4(joint4ID, joint4_angle, joint4_vel);
  delay(100);
}

void radicon_run(int A, int C, int F){
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
  Serial.print("state = ");
  Serial.println(state);

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

void radicon(){
  while(1){  
    int MR8_A = pulseIn(PIN_MR8_A,HIGH);
    int MR8_C = pulseIn(PIN_MR8_C,HIGH);
    int MR8_E = pulseIn(PIN_MR8_E,HIGH);
    int MR8_F = pulseIn(PIN_MR8_F,HIGH);

    if(1800 <  MR8_E) MR8_E = 1;
    else              MR8_E = 0;

    if(MR8_E == 1) break;

    raspi_send(4, state, MR8_A, MR8_C, MR8_E);
    
    Serial.print("MR8_A = ");
    Serial.print(MR8_A);
    Serial.print("  MR8_C = ");
    Serial.print(MR8_C);
    Serial.print("  MR8_E = ");
    Serial.print(MR8_E);
    Serial.print("  MR8_F = ");
    Serial.print(MR8_F);
    Serial.println();
    
    radicon_run(MR8_A, MR8_C, MR8_F);

    delay(10);
  }
  
}
