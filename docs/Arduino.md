# 💻 Codice Arduino

Spiegazione dettagliata del firmware per Arduino.

---

## 📄 File: `monitoraggio.ino`

### Librerie Utilizzate

```cpp
#include <LiquidCrystal.h>  // Gestione display LCD
#include <DHT.h>             // Lettura sensore DHT11
```

---

## ⚙️ Configurazione (Costanti)

```cpp
#define DHT_PIN 8        // Pin dati del sensore
#define DHT_TYPE DHT11   // Tipo di sensore
#define LED_VERDE 12     // Pin LED verde
#define LED_ROSSO 13     // Pin LED rosso
#define TEMP_MIN 18.0    // Soglia minima comfort
#define TEMP_MAX 25.0    // Soglia massima comfort
#define INTERVALLO 2000  // Intervallo lettura (ms)
```

### Come Modificare le Soglie

Per cambiare le soglie di comfort, modifica:
- `TEMP_MIN`: temperatura minima per lo stato "Comfort"
- `TEMP_MAX`: temperatura massima per lo stato "Comfort"

---

## 🔧 Funzione `setup()`

Eseguita **una sola volta** all'avvio:

```cpp
void setup() {
  // 1. Inizializza comunicazione seriale
  Serial.begin(9600);
  
  // 2. Configura i pin dei LED come output
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROSSO, OUTPUT);
  
  // 3. Inizializza il display LCD (16 colonne, 2 righe)
  lcd.begin(16, 2);
  lcd.print("Avvio...");
  
  // 4. Inizializza il sensore DHT11
  dht.begin();
  
  // 5. Test LED (lampeggio di conferma)
  digitalWrite(LED_VERDE, HIGH);
  digitalWrite(LED_ROSSO, HIGH);
  delay(1000);
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROSSO, LOW);
}
```

---

## 🔄 Funzione `loop()`

Eseguita **continuamente** dopo il setup:

### Timing Non-Bloccante

```cpp
if (millis() - ultimaLettura < INTERVALLO) return;
ultimaLettura = millis();
```

> 💡 Usiamo `millis()` invece di `delay()` per non bloccare l'esecuzione.

### Lettura Sensore

```cpp
float temp = dht.readTemperature();  // Legge temperatura in °C
float umid = dht.readHumidity();      // Legge umidità in %
```

### Gestione Errori

```cpp
if (isnan(temp) || isnan(umid)) {
  Serial.println("ERR:SENSOR");  // Segnala errore via seriale
  lcd.print("Errore sensore!");
  return;  // Salta questa iterazione
}
```

### Invio Dati Seriali

```cpp
Serial.print(temp, 1);   // Temperatura con 1 decimale
Serial.print(",");       // Separatore
Serial.println(umid, 1); // Umidità + newline
```

**Formato output**: `23.5,65.0\n`

### Controllo LED

```cpp
// LED Rosso: acceso se temperatura troppo alta
digitalWrite(LED_ROSSO, temp > TEMP_MAX);

// LED Verde: acceso se temperatura nel range comfort
digitalWrite(LED_VERDE, temp >= TEMP_MIN && temp <= TEMP_MAX);
```

### Aggiornamento Display

```cpp
// Riga 1: Valori
lcd.setCursor(0, 0);
lcd.print("T:");
lcd.print(temp, 1);
lcd.print("C U:");
lcd.print(umid, 0);
lcd.print("%");

// Riga 2: Stato
lcd.setCursor(0, 1);
if (temp > TEMP_MAX) 
  lcd.print("! TROPPO CALDO !");
else if (temp >= TEMP_MIN) 
  lcd.print("OK - Comfort    ");
else 
  lcd.print("Temp. bassa     ");
```

---

## 📊 Diagramma di Flusso

```
        ┌─────────────┐
        │   START     │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   setup()   │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   loop()    │◄─────────────┐
        └──────┬──────┘              │
               │                     │
        ┌──────▼──────┐              │
        │ Tempo       │──NO──────────┤
        │ trascorso?  │              │
        └──────┬──────┘              │
               │ SI                  │
        ┌──────▼──────┐              │
        │ Leggi DHT11 │              │
        └──────┬──────┘              │
               │                     │
        ┌──────▼──────┐              │
        │ Dati validi?│──NO──► Errore├
        └──────┬──────┘              │
               │ SI                  │
        ┌──────▼──────┐              │
        │ Invia dati  │              │
        │ via seriale │              │
        └──────┬──────┘              │
               │                     │
        ┌──────▼──────┐              │
        │ Aggiorna    │              │
        │ LED + LCD   │              │
        └──────┬──────┘              │
               │                     │
               └─────────────────────┘
```

---

## 🔬 Debug e Test

### Monitor Seriale

1. Apri **Tools → Serial Monitor**
2. Imposta **9600 baud**
3. Dovresti vedere output tipo:
   ```
   23.5,65.0
   23.6,64.8
   23.5,65.2
   ```

### Test Soglie

Per testare rapidamente le soglie:
1. Avvicina una fonte di calore al sensore (LED Rosso)
2. Soffia sul sensore (abbassa temperatura)
3. Osserva i cambiamenti su LCD e LED

---

## 📝 Personalizzazioni Suggerite

| Modifica | Come |
|----------|------|
| Cambiare intervallo | Modifica `INTERVALLO` |
| Aggiungere sensore CO2 | Aggiungi nuovo pin e lettura |
| Usare DHT22 | Cambia `DHT_TYPE DHT22` |
| Aggiungere buzzer | Nuovo pin + `tone()` per allarmi |

---

[⬅️ Hardware](Hardware.md) | [➡️ Applicazione Python](Python.md)
