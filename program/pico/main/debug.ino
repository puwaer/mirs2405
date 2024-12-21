float x_coordinate = 0; //[m]
float y_coordinate = 0; //[m]
int arm_debug_count = 0;

void run_debug(){
  x_coordinate = -0.25;
  y_coordinate = 0.0;
  run_To(x_coordinate, y_coordinate); 
}

void arm_debug(){
  while(1){
    arm_debug_count++;
    if(arm_debug_count >= 100){
      Serial.print("POT_R = ");
      Serial.print(analogRead(PIN_JOINT_1_R_POT));
      Serial.print("  POT_L = ");
      Serial.print(analogRead(PIN_JOINT_1_L_POT));
      Serial.print("  POT_2 = ");
      Serial.print(analogRead(PIN_JOINT_2_POT));
      Serial.println();
      arm_debug_count = 0;
    }
    
    int val[4] = {0};
    if (Serial.available() > 0) {
      delay(10);
      for (int i = 0; i < 4; i++) {
        val[i] = Serial.parseInt();    //文字列データを数値に変換
      }
      arm(val[0], val[1], val[2], val[3]);
      while (Serial.available() > 0) {//受信バッファクリア
        char t = Serial.read();
      }
    }
    delay(10);
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
