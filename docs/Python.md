# Applicazione Python

Guida completa all'applicazione desktop per il monitoraggio.

---

## File: `app.py`

L'applicazione Python funge da **consumatore** nel pattern produttore-consumatore, ricevendo i dati da Arduino e visualizzandoli.

---

## Dipendenze

```toml
[project]
dependencies = [
    "pyserial>=3.5",      # Comunicazione seriale
    "dearpygui>=1.9.0",   # Interfaccia grafica
]
```

### Installazione

```powershell
# Con uv (consigliato)
uv sync

# Con pip
pip install pyserial dearpygui
```

---

## Configurazione

All'inizio del file `app.py`:

```python
PORTA_SERIALE = "COM7"          # Porta Arduino
BAUD_RATE = 9600                # Velocità comunicazione
INTERVALLO_CAMPIONAMENTO = 10   # Secondi tra salvataggi CSV
FILE_CSV = "dati_sensore.csv"   # Nome file storico
SOGLIA_MIN = 18.0               # Temperatura minima comfort
SOGLIA_MAX = 25.0               # Temperatura massima comfort
```

### Come Configurare

| Parametro | Descrizione | Come Trovare |
|-----------|-------------|--------------|
| `PORTA_SERIALE` | Porta COM di Arduino | Gestione Dispositivi |
| `BAUD_RATE` | Deve corrispondere ad Arduino | 9600 di default |
| `INTERVALLO_CAMPIONAMENTO` | Frequenza salvataggio | A piacere |

---

## Architettura dell'Applicazione

```
┌─────────────────────────────────────────────────────┐
│                    main()                           │
│  ┌─────────────────┐    ┌───────────────────────┐  │
│  │ Thread Seriale  │    │    Loop Principale    │  │
│  │                 │    │                       │  │
│  │ ┌─────────────┐ │    │  ┌─────────────────┐  │  │
│  │ │ Leggi dati  │ │    │  │ aggiorna_gui()  │  │  │
│  │ │ da Arduino  │ │    │  │ - Legge Queue   │  │  │
│  │ └──────┬──────┘ │    │  │ - Aggiorna GUI  │  │  │
│  │        │        │    │  └─────────────────┘  │  │
│  │        ▼        │    │                       │  │
│  │ ┌─────────────┐ │    │  ┌─────────────────┐  │  │
│  │ │ Metti in    │─┼────┼─►│     Queue       │  │  │
│  │ │   Queue     │ │    │  │  (thread-safe)  │  │  │
│  │ └──────┬──────┘ │    │  └─────────────────┘  │  │
│  │        │        │    │                       │  │
│  │        ▼        │    │  ┌─────────────────┐  │  │
│  │ ┌─────────────┐ │    │  │ render_frame()  │  │  │
│  │ │ Salva CSV   │ │    │  │ - Disegna GUI   │  │  │
│  │ │ (ogni 10s)  │ │    │  └─────────────────┘  │  │
│  │ └─────────────┘ │    │                       │  │
│  └─────────────────┘    └───────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Componenti Principali

### 1. Rilevamento Automatico Porta

```python
def trova_porta_arduino():
    for porta in serial.tools.list_ports.comports():
        if any(x in porta.description for x in ["Arduino", "CH340", "USB"]):
            return porta.device
    return None
```

> Cerca automaticamente Arduino tra le porte disponibili.

### 2. Thread di Lettura Seriale

```python
def thread_lettura_seriale():
    porta = trova_porta_arduino() or PORTA_SERIALE
    ser = serial.Serial(porta, BAUD_RATE, timeout=1)
    
    while running:
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            # Parse: "23.5,65.0" → (23.5, 65.0)
            parti = linea.split(',')
            temp = float(parti[0])
            umid = float(parti[1])
            coda_dati.put((timestamp, temp, umid))
```

> Esegue in background, non blocca la GUI.

### 3. Modalità Simulazione

Se Arduino non è connesso, l'app genera dati casuali:

```python
except serial.SerialException:
    print("Modalità simulazione attiva...")
    while running:
        temp = round(random.uniform(15, 30), 1)
        umid = round(random.uniform(40, 70), 1)
        coda_dati.put((timestamp, temp, umid))
        time.sleep(2)
```

> Utile per sviluppo e test senza hardware.

### 4. Gestione CSV

```python
def salva_csv(timestamp, temperatura, umidita):
    with open(FILE_CSV, 'a', newline='') as f:
        csv.writer(f).writerow([timestamp, temperatura, umidita])
```

> Salva i dati ogni `INTERVALLO_CAMPIONAMENTO` secondi.

### 5. Interfaccia Grafica (DearPyGui)

L'interfaccia include:
- **Pannelli informativi**: temperatura, umidità, stato
- **Grafico real-time**: andamento nel tempo
- **Indicatori colorati**: verde/rosso per lo stato
- **Pulsante storico**: ricarica dati salvati

---

## Screenshot Interfaccia

```
┌─────────────────────────────────────────────────────┐
│  MONITORAGGIO EFFICIENZA ENERGETICA                 │
│  UdA - Sostenibilità Ambientale                     │
├─────────────────────────────────────────────────────┤
│ ┌───────────┐ ┌───────────┐ ┌─────────────────────┐ │
│ │TEMPERATURA│ │  UMIDITÀ  │ │       STATO         │ │
│ │  23.5 °C  │ │  65.0 %   │ │      COMFORT        │ │
│ │           │ │           │ │ Temperatura ottimale│ │
│ └───────────┘ └───────────┘ └─────────────────────┘ │
│                                                     │
│ Ultimo aggiornamento: 2026-03-11 14:30:25          │
├─────────────────────────────────────────────────────┤
│ GRAFICO TEMPERATURA E UMIDITÀ                       │
│ ┌─────────────────────────────────────────────────┐ │
│ │     ╱╲    ╱╲                                    │ │
│ │    ╱  ╲  ╱  ╲   ← Temperatura                   │ │
│ │   ╱    ╲╱    ╲                                  │ │
│ │  ────────────── ← Umidità                       │ │
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ [Ricarica Storico]  File: dati_sensore.csv         │
├─────────────────────────────────────────────────────┤
│ Stand-by: <18°C | Comfort: 18-25°C | Critico: >25°C│
└─────────────────────────────────────────────────────┘
```

---

## Avvio dell'Applicazione

### Metodo 1: Con uv

```powershell
cd python
uv run app.py
```

### Metodo 2: Con Python

```powershell
cd python
python app.py
```

---

## Formato File CSV

Il file `dati_sensore.csv` contiene:

```csv
timestamp,temperatura,umidita
2026-03-11 14:30:25,23.5,65.0
2026-03-11 14:30:35,23.6,64.8
2026-03-11 14:30:45,23.7,65.2
```

### Analisi Dati

Puoi analizzare i dati con:
- **Excel**: importa direttamente il CSV
- **Python/Pandas**: `pd.read_csv('dati_sensore.csv')`
- **Grafici online**: carica su Google Sheets

---

## Personalizzazioni

| Modifica | File | Riga |
|----------|------|------|
| Cambiare soglie | `app.py` | `SOGLIA_MIN`, `SOGLIA_MAX` |
| Frequenza salvataggio | `app.py` | `INTERVALLO_CAMPIONAMENTO` |
| Dimensione finestra | `app.py` | `create_viewport(width=700, height=650)` |
| Colori tema | `app.py` | Sezione `dpg.theme()` |

---

## Debug

### Abilitare Log Dettagliati

Aggiungi all'inizio di `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verificare Connessione Seriale

```python
import serial.tools.list_ports
for p in serial.tools.list_ports.comports():
    print(f"{p.device}: {p.description}")
```

---

[Codice Arduino](Arduino.md) | [Risoluzione Problemi](Troubleshooting.md)
