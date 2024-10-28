void led_high() {
  analogWrite( LED_PIN, 100 );
  delay(1000);
}

void led_low() {
  analogWrite( LED_PIN, 0 );
  delay(1000);
}