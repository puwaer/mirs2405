float target_ang_joint1;
float angle_joint1;

float err_ang_joint1;
float integral_ang_joint1;
float differential_ang_joint1;
float pre_err_ang_joint1;
int joint1_pwm;

void joint1_initialize(float a, float *b){
  PID_reset_joint1();
  joint1_stop();

  *b = a;
}

void joint1_limitter(int a, int *b){
  if(a > joint1_pwm_limitter_H){
    *b = joint1_pwm_limitter_H;
  }
  else if(a < joint1_pwm_limitter_L){
    *b = joint1_pwm_limitter_L;
  }
  else if(0 < a && a < joint1_dead_zone){
    *b = joint1_dead_zone;
  }
  else if(-joint1_dead_zone < a && a < 0){
    *b = -joint1_dead_zone;
  }
  else{
    *b = a;
  }
}

void PID_reset_joint1(){
  err_ang_joint1 = 0.0;
  integral_ang_joint1 = 0.0;
  differential_ang_joint1 = 0.0;
  pre_err_ang_joint1 = 0.0;
  joint1_pwm = 0.0;
}

void PID_joint1(float a, float b, int *c){
  err_ang_joint1 = a - b;
  integral_ang_joint1 += (err_ang_joint1 + pre_err_ang_joint1) * (control_period / 2000.0);
  differential_ang_joint1 = (err_ang_joint1 - pre_err_ang_joint1) / (control_period / 1000.0);
  joint1_pwm = Kp_joint1 * err_ang_joint1 + Ki_joint1 * integral_ang_joint1 + Kd_joint1 * differential_ang_joint1;
  *c = (int)(joint1_pwm + 0.5);
  pre_err_ang_joint1 = err_ang_joint1;
}

void joint1(float _angle) {
  joint1_initialize(_angle, &target_ang_joint1);
  while(1){
    angle_joint1 = analogRead(PIN_JOINT_1_POT);
    angle_joint1 = map(angle_joint1, 0, 1023, POT_MIN, POT_MAX);
    PID_joint1(target_ang_joint1, angle_joint1, &joint1_pwm);
    joint1_limitter(joint1_pwm, &joint1_pwm);

    if(abs(target_ang_joint1) < abs(angle_joint1)){
      joint1_stop();
      break;
    }
    if(target_ang_joint1 == 0){
      joint1_stop();
      break;
    }

    joint1_R_run(joint1_pwm);
    joint1_L_run(-joint1_pwm);

    delay(10);
  } 
}

void joint1_stop(){
  analogWrite(PIN_JOINT_1_R_PWM, 0);
  analogWrite(PIN_JOINT_1_R_PWM, 0);
}

void joint1_R_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_R_DIR, HIGH);
    analogWrite(PIN_JOINT_1_R_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_R_DIR, LOW);
    analogWrite(PIN_JOINT_1_R_PWM, _pwm);
  }
  else{
    analogWrite(PIN_JOINT_1_R_PWM, 0);
  }
}

void joint1_L_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_L_DIR, HIGH);
    analogWrite(PIN_JOINT_1_L_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_L_DIR, LOW);
    analogWrite(PIN_JOINT_1_L_PWM, _pwm);
  }
  else{
    analogWrite(PIN_JOINT_1_L_PWM, 0);
  }
}

