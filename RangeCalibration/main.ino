#define echo 3
#define trig 4
#define thePin A0

long int start_T = 0;
long int curr_T = 0;
bool is_trigged = false;
const int max_T = 100;
const float U = 0.03443;
int d1 = 0;
int d2 = 0;
bool is_rec = false;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(echo), echo_catch, FALLING);
  Serial.begin(9600);
}

void echo_catch()
{
  is_rec = true;
}

void loop() {

  // Считываем консоль, если t - даём сигнал
  if (Serial.available() > 0)
  {
    String ans = "";
    ans = Serial.readString();
    ans.trim();
    if (ans == "t")
    {
      start_T = micros();
      digitalWrite(trig, HIGH); // trig HIGH
      is_trigged = true;
    }
  }

  // Отправляем данные
  if (is_rec == true)
  {
    is_rec = false;
    is_trigged = false; 
    digitalWrite(trig, LOW); // trig LOW
    d1 = (curr_T - start_T)/2.0*U;
    d2 = analogRead(thePin);

    d1 = constrain(static_cast<int>(d1), 0, 1023);
    d2 = constrain(static_cast<int>(d2), 0, 1023);
    char message[9];
    snprintf(message, sizeof(message), "%04d%04d", d1, d2);
    Serial.println(message);
  }

  // Проверка на таймаут
  curr_T = micros();
  if (is_trigged && (curr_T - start_T >= max_T))
  {
      digitalWrite(trig, LOW); // trig TIMEOUT LOW
      is_trigged = false;
  }

}
