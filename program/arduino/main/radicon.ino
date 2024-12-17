static int turntable_speed = 50;

static bool front_l = false;
static bool back_l = false;
static bool front_r = false;
static bool back_r = false;

static int var = 0;
static int old_var = 0;
static int state = 0;   //0:走行 1:グリッパー、ターンテーブル 2:一、二関節 3:三、四関節
static int maxState = 3; 

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

void radicon_run(int A, int C, int state){
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
    front_l = true;
    back_l = false;
  }
  else if(1700 < C){
    front_l = false;
    back_l = true;
  } 
  else{
    front_l = false;
    back_l = false;
  }

  if(state == 0){
    radicon_gripper(false, false);
    radicon_turntable(false, false);
  }
  else if(state == 1){
    radicon_gripper(front_l, back_l);
    radicon_turntable(front_r, back_r);
    
  }
  else if(state == 2){
    radicon_gripper(false, false);
    radicon_turntable(false, false);
  }
  else if(state == 3){
    radicon_gripper(false, false);
    radicon_turntable(false, false); 
  }
  else{
    radicon_gripper(false, false);
    radicon_turntable(false, false);
  }
}

void radicon(bool _check, int MR8_A, int MR8_C, int state){
  while(1){
    if(!_check){
      break;
    }
    
    radicon_run(MR8_A, MR8_C, state);
    delay(10);
  }
  
}
