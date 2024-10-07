static float err_count_l;
static float err_count_r;
static float pre_count_l;
static float pre_count_r;

//クローラーの初期化
void control_initialize(float a, float b, float c, float d, float *e, float *f, float *g, float *h){
  encoder_reset();
  PID_reset();
  control_reset();
  motor_stop();
  *e = a * 1000.0;
  *f = b * 1000.0;
  *g = c * 1000.0;
  *h = d * 1000.0;
}

void control_reset(){
  pre_count_l = 0.0;
  pre_count_r = 0.0;
}

void control_calculate_velocity(float a, float b, float *c, float *d){
  err_count_l = a - pre_count_l;
  *c = err_count_l / (control_period / 1000.0);
  pre_count_l = a;
  
  err_count_r = b - pre_count_r;
  *d = err_count_r / (control_period / 1000.0);
  pre_count_r = b;
}

void control_limitter(int a, int b, int *c, int *d){
  if(a > pwm_limitter_H){
    *c = pwm_limitter_H;
  }
  else if(a < pwm_limitter_L){
    *c = pwm_limitter_L;
  }
  else if(0 < a && a < dead_zone){
    *c = dead_zone;
  }
  else if(-dead_zone < a && a < 0){
    *c = -dead_zone;
  }
  else{
    *c = a;
  }
  
  if(b > pwm_limitter_H){
    *d = pwm_limitter_H;
  }
  else if(b < pwm_limitter_L){
    *d = pwm_limitter_L;
  }
  else if(0 < b && b < dead_zone){
    *d = dead_zone;
  }
  else if(-dead_zone < b && b < 0){
    *d = -dead_zone;
  }
  else{
    *d = b;
  }
}

void control_convolution(int a, int b, int c, int d, float e, float f, float g, float h, int *i, int *j){
  if(0 < a && 0 < c){
    *i = (a < c) ? a : c;
  }
  if(a < 0 && c < 0){
    *i = (a > c) ? a : c;
  }
  if(0 < a && c < 0){
    *i = (a < -c) ? a : c;
  }
  if(a < 0 && 0 < c){
    *i = (-a < c) ? a : c;
  }
  
  
  if(b > 0 && d > 0){
    *j = (b < d) ? b : d;
  }
  if(b < 0 && d < 0){
    *j = (b > d) ? b : d;
  }
  if(b > 0 && d < 0){
    *j = (b < -d) ? b : d;
  }
  if(b < 0 && d > 0){
    *j = (-b < d) ? b : d;
  }
}
