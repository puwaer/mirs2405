float x_coordinate = 0; //[m]
float y_coordinate = 0; //[m]

void run_debug(){
  x_coordinate = -0.25;
  y_coordinate = 0.0;
  run_To(x_coordinate, y_coordinate); 
}

void arm_debug(){
  int joint1_ang = 0;
  int joint2_ang = 0;
  int joint3_ang = 180;
  int joint4_ang = 180;
  while(1){
    arm(0, 0, 0, 0);
    delay(10000);
    arm(joint1_ang, joint2_ang, joint3_ang, joint4_ang);
    delay(10000);
  }
}

void radicon_debug(){
  while(1){
    while(!Serial.available());
    String n = Serial.readString();   
    int A = n.toInt();
    while(!Serial.available());
    n = Serial.readString();   
    int C = n.toInt();
    while(!Serial.available());
    n = Serial.readString();   
    int F = n.toInt();
    
    radicon(A, C, F);
    
  }
  
}

void show_XXX(){
  
}
