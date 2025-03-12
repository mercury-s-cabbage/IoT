
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
bool btn_pressed[NCOLS] = {false, false, false};
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

  for(int icol = 0; icol < NCOLS; icol++) {
    btn_pressed[icol] = !digitalRead(col_pins[icol]);
  }
  report_row_states(current_row);

  current_row = (current_row + 1) % NROWS;
}

void report_row_states(int row_number) {
  for(int icol = 0; icol < NCOLS; icol++) {
    if(btn_pressed[icol] == true) {
      Serial.print("Button ");
      Serial.print(1 + icol + NCOLS * row_number);
      Serial.println(" pressed");
    }
  }
}