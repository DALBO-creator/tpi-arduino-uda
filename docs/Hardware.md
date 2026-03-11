# Schema Hardware

Guida completa ai collegamenti elettronici del progetto.

---

## Lista Componenti

| Componente | Quantità | Note |
|------------|----------|------|
| Arduino Uno/Nano | 1 | Qualsiasi board compatibile |
| DHT11 | 1 | Sensore temperatura/umidità |
| LCD 16x2 | 1 | Con controller HD44780 |
| LED Verde | 1 | 5mm standard |
| LED Rosso | 1 | 5mm standard |
| Resistenza 220Ω | 2 | Per i LED |
| Resistenza 10kΩ | 1 | Pull-up per DHT11 (opzionale) |
| Potenziometro 10kΩ | 1 | Per contrasto LCD (opzionale) |
| Breadboard | 1 | 400+ punti |
| Cavetti | ~20 | M-M o M-F |

---

## Tabella Collegamenti

### Sensore DHT11

| Pin DHT11 | Pin Arduino | Note |
|-----------|-------------|------|
| VCC (+) | 5V | Alimentazione |
| DATA | 8 | Segnale dati |
| GND (-) | GND | Massa |

> **Suggerimento**: Alcuni moduli DHT11 hanno già la resistenza pull-up integrata.

### LED Indicatori

| Componente | Pin Arduino | Note |
|------------|-------------|------|
| LED Verde (+) | 12 | Tramite resistenza 220Ω |
| LED Verde (-) | GND | Catodo |
| LED Rosso (+) | 13 | Tramite resistenza 220Ω |
| LED Rosso (-) | GND | Catodo |

### Display LCD 16x2

| Pin LCD | Pin Arduino | Note |
|---------|-------------|------|
| VSS | GND | Massa |
| VDD | 5V | Alimentazione |
| V0 | GND | Contrasto (o potenziometro) |
| RS | 11 | Register Select |
| RW | GND | Read/Write (sempre Write) |
| E | 10 | Enable |
| D4 | 6 | Data 4 |
| D5 | 5 | Data 5 |
| D6 | 4 | Data 6 |
| D7 | 3 | Data 7 |
| A | 5V | Retroilluminazione + |
| K | GND | Retroilluminazione - |

---

## Schema di Collegamento

```
                    ARDUINO UNO
                 ┌──────────────┐
                 │              │
    DHT11 DATA ──│ D8       D13 │── LED Rosso (+)
                 │          D12 │── LED Verde (+)
       LCD RS ──│ D11      D11 │
        LCD E ──│ D10      D10 │
       LCD D4 ──│ D6           │
       LCD D5 ──│ D5           │
       LCD D6 ──│ D4           │
       LCD D7 ──│ D3           │
                 │              │
                 │  5V     GND  │
                 └──────────────┘
                    │       │
                    │       └──► GND comune
                    └──────────► VCC comune (5V)
```

---

## Schema Fritzing

```
         DHT11
        ┌─────┐
        │ S   │
        │ +   │──── 5V
        │ -   │──── GND
        │ OUT │──── Pin 8
        └─────┘

         LCD 16x2
    ┌────────────────────────┐
    │  VSS VDD V0  RS RW  E  │
    │   │   │   │   │  │  │  │
    │  GND 5V GND D11 GND D10│
    │                        │
    │  D0 D1 D2 D3 D4 D5 D6 D7│
    │   │  │  │  │  │  │  │  │ 
    │  NC NC NC NC D6 D5 D4 D3│
    │                        │
    │  A   K                 │
    │  │   │                 │
    │ 5V  GND                │
    └────────────────────────┘

    LED Verde          LED Rosso
    ┌───┐              ┌───┐
    │ + │── 220Ω ── D12│ + │── 220Ω ── D13
    │ - │──── GND      │ - │──── GND
    └───┘              └───┘
```

---

## Note Importanti

### Contrasto LCD
Se il display non mostra caratteri visibili:
- Collega V0 a GND per massimo contrasto
- Oppure usa un potenziometro 10kΩ tra 5V-V0-GND

### Polarità LED
- Il terminale **lungo** è il positivo (anodo) → va alla resistenza
- Il terminale **corto** è il negativo (catodo) → va a GND

### Alimentazione
- Non superare mai i 5V sui pin Arduino
- Il DHT11 funziona a 3.3V-5V
- L'LCD richiede esattamente 5V

---

## Verifica Collegamenti

Prima di accendere, controlla:

- [ ] Nessun cortocircuito tra 5V e GND
- [ ] Resistenze sui LED correttamente collegate
- [ ] DHT11 con la giusta polarità
- [ ] LCD con tutti i pin collegati

---

[Installazione](Installazione.md) | [Codice Arduino](Arduino.md)
