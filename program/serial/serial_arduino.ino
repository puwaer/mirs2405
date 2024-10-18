//raspberry pi → arduino シリアル通信
#define ROWS 3
#define COLS 3

int matrix[ROWS][COLS];

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    receiveMatrix();  // 行列を受信する関数を呼び出す
    printMatrix();    // 行列を表示する関数を呼び出す
  }
}

void receiveMatrix() {
  for (int i = 0; i < ROWS; i++) {
    String line = Serial.readStringUntil('\n');  // 行を受信
    parseLine(line, i);  // 行を解析して行列に格納
  }
}

void parseLine(String line, int row) {
  int index = 0;
  char* token = strtok(line.c_str(), ",");
  while (token != NULL && index < COLS) {
    matrix[row][index] = atoi(token);  // 文字列を整数に変換
    token = strtok(NULL, ",");
    index++;
  }
}

void printMatrix() {
  // 受信した行列の表示（デバッグ用）
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < COLS; j++) {
      Serial.print(matrix[i][j]);
      Serial.print(" ");
    }
    Serial.println();
  }
}
