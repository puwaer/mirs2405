static int turntable_speed = 50;

static bool front_l = false;
static bool back_l = false;
static bool front_r = false;
static bool back_r = false;
static bool left_l = false;
static bool right_l = false;
static bool left_r = false;
static bool right_r = false;

static bool h = false;

static int mode = 0;

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

void radicon_run(int A, int B, int C, int D, int G, int H){
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

  if (990 <= G && G <= 1000) mode = 0;
  else if (1040 <= G && G <=1050) mode = 1;
  else if (1090 <= G && G <=1100) mode = 2;
  else mode = 0;

  if (990 <= H && H <= 1000) h = false;
  else if (1040 <= H && H <=1050) h = true;
  else h = false;

  if(mode == 1){
    radicon_turntable(left_l, right_l);
  }
  else if(mode == 2){
    radicon_turntable(false, false);
  }
  else{
    radicon_turntable(false, false);
  }
}

void radicon(int MR8_A, int MR8_B, int MR8_C, int MR8_D, int MR8_G, int MR8_H){
  
  Serial.print("MR8_A = ");
  Serial.print(MR8_A);
  Serial.print("  MR8_B = ");
  Serial.print(MR8_B);
  Serial.print("  MR8_C = ");
  Serial.print(MR8_C);
  Serial.print("  MR8_D = ");
  Serial.print(MR8_D);
  Serial.print("  MR8_G = ");
  Serial.print(MR8_G);
  Serial.print("  MR8_H= ");
  Serial.print(MR8_H);
  Serial.println();
  
  radicon_run(MR8_A, MR8_B, MR8_C, MR8_D, MR8_G, MR8_H);
    
  delay(10);
  
}
