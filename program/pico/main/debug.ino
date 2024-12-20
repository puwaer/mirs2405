float x_coordinate = 0; //[m]
float y_coordinate = 0; //[m]

void run_debug(){
  x_coordinate = -0.25;
  y_coordinate = 0.0;
  run_To(x_coordinate, y_coordinate); 
}

void arm_debug(){
  int joint1_ang = 30;
  int joint2_ang = 30;
  int joint3_ang = 30;
  int joint4_ang = 30;

  /*arm(joint1_ang, joint2_ang, joint3_ang, joint4_ang);
  delay(100000);*/

  while(1){
    arm(0, 0, 0, 0);
    delay(20000);
    arm(30, 0, joint3_ang, joint4_ang);
    delay(20000);
    arm(30, 30, 0, 0);
    delay(20000);
    arm(0, 30, joint3_ang, joint4_ang);
    delay(20000);
  }

}

/*void radicon_debug(){
  while(1){  
    unsigned int MR8_A = pulseIn(PIN_MR8_A,HIGH);
    unsigned int MR8_C = pulseIn(PIN_MR8_C,HIGH);
    unsigned int MR8_E = pulseIn(PIN_MR8_E,HIGH);
    unsigned int MR8_F = pulseIn(PIN_MR8_F,HIGH);

    /*if(1800 <  MR8_E) MR8_E = 1;
    else              MR8_E = 0;
    
    //raspi_send(4, state, MR8_A, MR8_C, MR8_E);

    if(MR8_E == 1) break;
    
    Serial.print("MR8_A = ");
    Serial.print(MR8_A);
    Serial.print("  MR8_C = ");
    Serial.print(MR8_C);
    Serial.print("  MR8_E = ");
    Serial.print(MR8_E);
    Serial.print("  MR8_F = ");
    Serial.print(MR8_F);
    Serial.println();

    //Serial.println(analogRead(PIN_JOINT_1_R_POT));
    
    //radicon_run(MR8_A, MR8_C, MR8_F);

    delay(10);
  }
  
}*/

void show_XXX(){
  
}
