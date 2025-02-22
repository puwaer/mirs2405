#include "define.h"

void setup() {
  Serial.begin(115200);
  rc_init();
  
}

void loop() {
  raspi_receive();
  send_rc();
  exit(0);
}
