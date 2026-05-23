#define MOTOR 3

char signal;

int speedMotor = 90;

void setup() {

  Serial.begin(9600);

  pinMode(MOTOR, OUTPUT);

  stopMotor();

}

void loop() {

  if (Serial.available() > 0) {

    signal = Serial.read();

    if (signal == '1') {

      openCurtain();

    }

  }

}

void openCurtain() {

  // плавное открытие
  analogWrite(MOTOR, speedMotor);

  // работа 3 секунды
  delay(500);

  // остановка
  stopMotor();

}

void stopMotor() {

  analogWrite(MOTOR, 0);

}