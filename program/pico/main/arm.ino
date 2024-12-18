

void arm(float _ang1, float _ang2, float _ang3, float _ang4){
  joint4(joint4ID, _ang4, joint4_vel);
  joint3(joint3ID, _ang3, joint3_vel); 
  //joint2(_ang2);
  joint1(_ang1);
  
}

void photoreflector(){
  int photo_check = digitalRead(PIN_PHOTOREFLECTOR);
  raspi_send(4, photo_check, 0, 0, 0);
}

void all_stop(){
  motor_stop();
  joint1_stop();
  joint2_stop();
}