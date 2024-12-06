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
  int joint3_ang = 0;
  int joint4_ang = 0;

  while(1){
    arm(-joint1_ang_center, -joint2_ang_center, 0, 0);
    delay(10000);
    while(1){
      if ( Serial.available() ) {
        String str = Serial.readStringUntil('\n');
        int d_angle[4];
        stringToIntValues( str, d_angle, ',' );
        for (int i = 0; i < 4; i++) {
          Serial.print("d_angle[");
          Serial.print(i);
          Serial.print("]=");
          Serial.println(d_angle[i]);
        }
        joint1_ang = d_angle[0];
        joint2_ang = d_angle[1];
        joint3_ang = d_angle[2];
        joint4_ang = d_angle[3];
        break;
      }
    }
    
    
    arm(joint1_ang, joint2_ang, joint3_ang, joint4_ang);
    delay(10000);
    
  }
}

void stringToIntValues(String str, int value[], char delim) {
  int k = 0;
  int j = 0;
  char text[8];

  for (int i = 0; i <= str.length(); i++) {
    char c = str.charAt(i);
    if ( c == delim || i == str.length() ) {
      text[k] = '\0';
      value[j] = atoi(text);
      j++;
      k = 0;
    } else {
      text[k] = c;
      k++;
    }
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
