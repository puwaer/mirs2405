#include "define.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
//#include <arduino.h>

void setup() {
  encoder_open();
  motor_open();
  arm_open();
  analogWriteRange(PWM_MAX);
  Serial.begin(115200);
  Serial.setTimeout(10);
  delay(100);

  //raspi_open();
}

void loop(){
  while(1){
    raspi_receive();
    delay(200);
  }

  /*while(1){
    raspi_send(4,2,1800,1800,0);
    delay(10);
  }*/

  /*while(1){
    joint4(joint3ID, 0, 1);
    delay(10);
  }:/
  /*arm(0, 0, 0, 0);
  delay(2000);
  arm(-15, 180, 0, 0);
  delay(1000);
  arm(-21, 180, 0, 0);
  delay(1000);
  //pomp
  delay(5000);
  arm(-15, 90, 90, -180);

  while(1)
  */
  
  
  
  
  //run_debug();
  //arm_debug();
  //radicon();

  /*while(1){
    digitalWrite(PIN_JOINT_1_R_DIR, HIGH);
    digitalWrite(PIN_JOINT_2_DIR, HIGH);
  }*/

  //joint2(0);
  //delay(10000);
  /*joint1_R_run(-200);
  delay(5000);
  joint1_R_run(0);
  delay(1000);
  joint1_R_run(200);
  delay(5000);*/
  
  joint1_stop();
  joint2_stop();
  motor_stop();
  exit(0);
}

/*  run(x, y)  (x,y)へ移動

    arm(ang1, ang2, ang3, ang4) アームを指定角度へ　すべて絶対角度
      ang1: -75~75[°]
      ang2: -10~190[°]
      ang3,4: -150~150[°]

    radicon(bool _check) 
      _check  :   trueならラジコン動作オン
                  falseならオフ
      A, C :  1100 - 1900 1200以下:前進 1700以上:後退
      F    :　1500以下:通常 1900以上:押し込み
      Fを押した回数
      　0:走行 1:グリッパー、ターンテーブル 2:一、二関節 3:三、四関節
      

*/
