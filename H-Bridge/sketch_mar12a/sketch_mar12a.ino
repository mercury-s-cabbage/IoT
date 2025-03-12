#define FORWARD_PIN 4
#define BACKWARD_PIN 2
#define SPEED_PIN 6


void setup() {
  pinMode(FORWARD_PIN, OUTPUT);
  digitalWrite(FORWARD_PIN, LOW);

  pinMode(BACKWARD_PIN, OUTPUT);
  digitalWrite(BACKWARD_PIN, LOW);

  pinMode(SPEED_PIN, OUTPUT);
  digitalWrite(SPEED_PIN, 0);

  Serial.begin(9600);
  Serial.println("Enter direction (1 - forward, 2 - backward, 0 - stop) and speed (0-255):");
}

void rotate(int direction, int speed){
  speed = constrain(speed, 0, 255);

  switch (direction) {
    case 1:
      digitalWrite(BACKWARD_PIN, LOW);
      digitalWrite(FORWARD_PIN, HIGH);
      break;

    case 2:
      digitalWrite(FORWARD_PIN, LOW);
      digitalWrite(BACKWARD_PIN, HIGH);
      break;

    default:
      digitalWrite(FORWARD_PIN, LOW);
      digitalWrite(BACKWARD_PIN, LOW);
      speed = 0;
  }
  analogWrite(SPEED_PIN, speed);
}


void loop() {
    if (Serial.available() > 0) {
    int direction, speed;
    
    direction = Serial.parseInt();
    speed = Serial.parseInt();
    
    while (Serial.available()) Serial.read();
    rotate(direction, speed);    

  }
}