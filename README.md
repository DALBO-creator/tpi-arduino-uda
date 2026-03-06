# Sistema di Monitoraggio Efficienza Energetica

**UdA Sostenibilità Ambientale** - Sistema di monitoraggio parametri ambientali con paradigma produttore-consumatore.

## Architettura

```
┌─────────────────┐     Seriale      ┌─────────────────┐
│     ARDUINO     │ ───────────────► │     PYTHON      │
│   (Produttore)  │   temp,umid\n    │  (Consumatore)  │
│                 │                  │                 │
│  DHT11 → Dati   │                  │  Thread → GUI   │
│  LED → Stato    │                  │  Queue → Sync   │
│  LCD → Display  │                  │  CSV → Storage  │
└─────────────────┘                  └─────────────────┘
```

## Struttura

```
tpi-arduino-uda/
├── arduino/
│   └── monitoraggio/
│       └── monitoraggio.ino
├── python/
│   ├── app.py
│   ├── pyproject.toml
│   └── dati_sensore.csv
└── README.md
```

## Hardware

| Componente | Pin |
|------------|-----|
| DHT11 DATA | 8 |
| DHT11 VCC | 5V |
| DHT11 GND | GND |
| LED Verde | 12 |
| LED Rosso | 13 |
| LCD RS | 11 |
| LCD E | 10 |
| LCD D4-D7 | 6, 5, 4, 3 |
| LCD V0 | GND |
| LCD VDD/A | 5V |
| LCD VSS/RW/K | GND |

## Installazione

### Arduino
1. Installa libreria **DHT sensor library** da Library Manager
2. Carica `arduino/monitoraggio/monitoraggio.ino`

### Python
```bash
cd python
uv sync
uv run app.py
```

## Soglie

| Stato | Temperatura | LED |
|-------|-------------|-----|
| Stand-by | < 18°C | Spenti |
| Comfort | 18-25°C | Verde |
| Critico | > 25°C | Rosso |

## Sincronizzazione

- **Arduino**: `millis()` per timing non bloccante
- **Seriale**: Pacchetti `temp,umid\n` a 9600 baud
- **Python**: Thread + Queue per disaccoppiamento I/O e GUI
- **Storage**: CSV con campionamento ogni 10 secondi
