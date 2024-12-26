static float err_count_l;
static float err_count_r;
static float pre_count_l;
static float pre_count_r;

float r      = 0; //[m]
float theta  = 0; //[rad]
float omega  = 1; //[m/rad]
float dist   = 0; //[m]
float vel    = 0.5; //[m/s]

float dist_l = 0;
float dist_r = 0;
float vel_l  = 0;
float vel_r  = 0;

float target_velocity_l;
float target_velocity_r;
float target_displacement_l;
float target_displacement_r;
float velocity_l;
float velocity_r;
float displacement_l;
float displacement_r;
int pwm_ln_v;
int pwm_rn_v;
int pwm_ln_d;
int pwm_rn_d;
int pwm_l;
int pwm_r;

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

void run_To(float x, float y){
  r = powf(powf(x,2)+powf(y,2), 0.5);
  if(y == 0){
    if(x >= 0) theta = 0;
    else if(x < 0) theta = PI;
  }
  else theta = atan2(y, x);

  run_tur(theta, omega);
  
  dist_l = r;
  dist_r = r * ratio_dis_RperL;
  vel_l = vel;
  vel_r = vel;
  

  delay(1000);
  run_st(vel_l, dist_l, vel_r, dist_r);
  
}

void run_st(float L_velocity, float L_displacement, float R_velocity, float R_displacement) {
  control_initialize(L_velocity, R_velocity, L_displacement, R_displacement, &target_velocity_l, &target_velocity_r, &target_displacement_l, &target_displacement_r);
  while(1){
    encoder_get(&displacement_l, &displacement_r);
    control_calculate_velocity(displacement_l, displacement_r, &velocity_l, &velocity_r);
    PID_velocity(target_velocity_l, target_velocity_r, velocity_l, velocity_r, &pwm_ln_v, &pwm_rn_v);
    PID_displacement(target_displacement_l, target_displacement_r, displacement_l, displacement_r, &pwm_ln_d, &pwm_rn_d);
    control_convolution(pwm_ln_v, pwm_rn_v, pwm_ln_d, pwm_rn_d, target_displacement_l, target_displacement_r, displacement_l, displacement_r, &pwm_l, &pwm_r);
    control_limitter(pwm_l, pwm_r, &pwm_l, &pwm_r);
    
    if(target_displacement_l > 0 && target_displacement_r > 0){
      if(target_displacement_l < displacement_l && target_displacement_r < displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l > 0 && target_displacement_r < 0){
      if(target_displacement_l < displacement_l || target_displacement_r > displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l < 0 && target_displacement_r > 0){
      if(target_displacement_l > displacement_l || target_displacement_r < displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l < 0 && target_displacement_r < 0){
      if(target_displacement_l > displacement_l && target_displacement_r > displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l == 0 && target_displacement_r == 0){
      motor_stop();
      break;
    }
    Serial.print("pwm L : ");
    Serial.print(pwm_l);
    Serial.print(" R : ");
    Serial.println(pwm_r);

    motor_run_l(pwm_l);
    motor_run_r(pwm_r);
    delay(10);
  } 
}

void run_tur(float angle, float ang_vel) {
  float L_velocity, R_velocity, L_displacement, R_displacement;

  if((-PI <= angle) && (angle <= 0)){
    L_velocity      = 0.5 * ang_vel;
    R_velocity      = -0.5 * ang_vel;
    L_displacement  = -(one_round_meter * angle / 2 / PI);
    R_displacement  = -(-one_round_meter * angle / 2 / PI);
  }
  else if((0 < angle) && (angle <= (PI))){
    L_velocity      = -0.5 * ang_vel;
    R_velocity      = 0.5 * ang_vel;
    L_displacement  = -one_round_meter * angle / 2 / PI;
    R_displacement  = one_round_meter * angle / 2 / PI;
  }

  
  
  control_initialize(L_velocity, R_velocity, L_displacement, R_displacement, &target_velocity_l, &target_velocity_r, &target_displacement_l, &target_displacement_r);
  while(1){
    encoder_get(&displacement_l, &displacement_r);
    control_calculate_velocity(displacement_l, displacement_r, &velocity_l, &velocity_r);
    PID_velocity(target_velocity_l, target_velocity_r, velocity_l, velocity_r, &pwm_ln_v, &pwm_rn_v);
    PID_displacement(target_displacement_l, target_displacement_r, displacement_l, displacement_r, &pwm_ln_d, &pwm_rn_d);
    control_convolution(pwm_ln_v, pwm_rn_v, pwm_ln_d, pwm_rn_d, target_displacement_l, target_displacement_r, displacement_l, displacement_r, &pwm_l, &pwm_r);
    control_limitter(pwm_l, pwm_r, &pwm_l, &pwm_r);
    
    if(target_displacement_l > 0 && target_displacement_r > 0){
      if(target_displacement_l < displacement_l && target_displacement_r < displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l > 0 && target_displacement_r < 0){
      if(target_displacement_l < displacement_l || target_displacement_r > displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l < 0 && target_displacement_r > 0){
      if(target_displacement_l > displacement_l || target_displacement_r < displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l < 0 && target_displacement_r < 0){
      if(target_displacement_l > displacement_l && target_displacement_r > displacement_r){
        motor_stop();
        break;
      }
    }
    if(target_displacement_l == 0 && target_displacement_r == 0){
      motor_stop();
      break;
    }

    

    /*Serial.print("    target displacement L : ");
    Serial.print(target_displacement_l);
    Serial.print("mm    target displacement R : ");
    Serial.print(target_displacement_r);
    Serial.print("mm");
    
    Serial.print("    displacement L : ");
    Serial.print(displacement_l);
    Serial.print("mm  R : ");
    Serial.print(displacement_r);
    Serial.print("mm");
    
    /*Serial.print("    target velocity L : ");
    Serial.print(target_velocity_l);
    Serial.print("mm/s    target velocity R : ");
    Serial.print(target_velocity_r);
    Serial.print("mm/s");
    /*
    Serial.print("    velocity L : ");
    Serial.print(velocity_l);
    Serial.print("mm/s  R : ");
    Serial.print(velocity_r);
    */Serial.print("mm/s    pwm L : ");
    Serial.print(pwm_l);
    Serial.print(" R : ");
    Serial.print(pwm_r);
    
    Serial.println();
    
    
    
    motor_run_l(pwm_l);
    motor_run_r(pwm_r);
    delay(10);
  }
}


void test_tension_adjustment(){
  while(1){
    digitalWrite(PIN_DIR_L, LOW);
    analogWrite(PIN_PWM_L, 50);
    digitalWrite(PIN_DIR_R, HIGH);
    analogWrite(PIN_PWM_R, 50);
  }
}
