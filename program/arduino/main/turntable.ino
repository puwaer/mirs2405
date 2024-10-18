float err_count;
float pre_count;
float target_ang;
float angle;

float err_ang;
float integral_ang;
float differential_ang;
float pre_err_ang;
int pwm;

void turntable_initialize(float a, float *b){
  encoder_reset();
  PID_reset_turntable();
  pre_count = 0.0;
  turntable_stop();

  *b = a;
}

void turntable_limitter(int a, int *b){
  if(a > turntable_pwm_limitter_H){
    *b = turntable_pwm_limitter_H;
  }
  else if(a < turntable_pwm_limitter_L){
    *b = turntable_pwm_limitter_L;
  }
  else if(0 < a && a < turntable_dead_zone){
    *b = turntable_dead_zone;
  }
  else if(-turntable_dead_zone < a && a < 0){
    *b = -turntable_dead_zone;
  }
  else{
    *b = a;
  }
}

void PID_reset_turntable(){
  err_ang = 0.0;
  integral_ang = 0.0;
  differential_ang = 0.0;
  pre_err_ang = 0.0;
  pwm = 0.0;
}

void PID_turntable(float a, float b, int *c){
  err_ang = a - b;
  integral_ang += (err_ang + pre_err_ang) * (control_period / 2000.0);
  differential_ang = (err_ang - pre_err_ang) / (control_period / 1000.0);
  pwm = Kp_turntable * err_ang + Ki_turntable * integral_ang + Kd_turntable * differential_ang;
  *c = (int)(pwm + 0.5);
  pre_err_ang = err_ang;
}

void turntable(float _angle) {
  turntable_initialize(_angle, &target_ang);
  while(1){
    encoder_get(&angle);
    PID_turntable(target_ang, angle, &pwm);
    turntable_limitter(pwm, &pwm);

    if(abs(target_ang) < abs(angle)){
      turntable_stop();
      break;
    }
    if(target_ang == 0){
      turntable_stop();
      break;
    }

    turntable_run(pwm);
  } 
}

void turntable_stop(){
  analogWrite(PIN_TURNTABLE_PWM, 0);
}

void turntable_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_TURNTABLE_DIR, LOW);
    analogWrite(PIN_TURNTABLE_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_TURNTABLE_DIR, HIGH);
    analogWrite(PIN_TURNTABLE_PWM, _pwm);
  }
  else{
    analogWrite(PIN_TURNTABLE_PWM, 0);
  }
}

