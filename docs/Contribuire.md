# Contribuire al Progetto

Grazie per l'interesse a contribuire! Questa guida spiega come partecipare.

---

## Codice di Condotta

- Sii rispettoso e costruttivo
- Accetta feedback con apertura
- Aiuta gli altri a imparare
- Mantieni un ambiente inclusivo

---

## Segnalare Bug

### Prima di Segnalare

1. Verifica che il bug non sia già stato segnalato
2. Prova le soluzioni nella [Guida Troubleshooting](Troubleshooting.md)
3. Raccogli informazioni utili

### Come Segnalare

Crea una **Issue** su GitHub con:

```markdown
## Descrizione Bug
Breve descrizione del problema.

## Come Riprodurre
1. Vai su '...'
2. Clicca su '...'
3. Osserva l'errore

## Comportamento Atteso
Cosa dovrebbe succedere.

## Comportamento Attuale
Cosa succede invece.

## Ambiente
- OS: Windows 11
- Python: 3.11
- Arduino: Uno R3
- Versione progetto: 1.0.0

## Screenshot/Log
[Se applicabile]
```

---

## Proporre Miglioramenti

### Idee Benvenute

- Nuovi sensori (CO2, luminosità, rumore)
- Miglioramenti UI
- Nuove funzionalità (allarmi, notifiche, export)
- Ottimizzazioni codice
- Documentazione

### Come Proporre

1. Apri una **Issue** con il tag `enhancement`
2. Descrivi la funzionalità
3. Spiega il beneficio
4. Proponi un'implementazione (opzionale)

---

## Contribuire Codice

### Setup Sviluppo

```powershell
# 1. Fork del repository (su GitHub)

# 2. Clona il tuo fork
git clone https://github.com/TUO-USERNAME/tpi-arduino-uda.git

# 3. Crea un branch
git checkout -b feature/mia-funzionalita

# 4. Sviluppa e testa

# 5. Commit con messaggi chiari
git commit -m "Aggiunge supporto sensore CO2"

# 6. Push sul tuo fork
git push origin feature/mia-funzionalita

# 7. Apri una Pull Request
```

### Linee Guida Codice

#### Arduino
- Commenta le funzioni principali
- Usa nomi variabili descrittivi in italiano
- Mantieni il codice compatto e leggibile
- Testa su hardware reale prima di inviare

#### Python
- Segui PEP 8 per lo stile
- Aggiungi docstring alle funzioni
- Gestisci le eccezioni appropriatamente
- Mantieni la retrocompatibilità

### Esempio di Buon Commit

```
feat: Aggiunge allarme sonoro per temperatura critica

- Nuovo pin BUZZER configurabile
- Funzione allarme_sonoro() con frequenza variabile
- Attivazione automatica sopra TEMP_MAX
- Documentazione aggiornata

Closes #12
```

---

## Contribuire Documentazione

La documentazione è importante quanto il codice!

### Puoi Contribuire Con

- Correzioni errori di battitura
- Miglioramenti chiarezza
- Traduzioni
- Nuove guide
- Esempi aggiuntivi

### Stile Documentazione

- Usa italiano semplice e chiaro
- Includi esempi pratici
- Aggiungi screenshot quando utile
- Mantieni la struttura esistente

---

## Testing

Prima di inviare una PR:

### Checklist Test

- [ ] Lo sketch Arduino compila senza errori
- [ ] L'app Python si avvia correttamente
- [ ] La comunicazione seriale funziona
- [ ] I nuovi dati vengono salvati nel CSV
- [ ] La GUI mostra i dati correttamente
- [ ] Nessuna regressione su funzionalità esistenti

---

## Template Pull Request

```markdown
## Descrizione
Breve descrizione delle modifiche.

## Tipo di Modifica
- [ ] Bug fix
- [ ] Nuova funzionalità
- [ ] Documentazione
- [ ] Refactoring
- [ ] Altro: ________

## Checklist
- [ ] Ho testato le modifiche
- [ ] Ho aggiornato la documentazione
- [ ] Il codice segue le linee guida
- [ ] Ho aggiunto commenti dove necessario

## Screenshot
[Se applicabile]

## Note Aggiuntive
[Qualsiasi altra informazione utile]
```

---

## Per Studenti

Questo progetto è pensato per l'apprendimento. Se sei uno studente:

1. **Sperimenta**: Modifica il codice e osserva cosa succede
2. **Chiedi**: Non aver paura di fare domande
3. **Documenta**: Scrivi cosa hai imparato
4. **Condividi**: Aiuta i compagni con le tue scoperte

### Idee per Progetti Derivati

- Dashboard web con Flask/Django
- App mobile con React Native
- Machine learning per predizioni
- Sistema di notifiche via email
- Integrazione con domotica

---

## Licenza

Contribuendo a questo progetto, accetti che il tuo contributo sia rilasciato sotto la stessa licenza MIT del progetto.

---

## Ringraziamenti

Grazie a tutti i contributori che hanno reso possibile questo progetto!

---

[Troubleshooting](Troubleshooting.md) | [Home](Home.md)
