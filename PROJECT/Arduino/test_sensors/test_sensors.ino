#define S0 5   // GPIO5
#define S1 4   // GPIO4
#define S2 14  // GPIO14
#define S3 12  // GPIO12
#define EN 15  // GPIO15
#define SIG 13 // GPIO13 (например, цифровой вход D7)

void setup() {
  Serial.begin(9600);

  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);

  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW); // Включаем мультиплексор

  pinMode(SIG, INPUT);   // Цифровой вход для сигнала с мультиплексора

  delay(100);
}

void loop() {
  for(int i = 0; i < 16; i++) {
    int state = readMux(i);
    Serial.print("Channel ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(state == HIGH ? "Pressed" : "Not pressed");
  }
  Serial.println();
  delay(500);
}

int readMux(int channel) {
  int controlPin[] = {S0, S1, S2, S3};

  int muxChannel[16][4] = {
    {0,0,0,0}, {1,0,0,0}, {0,1,0,0}, {1,1,0,0},
    {0,0,1,0}, {1,0,1,0}, {0,1,1,0}, {1,1,1,0},
    {0,0,0,1}, {1,0,0,1}, {0,1,0,1}, {1,1,0,1},
    {0,0,1,1}, {1,0,1,1}, {0,1,1,1}, {1,1,1,1}
  };

  for(int i = 0; i < 4; i++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  delay(5); // Небольшая задержка для стабилизации сигнала

  return digitalRead(SIG);
}


