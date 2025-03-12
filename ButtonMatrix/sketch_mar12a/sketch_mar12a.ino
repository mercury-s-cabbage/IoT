
#define ROW1 2
#define ROW2 3
#define ROW3 4

#define COL1 5
#define COL2 6
#define COL3 7

#define NROWS 3
#define NCOLS 3
#define SCAN_INTERVAL 10 

const int row_pins[NROWS] = {2, 3, 4};
const int col_pins[NCOLS] = {5, 6, 7};
bool btn_pressed[NROWS][NCOLS] = {{false, false, false}, {false, false, false}, {false, false, false}};
bool prev_btn_pressed[NROWS][NCOLS] = {{false, false, false}, {false, false, false}, {false, false, false}};
unsigned long press_start_time[NROWS][NCOLS] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
volatile uint8_t current_row = 0;

void setup_timer() {
  cli(); // Остановить прерывания
  TCCR1A = 0; 
  TCCR1B = (1 << WGM12) | (1 << CS12); 
  OCR1A = (F_CPU / 256 / 1000) * SCAN_INTERVAL - 1; 
  TIMSK1 |= (1 << OCIE1A); 
  sei(); // Включить прерывания
}

void setup()
{
  for(int i = 0;i < NROWS; i++) {
    pinMode(row_pins[i], OUTPUT);
  }
  for(int i = 0;i < NCOLS; i++) {
    pinMode(col_pins[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
    setup_timer();
}

void loop()
{
}

ISR(TIMER1_COMPA_vect) {
  for(int i = 0; i < NROWS; i++) {
    digitalWrite(row_pins[i], HIGH);
  }
  digitalWrite(row_pins[current_row], LOW);

  bool state_changed = false;
  unsigned long current_time = millis();

  for(int icol = 0; icol < NCOLS; icol++) {
    bool is_pressed = !digitalRead(col_pins[icol]);
    if (is_pressed && !prev_btn_pressed[current_row][icol]) {
      press_start_time[current_row][icol] = current_time;
    }
    if (!is_pressed && prev_btn_pressed[current_row][icol]) {
      Serial.print("Button ");
      Serial.print(1 + icol + NCOLS * current_row);
      Serial.print(" duration: ");
      Serial.print(current_time - press_start_time[current_row][icol]);
      Serial.print(" ms, started at: ");
      Serial.println(press_start_time[current_row][icol]);
    }
    btn_pressed[current_row][icol] = is_pressed;
    if (btn_pressed[current_row][icol] != prev_btn_pressed[current_row][icol]) {
      state_changed = true;
    }
  }
  
  if (state_changed) {
    report_button_states();
  }

  memcpy(prev_btn_pressed, btn_pressed, sizeof(btn_pressed));
  current_row = (current_row + 1) % NROWS;
}

void report_button_states() {
  Serial.print("Pressed buttons: ");
  bool any_pressed = false;
  for (int irow = 0; irow < NROWS; irow++) {
    for (int icol = 0; icol < NCOLS; icol++) {
      if (btn_pressed[irow][icol]) {
        Serial.print(1 + icol + NCOLS * irow);
        Serial.print(" ");
        any_pressed = true;
      }
    }
  }
  if (!any_pressed) {
    Serial.print("None");
  }
  Serial.println();
}
