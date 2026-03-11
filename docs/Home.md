# Home - Panoramica del Progetto

## Cos'è questo progetto?

Il **Sistema di Monitoraggio Efficienza Energetica** è un progetto didattico per l'Unità di Apprendimento (UdA) sulla **Sostenibilità Ambientale**. 

Permette di monitorare in tempo reale temperatura e umidità di un ambiente, visualizzando i dati su un'interfaccia grafica e salvandoli per analisi successive.

---

## Obiettivi Didattici

- Comprendere il paradigma **Produttore-Consumatore**
- Imparare la comunicazione **seriale** tra dispositivi
- Utilizzare **thread** e **code** per la sincronizzazione
- Sviluppare interfacce grafiche con Python
- Sensibilizzare sull'**efficienza energetica**

---

## Architettura del Sistema

```
┌─────────────────────────┐          ┌─────────────────────────┐
│       ARDUINO           │          │        PYTHON           │
│      (Produttore)       │          │      (Consumatore)      │
│                         │          │                         │
│  ┌─────────┐           │  Seriale │  ┌─────────┐           │
│  │  DHT11  │──► Lettura │ ───────► │  │ Thread  │──► Ricezione│
│  └─────────┘    dati    │ temp,umid│  └─────────┘    dati    │
│                         │    \n    │       │                 │
│  ┌─────────┐           │          │       ▼                 │
│  │   LCD   │◄── Display │          │  ┌─────────┐           │
│  └─────────┘            │          │  │  Queue  │──► Sync    │
│                         │          │  └─────────┘            │
│  ┌─────────┐           │          │       │                 │
│  │   LED   │◄── Stato   │          │       ▼                 │
│  └─────────┘            │          │  ┌─────────┐ ┌───────┐ │
└─────────────────────────┘          │  │   GUI   │ │  CSV  │ │
                                     │  └─────────┘ └───────┘ │
                                     └─────────────────────────┘
```

---

## Funzionalità Principali

| Funzionalità | Descrizione |
|--------------|-------------|
| **Monitoraggio Real-time** | Lettura continua di temperatura e umidità |
| **Visualizzazione** | Display LCD + GUI desktop con grafici |
| **Indicatori LED** | Feedback visivo immediato sullo stato |
| **Storico Dati** | Salvataggio automatico su file CSV |
| **Soglie Configurabili** | Personalizzazione delle soglie di comfort |

---

## Struttura del Progetto

```
tpi-arduino-uda/
├── arduino/
│   └── monitoraggio/
│       └── monitoraggio.ino    # Firmware Arduino
├── python/
│   ├── app.py                  # Applicazione principale
│   ├── pyproject.toml          # Dipendenze Python
│   ├── uv.lock                 # Lock delle versioni
│   └── dati_sensore.csv        # Dati raccolti
├── docs/                       # Documentazione
├── README.md                   # Readme principale
└── LICENSE                     # Licenza MIT
```

---

## Soglie di Comfort

| Stato | Temperatura | LED | Significato |
|-------|-------------|-----|-------------|
| **Stand-by** | < 18°C | Spenti | Ambiente freddo |
| **Comfort** | 18-25°C | Verde | Temperatura ottimale |
| **Critico** | > 25°C | Rosso | Spreco energetico |

---

## Prossimi Passi

1. Leggi la [Guida all'Installazione](Installazione.md)
2. Configura l'[Hardware](Hardware.md)
3. Carica il [Codice Arduino](Arduino.md)
4. Avvia l'[Applicazione Python](Python.md)

---

[Vai alla Guida Installazione](Installazione.md)
