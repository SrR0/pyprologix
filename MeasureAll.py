import threading
import time
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.widgets import Button
from pm2534 import pm2534
from hp3478a import hp3478a

# Initialisiere die Messgeräte (pm2534 und hp3478a)
device_1 = pm2534(22, "COM11", debug=True)
device_1.setSpeed(device_1.Speeds.Speed1)
device_1.setRange(3E0)
device_2 = hp3478a(23, "COM12", debug=False)
device_2.setRange("3")

Geraet1 = 'PM2534'
Geraet2 = 'HP3478A'

# Betriebsmodus für die Geräte
mode_device_1 = "Mode A"
mode_device_2 = "Mode A"

# Datenpuffer für jedes Messgerät (deque für die Echtzeitdaten)
data_1 = deque(maxlen=100)  # (time, value)
data_2 = deque(maxlen=100)  # (time, value)

# Steuerung für das Beenden der Threads
stop_threads = False
pause_plotting = False  # Flag für das Pausieren des Neuzeichnens

# Echtzeitplot mit Matplotlib (muss im Hauptthread laufen)
plt.ion()  # Interaktiver Modus für Echtzeitplot
fig, ax = plt.subplots()  # Nur eine Achse ohne Histogramm
plt.subplots_adjust(bottom=0.4)  # Platz für Schaltflächen

# Annotation für Mouseover
annotation = ax.annotate("", xy=(0,0), xytext=(20,20),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)

# Funktion zur Berechnung der Zeitdifferenz in Sekunden
def time_diff(start_time):
    return [t - start_time for t, _ in data_1], [t - start_time for t, _ in data_2]

# Hauptplot-Funktion, die die Werte in Echtzeit darstellt
def update_plot():
    ax.clear()

    if data_1 and data_2:
        start_time = data_1[0][0]  # Starte von der ersten Messung des ersten Geräts

        # Extrahiere Zeiten und Werte
        times_1, values_1 = zip(*data_1)
        times_2, values_2 = zip(*data_2)

        # Konvertiere Zeiten in Differenzen zur ersten Messung (in Sekunden)
        times_1 = [t - start_time for t in times_1]
        times_2 = [t - start_time for t in times_2]

        ax.plot(times_1, values_1, label=Geraet1, marker='*', linestyle='-')
        ax.plot(times_2, values_2, label=Geraet2, marker='*', linestyle='-')

        ax.legend()
        ax.set_xlabel('Zeit (s)')
        ax.set_ylabel('Messwert')
        ax.grid(True)

    plt.draw()

# Funktion, die in einem Thread für jedes Messgerät läuft und Werte liest
def read_device1(device, data_queue, mode):
    global stop_threads
    while not stop_threads:
        value = device.getMeasure()
        timestamp = time.time()  # Erfasse die aktuelle Zeit
        data_queue.append((timestamp, value))  # Speichere Zeit und Wert
        time.sleep(3)

def read_device2(device, data_queue, mode):
    global stop_threads
    while not stop_threads:
        value = device.getMeasure()
        timestamp = time.time()  # Erfasse die aktuelle Zeit
        data_queue.append((timestamp, value))  # Speichere Zeit und Wert
        time.sleep(3)

# Threads für jedes Gerät starten
thread_1 = threading.Thread(target=read_device1, args=(device_1, data_1, mode_device_1))
thread_2 = threading.Thread(target=read_device2, args=(device_2, data_2, mode_device_2))
thread_1.start()
thread_2.start()

# Schaltflächen für das Umschalten der Betriebsmodi und Pausieren
ax_button_reset = plt.axes([0.4, 0.1, 0.15, 0.075])  # Position für den Reset-Button
ax_button_pause = plt.axes([0.1, 0.1, 0.15, 0.075])  # Position für den Pause-Button

button_reset = Button(ax_button_reset, 'Reset Daten')  # Reset-Button
button_pause = Button(ax_button_pause, 'Pause Plotting')  # Pause-Button

# Funktion zum Zurücksetzen der Datenpuffer
def reset_data(event):
    global data_1, data_2
    data_1.clear()  # Leert den Datenpuffer von Gerät 1
    data_2.clear()  # Leert den Datenpuffer von Gerät 2
    print("Datenpuffer geleert")

# Funktion zum Pausieren des Neuzeichnens
def toggle_pause(event):
    global pause_plotting
    pause_plotting = not pause_plotting  # Toggle den Zustand
    button_pause.label.set_text('Resume Plotting' if pause_plotting else 'Pause Plotting')  # Ändere den Button-Text
    print("Neuzeichnen der Grafik pausiert." if pause_plotting else "Neuzeichnen der Grafik fortgesetzt.")

# Binde die Schaltflächen an die Callback-Funktionen
button_reset.on_clicked(reset_data)  # Reset-Button an die Funktion binden
button_pause.on_clicked(toggle_pause)  # Pause-Button an die Funktion binden

# Funktion, die ausgeführt wird, wenn das Fenster geschlossen wird
def on_close(event):
    global stop_threads
    stop_threads = True  # Threads stoppen
    plt.close('all')

# Event-Handler für das Schließen des Fensters binden
fig.canvas.mpl_connect('close_event', on_close)

def on_mouse_move(event):
    if event.inaxes == ax:  # Überprüfen, ob die Maus innerhalb der Achsen ist
        # Überprüfen, ob ein Punkt in der Nähe ist (für Gerät 1)
        for i, (t, y) in enumerate(data_1):
            if abs(event.xdata - (t - data_1[0][0])) < 0.2 and abs(event.ydata - y) < 0.2:
                annotation.xy = (t - data_1[0][0], y)
                annotation.set_text(f"{Geraet1}: {y:.2f}")
                annotation.set_visible(True)
                break
        else:  # Nur wenn kein Punkt gefunden wurde, wird die Annotation ausgeblendet
            annotation.set_visible(False)

        # Überprüfen für Gerät 2
        for i, (t, y) in enumerate(data_2):
            if abs(event.xdata - (t - data_2[0][0])) < 0.2 and abs(event.ydata - y) < 0.2:
                annotation.xy = (t - data_2[0][0], y)
                annotation.set_text(f"{Geraet2}: {y:.2f}")
                annotation.set_visible(True)
                break
        else:
            annotation.set_visible(False)

    fig.canvas.draw_idle()  # Aktualisiere die Darstellung

# Event-Handler für Mouseover binden
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Endlos-Schleife zur Aktualisierung des Plots
try:
    while not stop_threads:
        if not pause_plotting:
            update_plot()
        plt.pause(2)
finally:
    # Sauberes Beenden der Threads
    stop_threads = True
    thread_1.join()
    thread_2.join()
    print("Programm beendet.")
