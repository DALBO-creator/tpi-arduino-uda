# Risoluzione Problemi

Guida alle soluzioni dei problemi più comuni.

---

## Problemi Arduino

### Il LED non si accende

**Causa**: Collegamento errato o LED bruciato.

**Soluzioni**:
1. Verifica la polarità del LED (gamba lunga = +)
2. Controlla che la resistenza sia collegata
3. Testa il LED con una batteria 3V
4. Verifica il pin nel codice corrisponda al collegamento

---

### LCD non mostra nulla

**Causa**: Problema di contrasto o alimentazione.

**Soluzioni**:
1. **Contrasto**: Collega V0 direttamente a GND
2. **Alimentazione**: Verifica 5V su VDD
3. **Backlight**: Controlla A (5V) e K (GND)
4. **Collegamenti**: Ricontrolla tutti i pin

```
Configurazione minima per test LCD:
VSS → GND
VDD → 5V
V0  → GND (massimo contrasto)
RS  → Pin 11
RW  → GND
E   → Pin 10
D4-D7 → Pin 6,5,4,3
A   → 5V
K   → GND
```

---

### "Errore sensore" sul display

**Causa**: DHT11 non risponde.

**Soluzioni**:
1. Verifica i collegamenti del DHT11
2. Controlla che VCC sia su 5V (non 3.3V)
3. Prova ad aggiungere una resistenza 10kΩ pull-up tra DATA e VCC
4. Attendi qualche secondo dopo l'accensione

---

### Upload fallisce

**Causa**: Problema di comunicazione con Arduino.

**Soluzioni**:
1. Seleziona la scheda corretta in **Tools → Board**
2. Seleziona la porta corretta in **Tools → Port**
3. Scollega e ricollega Arduino
4. Installa/aggiorna i driver (CH340 per cloni)

---

## Problemi Python

### "ModuleNotFoundError: No module named 'serial'"

**Causa**: Dipendenza non installata.

**Soluzione**:
```powershell
# Con uv
uv sync

# Con pip
pip install pyserial
```

---

### "ModuleNotFoundError: No module named 'dearpygui'"

**Causa**: Libreria GUI non installata.

**Soluzione**:
```powershell
# Con uv
uv sync

# Con pip
pip install dearpygui
```

---

### "could not open port 'COM7'"

**Causa**: Porta seriale non disponibile.

**Soluzioni**:
1. **Verifica la porta**: Apri Gestione Dispositivi
2. **Modifica il codice**: Cambia `PORTA_SERIALE` in `app.py`
3. **Chiudi altri programmi**: Il Monitor Seriale di Arduino blocca la porta
4. **Scollega/ricollega**: Resetta la connessione USB

```python
# Trova la porta corretta
import serial.tools.list_ports
for p in serial.tools.list_ports.comports():
    print(f"{p.device}: {p.description}")
```

---

### La GUI non si apre

**Causa**: Problema con DearPyGui.

**Soluzioni**:
1. Aggiorna DearPyGui: `pip install --upgrade dearpygui`
2. Verifica la compatibilità Python (≥3.10)
3. Su Windows, installa Visual C++ Redistributable

---

### I dati non si aggiornano

**Causa**: Problema di comunicazione.

**Soluzioni**:
1. Verifica che Arduino stia inviando dati (Monitor Seriale)
2. Controlla che il baud rate corrisponda (9600)
3. Verifica che nessun altro programma usi la porta
4. L'app passa in modalità simulazione se non trova Arduino

---

### Il file CSV non viene creato

**Causa**: Problemi di permessi o path.

**Soluzioni**:
1. Esegui da una cartella con permessi di scrittura
2. Verifica che la cartella `python/` esista
3. Controlla antivirus/firewall

---

## Problemi di Comunicazione

### Dati corrotti o illeggibili

**Causa**: Baud rate non corrispondente.

**Soluzione**: Verifica che entrambi usino lo stesso valore:
- Arduino: `Serial.begin(9600);`
- Python: `BAUD_RATE = 9600`

---

### Ritardo nei dati

**Causa**: Buffer seriale pieno.

**Soluzioni**:
1. Riduci la frequenza di invio da Arduino
2. Aumenta `timeout` nella connessione Python
3. Svuota il buffer: `ser.reset_input_buffer()`

---

## Checklist di Debug

### Prima di Accendere
- [ ] Tutti i collegamenti sono corretti
- [ ] Nessun cortocircuito visibile
- [ ] Arduino connesso via USB
- [ ] Librerie Arduino installate

### Se Non Funziona
- [ ] Test LED con sketch di esempio
- [ ] Test LCD con sketch di esempio  
- [ ] Verifica Monitor Seriale
- [ ] Prova app Python in modalità simulazione

### Log Utili
```powershell
# Verifica porte disponibili
python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"

# Verifica versione Python
python --version

# Verifica pacchetti installati
pip list | findstr "serial\|dearpygui"
```

---

## Ancora Problemi?

Se non trovi la soluzione:

1. **Controlla il codice**: Assicurati di non aver modifiche accidentali
2. **Riparti da zero**: Ricarica lo sketch originale
3. **Testa componenti singoli**: Isola il problema
4. **Chiedi aiuto**: Descrivi il problema con:
   - Cosa hai fatto
   - Cosa ti aspettavi
   - Cosa è successo invece
   - Messaggi di errore completi

---

[Applicazione Python](Python.md) | [Contribuire](Contribuire.md)
