#include "define.h"

void setup() {
  Serial.begin(115200);
  rc_init();
  
}

void loop() {
  /*while(1){
    raspi_receive();
  }*/

  while(1){
    send_rc();
  }

  exit(0);
}
