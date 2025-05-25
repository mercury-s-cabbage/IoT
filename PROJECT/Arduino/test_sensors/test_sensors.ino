const int buttonPins[] = {13};  
const int numButtons = sizeof(buttonPins);  
int loopstate=0;
void setup() {
  Serial.begin(9600);
  
  for (int i = 0; i < numButtons; i++) {
    pinMode(buttonPins[i], INPUT);
  }
}

void loop() {
  bool anyActive = false; 
  loopstate=loopstate+1;
  for (int i = 0; i < numButtons; i++) {
    int state = digitalRead(buttonPins[i]);
      Serial.print(loopstate);
      Serial.print(" ");
      Serial.print("Pin ");
      Serial.print(buttonPins[i]);
      Serial.print(" ");
      Serial.println(state);
      anyActive = true;
    
  }
  
  delay(800);
}