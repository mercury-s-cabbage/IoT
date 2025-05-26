#include <SoftwareSerial.h>
SoftwareSerial BTSerial(10, 11); // tx 10, rx 11

// Pins to move
#define LEFT_DIR_PIN 7
#define LEFT_SPEED_PIN 6
#define RIGHT_DIR_PIN 4
#define RIGHT_SPEED_PIN 5

// Pins to get distance
#define TRIG_FRONT_PIN 2
#define ECHO_FRONT_PIN 3
#define TRIG_RIGHT_PIN 8
#define ECHO_RIGHT_PIN 9

float distance_front = 0.0;
float distance_right = 0.0;
int front_min = 30;
int right_min = 30;
int right_max = 70;
int step_time = 1;

int state = 1;
int counter = 0;

int left_speed = 160;
int right_speed = 160;

bool calibration_mode = false;
bool move_mode = false;
bool state_mode = false;
bool wheels_mode = false;
String wheel = "l";

const int num_moves = 4;
bool move_dirs[num_moves][2] = {
  {HIGH, LOW},
  {LOW, HIGH},
  {LOW, LOW},
  {HIGH, HIGH}
};

void move(bool left_dir, int left_speed, bool right_dir, int right_speed) {
  digitalWrite(LEFT_DIR_PIN, left_dir);
  analogWrite(LEFT_SPEED_PIN, left_speed);
  digitalWrite(RIGHT_DIR_PIN, right_dir);
  analogWrite(RIGHT_SPEED_PIN, right_speed);
}

void stop() {
  move(0, 0, 0, 0);
}

void move_calibrated(int idx, int left_speed, int right_speed) {
  move(move_dirs[idx][0], left_speed, move_dirs[idx][1], right_speed);
}

int get_button_index(char c) {
  switch (c) {
    case 'F': return 0;
    case 'B': return 1;
    case 'L': return 2;
    case 'R': return 3;
    default: return -1;
  }
}

int toggle_phase[num_moves] = { 0, 1, 2, 3 }; // Front, Back, Left, Right

float getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.0343 / 2.0;
  return distance;
}

void setup() {
  for (int i = 4; i <= 7; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }

  pinMode(TRIG_FRONT_PIN, OUTPUT);
  pinMode(ECHO_FRONT_PIN, INPUT);
  pinMode(TRIG_RIGHT_PIN, OUTPUT);
  pinMode(ECHO_RIGHT_PIN, INPUT);

  Serial.begin(9600);
  while (!Serial) { }
  BTSerial.println("Seril done.");

  BTSerial.begin(9600);
  Serial.println("Bluetooth ready.");
}

void loop() {
  if (Serial.available()) {
    BTSerial.write(Serial.read());
  }

  if (BTSerial.available()) {
    char cmd = BTSerial.read();
    // Serial.write(cmd);
    Serial.print("Received: ");
    Serial.println(cmd);

    if (cmd == 'X') {
      calibration_mode = !calibration_mode;
      move_mode = false;
      wheels_mode = false;
      state_mode = false;
      Serial.println(calibration_mode ? "Calibration mode ON" : "Calibration mode OFF");
    }
    else if (cmd == 'S') {
      move_mode = !move_mode;
      calibration_mode = false;
      wheels_mode = false;
      state_mode = false;
      Serial.println(move_mode ? "Move mode ON" : "Move mode OFF");
    }
    else if (cmd == 'C') {
      wheels_mode = !wheels_mode;
      calibration_mode = false;
      move_mode = false;
      state_mode = false;
      Serial.println(wheels_mode ? "Wheels mode ON" : "Wheels mode OFF");
    }
    else if (cmd == 'T') {
      state_mode = !state_mode;
      calibration_mode = false;
      move_mode = false;
      wheels_mode = false;
      Serial.println(state_mode ? "State mode ON" : "State mode OFF");
    }

    // mode to calibrate move destination
    else if (calibration_mode) {
      int idx = get_button_index(cmd);
      Serial.print("button id: ");
      Serial.println(idx);
      if (idx >= 0) {
        toggle_phase[idx] = (toggle_phase[idx] + 1) % num_moves;

        Serial.print("Calibrated button ");
        Serial.print(cmd);

        move_calibrated(toggle_phase[idx], left_speed, right_speed);
        delay(400);
        stop();
      }
    }

    // mode to move by buttons
    else if (move_mode) {
      int idx = get_button_index(cmd);
      Serial.print("button id: ");
      Serial.println(idx);
      if (idx >= 0) {
        move_calibrated(toggle_phase[idx], left_speed, right_speed);
        delay(400);
        stop();
      }
    }

    // mode to calibrate wheel speed
    else if (wheels_mode){
      int idx = get_button_index(cmd);
      Serial.print("button id: ");
      Serial.println(idx);

      // switch to left wheel
      if (idx == 2) {
        wheel = "l";
      }
      // switch to right wheel
      if (idx == 3) {
        wheel = "r";
      }

      if (idx >= 0 and idx < 2){
        // faster
        if (idx == 0){
          if (wheel == "l") {
            left_speed += 10;
            if (left_speed > 260){
              left_speed = 260;
            }
          }
          if (wheel == "r") {
            right_speed += 10;
            if (right_speed > 260){
              right_speed = 260;
            }
          }
        }

        // slower
        if (idx == 1){
          if (wheel == "l") {
            left_speed -= 10;
            if (left_speed < 100){
              left_speed = 100;
            }
          }
          if (wheel == "r") {
            right_speed -= 10;
            if (right_speed < 100){
              right_speed = 100;
            }
          }
        }
        Serial.print("left: ");
        Serial.println(left_speed);
        Serial.print("right: ");
        Serial.println(right_speed);

        move_calibrated(toggle_phase[0], left_speed, right_speed);
        delay(400);
        stop();
      }
    }
  }
  // mode to move as state machine
  else if (state_mode) {
    distance_front = getDistance(TRIG_FRONT_PIN, ECHO_FRONT_PIN);
    distance_right = getDistance(TRIG_RIGHT_PIN, ECHO_RIGHT_PIN);
    // Serial.print("right:");
    // Serial.println(distance_right);
    // Serial.print("front:");
    // Serial.println(distance_front);

    // to close to right
    if (state == 1 and distance_front > front_min and distance_right < right_min){
      move_calibrated(toggle_phase[2], left_speed, right_speed);
      state = 2;
      counter = 1;
    }
    else if (state == 2 and distance_right < right_min and counter % 3 == 0){
      move_calibrated(toggle_phase[0], left_speed, right_speed);
      counter += 1;
    }
    else if (state == 2 and distance_right < right_min and counter % 3 > 0){
      move_calibrated(toggle_phase[2], left_speed, right_speed);
      counter += 1;
    }
    else if (state == 2 and distance_right >= right_min){
      move_calibrated(toggle_phase[3], left_speed, right_speed);
      state = 1;
      counter = 0;
    }

    // before wall
    else if (state == 1 and distance_front <= front_min){
      move_calibrated(toggle_phase[2], left_speed, right_speed);
      state = 3;
      counter = 1;
    }
    else if (state == 3 and distance_front <= front_min){
      move_calibrated(toggle_phase[2], left_speed, right_speed);
      counter += 1;
    }
    else if (state == 3 and distance_front > front_min){
      move_calibrated(toggle_phase[3], left_speed, right_speed);
      state = 1;
      counter = 0;
    }

    // no wall on right
    if (state == 1 and distance_front > front_min and distance_right > right_max){
      move_calibrated(toggle_phase[3], left_speed, right_speed);
      state = 4;
      counter = 1;
    }
    else if (state == 4 and distance_right > right_max and counter % 3 == 0){
      move_calibrated(toggle_phase[0], left_speed, right_speed);
      counter += 1;
    }
    else if (state == 4 and distance_right > right_max and counter % 3 > 0){
      move_calibrated(toggle_phase[3], left_speed, right_speed);
      counter += 1;
    }
    else if (state == 4 and distance_right >= right_max){
      move_calibrated(toggle_phase[2], left_speed, right_speed);
      state = 1;
      counter = 0;
    }


    // all ok and we need to move forward
    else if (state == 1){
      move_calibrated(toggle_phase[0], left_speed, right_speed);
    }

    // reset if we are stuck in cycle
    if (counter >= 10){
      state = 1;
      counter = 0;
    }
    delay(step_time);
  }
}