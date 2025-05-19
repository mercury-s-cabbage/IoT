const int buttonPins[] = {5, 6, 7};  // массив пинов для сенсорных кнопок
const int numButtons = sizeof(buttonPins) / sizeof(buttonPins[0]);
const int ledPin = LED_BUILTIN;      // встроенный светодиод Arduino

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  
  for (int i = 0; i < numButtons; i++) {
    pinMode(buttonPins[i], INPUT);
  }
}

void loop() {
  bool anyActive = false;  // флаг, чтобы включить светодиод, если хотя бы одна кнопка активна
  
  for (int i = 0; i < numButtons; i++) {
    int state = digitalRead(buttonPins[i]);
    if (state == HIGH) {
      Serial.print("Пин ");
      Serial.print(buttonPins[i]);
      Serial.println(" активен (1)");
      anyActive = true;
    }
  }
  
  digitalWrite(ledPin, anyActive ? HIGH : LOW);
  delay(100);
}
