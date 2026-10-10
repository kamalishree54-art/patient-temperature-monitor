#include <math.h>

const int NTC_PIN = A0;
const int BUZZER_PIN = 8;

const float BETA = 3950.0;
const float R0 = 10000.0;
const float T0 = 298.15;

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println("Patient Temperature Monitor");
  Serial.println("---------------------------");
}

void loop() {

  int analogValue = analogRead(NTC_PIN);

  // Calculate NTC resistance
  float resistance = R0 * (1023.0 / analogValue - 1.0);

  // Calculate temperature
  float temperature =
    1.0 / (1.0 / T0 + log(resistance / R0) / BETA) - 273.15;

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // Fever threshold
  if (temperature >= 36.0) {
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("FEVER ALERT! Buzzer ON");
  }
  else {
    digitalWrite(BUZZER_PIN, LOW);
    Serial.println("Normal - Buzzer OFF");
  }

  Serial.println();
  delay(1000);
}