#define BUTTON_PIN 2 
#define BOUNCE_TIME 50
#define PRESSED HIGH
volatile long int press_time = 0;
volatile bool pressed_candidate = false;
volatile long int hold_time = 0;
volatile int press_count = 0;
volatile bool report_to_user = false;
bool button_pressed = false;

void setup() {
  pinMode(BUTTON_PIN, INPUT);
  Serial.begin(9600);
  // When BUTTON_PIN turns pressed, the function will start
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), process_button_click, RISING);
}

void loop() {

  if(report_to_user == true) {
    Serial.println("Press candidate");
    report_to_user = false;
  }
  
  hold_time = millis();

  // more than 50ms since prev press
  if(press_time - hold_time >= BOUNCE_TIME) 
  {
      pressed_candidate = false;
      press_count += 1;
      Serial.println("Press count = ");
      Serial.println(press_count);
      press_time = 0;
  }
}

void process_button_click() {
  if (pressed_candidate == false) // if it's first press
  {
    press_time = millis();
    pressed_candidate = true;
    report_to_user = true;
    hold_time = 0;
  }
}