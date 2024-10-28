#include "define.h"
int mode = 0;
volatile unsigned long startPulse[8];  //
volatile int getPulse[8];  //取得したパルスを格納する配列

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(MR8_A_PIN,INPUT);
  pinMode(MR8_B_PIN,INPUT);
  pinMode(MR8_C_PIN,INPUT);
  pinMode(MR8_D_PIN,INPUT);
  pinMode(MR8_E_PIN,INPUT);
  pinMode(MR8_F_PIN,INPUT);
  pinMode(MR8_G_PIN,INPUT);
  pinMode(MR8_H_PIN,INPUT);
  Serial.begin(115200);
  attachInterrupt(MR8_A_PIN,chAChangeInterupt,CHANGE);  //端子に変化があった時に割り込み
}

void loop() {
  chAChangeInterupt();
  serial();
  /*if(mode = 1){
    led_high();
  }
  else led_low();*/
}
