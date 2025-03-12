
#define ROW1 2
#define ROW2 3
#define ROW3 4

#define COL1 5
#define COL2 6
#define COL3 7

#define NROWS 3
#define NCOLS 3

const int row_pins[NROWS] = {2, 3, 4};
const int col_pins[NCOLS] = {5, 6, 7};
bool btn_pressed[NCOLS] = {false, false, false};

const int buttons[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

void setup()
{
  for(int i = 0;i < NROWS; i++) {
    pinMode(row_pins[i], OUTPUT);
  }
  for(int i = 0;i < NCOLS; i++) {
    pinMode(col_pins[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
}

void loop()
{
  update_button_state();
  delay(50);
}

void update_button_state() {
  for(int irow = 0; irow < NROWS; irow++) {
    for(int i = 0; i < NROWS; i++) {
      digitalWrite(row_pins[i], HIGH);
    }
    // set the row that we check in LOW 
    digitalWrite(row_pins[irow], LOW);
    for(int icol = 0; icol < NCOLS; icol++) {
      // value inversion to make true correspond to press
      btn_pressed[icol] = !digitalRead(col_pins[icol]);
    }
    report_row_states(irow);
  }
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