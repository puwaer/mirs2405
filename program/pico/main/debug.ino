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
  int joint3_ang = 30;
  int joint4_ang = 30;

  /*arm(joint1_ang, joint2_ang, joint3_ang, joint4_ang);
  delay(100000);*/

  while(1){
    arm(0, -45, 0, 0);
    delay(20000);
    arm(0, 0, joint3_ang, joint4_ang);
    delay(20000);
    arm(0, 45, 0, 0);
    delay(20000);
    arm(0, 0, joint3_ang, joint4_ang);
    delay(20000);
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

void show_XXX(){
  
}
