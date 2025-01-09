static float err_velocity_l;
static float err_velocity_r;
static float integral_velocity_l;
static float integral_velocity_r;
static float differential_velocity_l;
static float differential_velocity_r;
static float pre_err_velocity_l;
static float pre_err_velocity_r;
static float pwm_l_v;
static float pwm_r_v;

static float err_displacement_l;
static float err_displacement_r;
static float integral_displacement_l;
static float integral_displacement_r;
static float differential_displacement_l;
static float differential_displacement_r;
static float pre_err_displacement_l;
static float pre_err_displacement_r;
static float pwm_l_d;
static float pwm_r_d;

void PID_reset(){
  err_velocity_l = 0.0;
  err_velocity_r = 0.0;
  integral_velocity_l = 0.0;
  integral_velocity_r = 0.0;
  differential_velocity_l = 0.0;
  differential_velocity_r = 0.0;
  pre_err_velocity_l = 0.0;
  pre_err_velocity_r = 0.0;
  pwm_l_v = 0.0;
  pwm_r_v = 0.0;

  err_displacement_l = 0.0;
  err_displacement_r = 0.0;
  integral_displacement_l = 0.0;
  integral_displacement_r = 0;
  differential_displacement_l = 0.0;
  differential_displacement_r = 0.0;
  pre_err_displacement_l = 0.0;
  pre_err_displacement_r = 0.0;
  pwm_l_d = 0.0;
  pwm_r_d = 0.0;
}

void PID_velocity(float a, float b, float c, float d, int *e, int *f){
  err_velocity_l = a - c;
  integral_velocity_l += (err_velocity_l + pre_err_velocity_l) * (control_period / 2000.0);
  differential_velocity_l = (err_velocity_l - pre_err_velocity_l) / (control_period / 1000.0);
  pwm_l_v = Kp_velocity_l * err_velocity_l + Ki_velocity_l * integral_velocity_l + Kd_velocity_l * differential_velocity_l;
  *e = (int)(pwm_l_v + 0.5);
  if(*e > 0){
    *e = *e + 30;
  }
  if(*e < 0){
    *e = *e - 30;
  }
  pre_err_velocity_l = err_velocity_l;

  err_velocity_r = b - d;
  integral_velocity_r += (err_velocity_r + pre_err_velocity_r) * (control_period / 2000.0);
  differential_velocity_r = (err_velocity_r - pre_err_velocity_r) / (control_period / 1000.0);
  pwm_r_v = Kp_velocity_r * err_velocity_r + Ki_velocity_r * integral_velocity_r + Kd_velocity_r * differential_velocity_r;
  *f = (int)(pwm_r_v + 0.5);
  if(*f > 0){
    *f = *f + 30;
  }
  if(*f < 0){
    *f = *f - 30;
  }
  pre_err_velocity_r = err_velocity_r;
}

void PID_displacement(float a, float b, float c, float d, int *e, int *f){
  err_displacement_l = a - c;
  integral_displacement_l += (err_displacement_l + pre_err_displacement_l) * (control_period / 2000.0);
  differential_displacement_l = (err_displacement_l - pre_err_displacement_l) / (control_period / 1000.0);
  pwm_l_d = Kp_displacement_l * err_displacement_l + Ki_displacement_l * integral_displacement_l + Kd_displacement_l * differential_displacement_l;
  *e = (int)(pwm_l_d + 0.5);
  pre_err_displacement_l = err_displacement_l;

  err_displacement_r = b - d;
  integral_displacement_r += (err_displacement_r + pre_err_displacement_r) * (control_period / 2000.0);
  differential_displacement_r = (err_displacement_r - pre_err_displacement_r) / (control_period / 1000.0);
  pwm_r_d = Kp_displacement_r * err_displacement_r + Ki_displacement_r * integral_displacement_r + Kd_displacement_r * differential_displacement_r;
  *f = (int)(pwm_r_d + 0.5);
  pre_err_displacement_r = err_displacement_r;
}
