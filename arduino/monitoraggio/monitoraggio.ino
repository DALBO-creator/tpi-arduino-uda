/**
 * Sistema di Monitoraggio Efficienza Energetica
 * UdA Sostenibilità Ambientale
 */

#include <LiquidCrystal.h>
#include <DHT.h>

#define DHT_PIN 8
#define DHT_TYPE DHT11
#define LED_VERDE 12
#define LED_ROSSO 13
#define TEMP_MIN 18.0
#define TEMP_MAX 25.0
#define INTERVALLO 2000

LiquidCrystal lcd(11, 10, 6, 5, 4, 3);
DHT dht(DHT_PIN, DHT_TYPE);
unsigned long ultimaLettura = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROSSO, OUTPUT);
  
  lcd.begin(16, 2);
  lcd.print("Avvio...");
  dht.begin();
  
  digitalWrite(LED_VERDE, HIGH);
  digitalWrite(LED_ROSSO, HIGH);
  delay(1000);
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROSSO, LOW);
  delay(500);
  lcd.clear();
}

void loop() {
  if (millis() - ultimaLettura < INTERVALLO) return;
  ultimaLettura = millis();
  
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();
  
  if (isnan(temp) || isnan(umid)) {
    Serial.println("ERR:SENSOR");
    lcd.setCursor(0, 0);
    lcd.print("Errore sensore! ");
    return;
  }
  
  Serial.print(temp, 1);
  Serial.print(",");
  Serial.println(umid, 1);
  
  digitalWrite(LED_ROSSO, temp > TEMP_MAX);
  digitalWrite(LED_VERDE, temp >= TEMP_MIN && temp <= TEMP_MAX);
  
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temp, 1);
  lcd.print("C U:");
  lcd.print(umid, 0);
  lcd.print("%  ");
  
  lcd.setCursor(0, 1);
  if (temp > TEMP_MAX) lcd.print("! TROPPO CALDO !");
  else if (temp >= TEMP_MIN) lcd.print("OK - Comfort    ");
  else lcd.print("Temp. bassa     ");
}
