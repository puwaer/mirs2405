#include "param.h"

void setup() {
  set_pin(); //各ピンの初期化
  Serial.begin(115200);
}

void loop() {
  check_raspy();
}
