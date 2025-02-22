

void arm(float _ang1, float _ang2, float _ang3, float _ang4){
  joint1(_ang1);
  joint2(_ang2);
  joint3(joint3ID, _ang3, joint3_vel); 
  joint4(joint4ID, _ang4, joint4_vel);
}

void get(float _ang1, float _ang2, float _ang3, float _ang4){
  arm(-11, 0, 0, 0);
  delay(10000);
  arm(-11, 170, 0, 0);
  delay(1000);
  arm(-13, 172, 0, 0);
  delay(1000);
  arm(-26, 172, 0, 0);
  raspi_send(6, 6, 0, 0, 0, 0, 0);
  delay(2000);
  //arm(-15, 90, 90, -160);
  arm(_ang1, _ang2, _ang3, _ang4);
}

void photoreflector(){
  int photo_check = digitalRead(PIN_PHOTOREFLECTOR);
  raspi_send(5, photo_check, 0, 0, 0, 0, 0);
}

void all_stop(){
  motor_stop();
  joint1_stop();
  joint2_stop();
}

float mapf(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
