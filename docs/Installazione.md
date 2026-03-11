# 🔧 Guida all'Installazione

Questa guida ti accompagnerà nell'installazione completa del sistema.

---

## 📋 Prerequisiti

### Software Necessario

| Software | Versione | Download |
|----------|----------|----------|
| Arduino IDE | 2.x | [arduino.cc](https://www.arduino.cc/en/software) |
| Python | ≥ 3.10 | [python.org](https://www.python.org/downloads/) |
| uv (opzionale) | latest | [astral.sh/uv](https://astral.sh/uv) |

### Hardware Necessario

- Arduino Uno/Nano/Mega
- Sensore DHT11
- Display LCD 16x2
- 2 LED (verde e rosso)
- Resistenze (220Ω per LED, 10kΩ per DHT11)
- Breadboard e cavetti

---

## 1️⃣ Installazione Arduino

### Passo 1: Installa le Librerie

Apri Arduino IDE e vai su **Sketch → Include Library → Manage Libraries...**

Cerca e installa:
- **DHT sensor library** (by Adafruit)
- **LiquidCrystal** (già inclusa)

### Passo 2: Configura la Scheda

1. Vai su **Tools → Board** e seleziona la tua scheda Arduino
2. Vai su **Tools → Port** e seleziona la porta COM corretta

### Passo 3: Carica lo Sketch

1. Apri il file `arduino/monitoraggio/monitoraggio.ino`
2. Clicca su **Upload** (freccia →)
3. Attendi il messaggio "Done uploading"

---

## 2️⃣ Installazione Python

### Opzione A: Con uv (Consigliato)

```powershell
# Installa uv (se non presente)
irm https://astral.sh/uv/install.ps1 | iex

# Vai nella cartella python
cd python

# Sincronizza le dipendenze
uv sync

# Avvia l'applicazione
uv run app.py
```

### Opzione B: Con pip Tradizionale

```powershell
# Vai nella cartella python
cd python

# Crea un ambiente virtuale
python -m venv venv

# Attiva l'ambiente virtuale
.\venv\Scripts\Activate.ps1

# Installa le dipendenze
pip install pyserial dearpygui

# Avvia l'applicazione
python app.py
```

---

## 3️⃣ Configurazione della Porta Seriale

L'applicazione Python cerca automaticamente la porta Arduino. Se non funziona:

### Trova la Porta Manualmente

1. Apri **Gestione Dispositivi** (Windows)
2. Espandi **Porte (COM e LPT)**
3. Trova "Arduino" o "USB-SERIAL CH340"
4. Annota il numero della porta (es. COM3)

### Modifica la Porta nel Codice

Apri `python/app.py` e modifica la riga:

```python
PORTA_SERIALE = "COM7"  # Cambia con la tua porta
```

---

## 4️⃣ Verifica dell'Installazione

### Test Arduino

1. Apri il **Monitor Seriale** (Tools → Serial Monitor)
2. Imposta il baud rate a **9600**
3. Dovresti vedere dati nel formato: `23.5,65.0`

### Test Python

1. Avvia l'applicazione
2. Dovresti vedere la finestra con i grafici
3. I dati dovrebbero aggiornarsi ogni 2 secondi

---

## ⚠️ Risoluzione Problemi Comuni

| Problema | Soluzione |
|----------|-----------|
| "Porta non trovata" | Verifica i driver CH340/Arduino |
| "Errore sensore" | Controlla i collegamenti del DHT11 |
| "ModuleNotFoundError" | Esegui `uv sync` o `pip install` |
| LCD non si accende | Verifica alimentazione 5V |

Per problemi più specifici, consulta la [Guida Troubleshooting](Troubleshooting.md).

---

[⬅️ Home](Home.md) | [➡️ Schema Hardware](Hardware.md)
