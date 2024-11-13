

void send() {
  int values[] = {a, c, e, f, g, h}; // 送信する整数型の配列

  // 各要素を1回ずつ送信
  for (int i = 0; i < 6; i++) {
      Serial.write((uint8_t *)&values[i], sizeof(values[i]));
      delay(100); // 送信の間に短い待機時間を追加
  }

  delay(100); // 待機してから再送信
}
