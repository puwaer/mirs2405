static int turntable_speed = 50;

static bool front_l = false;
static bool back_l = false;
static bool front_r = false;
static bool back_r = false;
static bool left_l = false;
static bool right_l = false;
static bool left_r = false;
static bool right_r = false;

void radicon_gripper(bool _open, bool _close){
  int _ang;
  if(_open){
    _ang += 1;
    if(GRIP_OPEN_ANG <= _ang){
      _ang = GRIP_OPEN_ANG;
    }
  }
  else if(_close){
    _ang -= 1;
    if(_ang <= GRIP_CLOSE_ANG){
      _ang = GRIP_CLOSE_ANG;
    }
  }
  else{
  }
  
  grip.write(_ang);
  
  delay(1000);
}

void radicon_turntable(bool _left, bool _right){
  turntable_run(turntable_speed);
  if(_left){
    turntable_run(turntable_speed);
  }
  else if(_right){
    turntable_run(-turntable_speed);
  }
  else{
    turntable_run(0);
  }
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

  if(state == 0){
    radicon_gripper(false, false);
    radicon_turntable(false, false);
  }
  else if(state == 1){
    radicon_gripper(false, false);
    radicon_turntable(left_l, right_l);
    
  }
  else if(state == 2){
    radicon_gripper(false, false);
    radicon_turntable(false, false);
  }
  else{
    radicon_gripper(false, false);
    radicon_turntable(false, false);
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
