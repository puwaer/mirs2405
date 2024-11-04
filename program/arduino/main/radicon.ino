
static int turntable_speed = 50;

static bool front_l = false;
static bool back_l = false;
static bool front_r = false;
static bool back_r = false;

static int var = 0;
static int old_var = 0;
static int state = 0;   //0:走行 1:グリッパー、ターンテーブル 2:一、二関節 3:三、四関節
static int maxState = 3; 


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

void radicon_gripper(bool _open, bool _close){
  int ang;
  if(_open){
    ang += 1;
    if(GRIP_OPEN_ANG <= ang){
      ang = GRIP_OPEN_ANG;
    }
  }
  else if(_close){
    ang -= 1;
    if(ang <= GRIP_CLOSE_ANG){
      ang = GRIP_CLOSE_ANG;
    }
  }
  else{
  }
  
  grip.write(ang);
  
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
