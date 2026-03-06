"""
Sistema di Monitoraggio Efficienza Energetica
UdA Sostenibilità Ambientale
"""

import serial
import serial.tools.list_ports
import threading
import queue
import csv
import os
from datetime import datetime
import dearpygui.dearpygui as dpg

PORTA_SERIALE = "COM7"
BAUD_RATE = 9600
INTERVALLO_CAMPIONAMENTO = 10
FILE_CSV = "dati_sensore.csv"
SOGLIA_MIN = 18.0
SOGLIA_MAX = 25.0

coda_dati = queue.Queue()
dati_temperatura = []
dati_umidita = []
dati_timestamp = []
running = True
ultimo_campionamento = 0


def trova_porta_arduino():
    for porta in serial.tools.list_ports.comports():
        if any(x in porta.description for x in ["Arduino", "CH340", "USB"]):
            return porta.device
    return None


def inizializza_csv():
    if not os.path.exists(FILE_CSV):
        with open(FILE_CSV, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(['timestamp', 'temperatura', 'umidita'])


def salva_csv(timestamp, temperatura, umidita):
    with open(FILE_CSV, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([timestamp, temperatura, umidita])


def carica_storico_csv():
    global dati_temperatura, dati_umidita, dati_timestamp
    if not os.path.exists(FILE_CSV):
        return
    with open(FILE_CSV, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                dati_timestamp.append(row['timestamp'])
                dati_temperatura.append(float(row['temperatura']))
                dati_umidita.append(float(row['umidita']))
            except (ValueError, KeyError):
                continue


def get_stato_messaggio(temperatura):
    if temperatura > SOGLIA_MAX:
        return "CRITICO", "Aprire le finestre! Riscaldamento eccessivo.", (255, 80, 80)
    elif temperatura >= SOGLIA_MIN:
        return "COMFORT", "Temperatura ottimale. Risparmio energetico.", (80, 255, 80)
    return "STAND-BY", "Temperatura bassa. Verificare isolamento.", (150, 150, 150)


def thread_lettura_seriale():
    global running, ultimo_campionamento
    porta = trova_porta_arduino() or PORTA_SERIALE
    print(f"Connessione a: {porta}")
    
    try:
        ser = serial.Serial(porta, BAUD_RATE, timeout=1)
        print(f"Connesso a {porta}")
        
        while running:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8').strip()
                if linea.startswith("ERR"):
                    continue
                parti = linea.split(',')
                if len(parti) == 2:
                    try:
                        temp = float(parti[0])
                        umid = float(parti[1])
                        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        coda_dati.put((ts, temp, umid))
                        
                        tempo = datetime.now().timestamp()
                        if tempo - ultimo_campionamento >= INTERVALLO_CAMPIONAMENTO:
                            ultimo_campionamento = tempo
                            salva_csv(ts, temp, umid)
                            print(f"Salvato: {ts}, T={temp}°C, U={umid}%")
                    except ValueError:
                        continue
    except serial.SerialException as e:
        print(f"Errore seriale: {e}")
        print("Modalità simulazione attiva...")
        import random
        import time
        
        while running:
            temp = round(random.uniform(15, 30), 1)
            umid = round(random.uniform(40, 70), 1)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            coda_dati.put((ts, temp, umid))
            
            tempo = datetime.now().timestamp()
            if tempo - ultimo_campionamento >= INTERVALLO_CAMPIONAMENTO:
                ultimo_campionamento = tempo
                salva_csv(ts, temp, umid)
            time.sleep(2)


def aggiorna_gui():
    global dati_temperatura, dati_umidita, dati_timestamp
    try:
        while not coda_dati.empty():
            ts, temp, umid = coda_dati.get_nowait()
            dati_timestamp.append(ts)
            dati_temperatura.append(temp)
            dati_umidita.append(umid)
            
            if len(dati_temperatura) > 100:
                dati_temperatura = dati_temperatura[-100:]
                dati_umidita = dati_umidita[-100:]
                dati_timestamp = dati_timestamp[-100:]
            
            dpg.set_value("temp_value", f"{temp:.1f} °C")
            dpg.set_value("umid_value", f"{umid:.1f} %")
            dpg.set_value("time_value", ts)
            
            stato, msg, colore = get_stato_messaggio(temp)
            dpg.set_value("stato_value", stato)
            dpg.set_value("messaggio_value", msg)
            dpg.configure_item("stato_value", color=colore)
            
            x = list(range(len(dati_temperatura)))
            dpg.set_value("serie_temp", [x, dati_temperatura])
            dpg.set_value("serie_umid", [x, dati_umidita])
            
            if len(x) > 1:
                dpg.fit_axis_data("asse_x")
                dpg.fit_axis_data("asse_y")
                dpg.fit_axis_data("asse_y2")
    except:
        pass


def ricarica_storico():
    global dati_temperatura, dati_umidita, dati_timestamp
    dati_temperatura, dati_umidita, dati_timestamp = [], [], []
    carica_storico_csv()
    
    if dati_temperatura:
        x = list(range(len(dati_temperatura)))
        dpg.set_value("serie_temp", [x, dati_temperatura])
        dpg.set_value("serie_umid", [x, dati_umidita])
        dpg.fit_axis_data("asse_x")
        dpg.fit_axis_data("asse_y")
        dpg.fit_axis_data("asse_y2")
        dpg.set_value("temp_value", f"{dati_temperatura[-1]:.1f} °C")
        dpg.set_value("umid_value", f"{dati_umidita[-1]:.1f} %")
        dpg.set_value("time_value", dati_timestamp[-1])


def crea_gui():
    dpg.create_context()
    
    with dpg.theme() as tema:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)
    dpg.bind_theme(tema)
    
    with dpg.window(label="Monitoraggio Energetico", tag="main"):
        dpg.add_text("MONITORAGGIO EFFICIENZA ENERGETICA", color=(100, 200, 255))
        dpg.add_text("UdA - Sostenibilità Ambientale", color=(150, 150, 150))
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        with dpg.group(horizontal=True):
            with dpg.child_window(width=200, height=150):
                dpg.add_text("TEMPERATURA", color=(255, 200, 100))
                dpg.add_text("-- °C", tag="temp_value")
            with dpg.child_window(width=200, height=150):
                dpg.add_text("UMIDITÀ", color=(100, 200, 255))
                dpg.add_text("-- %", tag="umid_value")
            with dpg.child_window(width=250, height=150):
                dpg.add_text("STATO", color=(200, 200, 200))
                dpg.add_text("--", tag="stato_value", color=(150, 150, 150))
                dpg.add_spacer(height=5)
                dpg.add_text("", tag="messaggio_value", wrap=230)
        
        dpg.add_spacer(height=5)
        dpg.add_text("Ultimo aggiornamento:", color=(150, 150, 150))
        dpg.add_text("--", tag="time_value", color=(200, 200, 200))
        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        dpg.add_text("GRAFICO TEMPERATURA E UMIDITÀ", color=(100, 200, 255))
        with dpg.plot(label="Andamento", height=300, width=-1):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Campioni", tag="asse_x")
            dpg.add_plot_axis(dpg.mvYAxis, label="Temperatura (°C)", tag="asse_y")
            dpg.add_plot_axis(dpg.mvYAxis, label="Umidità (%)", tag="asse_y2")
            dpg.add_line_series([], [], label="Temperatura", parent="asse_y", tag="serie_temp")
            dpg.add_line_series([], [], label="Umidità", parent="asse_y2", tag="serie_umid")
        
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Ricarica Storico", callback=ricarica_storico)
            dpg.add_text(f"  File: {FILE_CSV}", color=(150, 150, 150))
        
        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_text(f"Stand-by: <{SOGLIA_MIN}°C", color=(150, 150, 150))
            dpg.add_text(f" | Comfort: {SOGLIA_MIN}-{SOGLIA_MAX}°C", color=(80, 255, 80))
            dpg.add_text(f" | Critico: >{SOGLIA_MAX}°C", color=(255, 80, 80))
    
    dpg.create_viewport(title="Monitoraggio Energetico", width=700, height=650)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main", True)


def main():
    global running
    inizializza_csv()
    carica_storico_csv()
    
    threading.Thread(target=thread_lettura_seriale, daemon=True).start()
    crea_gui()
    
    while dpg.is_dearpygui_running():
        aggiorna_gui()
        dpg.render_dearpygui_frame()
    
    running = False
    dpg.destroy_context()


if __name__ == "__main__":
    main()
