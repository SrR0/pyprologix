import threading
import time
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.widgets import Button
from pm2534 import pm2534
from hp3478a import hp3478a

# Initialisiere die Messgeräte (pm2534 und hp3478a)
device_1 = pm2534(22, "COM11", debug=False)
device_2 = hp3478a(23, "COM12", debug=False)

Geraet1 = 'PM2534'
Geraet2 = 'HP3478A'

# Betriebsmodus für die Geräte
mode_device_1 = "Mode A"
mode_device_2 = "Mode A"

# Datenpuffer für jedes Messgerät (deque für die Echtzeitdaten)
data_1 = deque(maxlen=100)
data_2 = deque(maxlen=100)

# Steuerung für das Beenden der Threads
stop_threads = False
pause_plotting = False  # Flag für das Pausieren des Neuzeichnens

# Echtzeitplot mit Matplotlib (muss im Hauptthread laufen)
plt.ion()  # Interaktiver Modus für Echtzeitplot
fig, (ax, ax_hist) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})
plt.subplots_adjust(bottom=0.4, hspace=0.4)  # Platz für Schaltflächen und Abstand zwischen Plots

# Annotation für Mouseover
annotation = ax.annotate("", xy=(0,0), xytext=(20,20),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)

# Hauptplot-Funktion, die die Werte in Echtzeit darstellt
def update_plot():
    ax.clear()
    ax.plot(data_1, label=Geraet1, marker='*', linestyle='-')  # Plot für Gerät 1 mit Sternen
    ax.plot(data_2, label=Geraet2, marker='*', linestyle='-')  # Plot für Gerät 2 mit Sternen
    ax.legend()
    ax.grid(True)  # Gittermuster aktivieren

    # Histogramm aktualisieren
    ax_hist.clear()
    ax_hist.hist(data_1, bins=10, alpha=0.5, label=Geraet1)  # Histogramm für Gerät 1
    ax_hist.hist(data_2, bins=10, alpha=0.5, label=Geraet2)  # Histogramm für Gerät 2
    ax_hist.legend()
    ax_hist.set_title('Histogramm der Messwerte')
    ax_hist.grid(True)

    plt.draw()

# Funktion, die in einem Thread für jedes Messgerät läuft und Werte liest
def read_device1(device, data_queue, mode):
    global stop_threads
    while not stop_threads:
        value = device.getMeasure()
        data_queue.append(value)
        print(f"Device 1 running in {mode}")
        time.sleep(1)

def read_device2(device, data_queue, mode):
    global stop_threads
    while not stop_threads:
        value = device.getMeasure()
        data_queue.append(value)
        print(f"Device 2 running in {mode}")
        time.sleep(1)

# Threads für jedes Gerät starten
thread_1 = threading.Thread(target=read_device1, args=(device_1, data_1, mode_device_1))
thread_2 = threading.Thread(target=read_device2, args=(device_2, data_2, mode_device_2))
thread_1.start()
thread_2.start()

# Schaltflächen für das Umschalten der Betriebsmodi und Pausieren
ax_button_1_mode_a = plt.axes([0.1, 0.25, 0.1, 0.075])
ax_button_1_mode_b = plt.axes([0.25, 0.25, 0.1, 0.075])
ax_button_2_mode_a = plt.axes([0.55, 0.25, 0.1, 0.075])
ax_button_2_mode_b = plt.axes([0.7, 0.25, 0.1, 0.075])
ax_button_reset = plt.axes([0.4, 0.05, 0.2, 0.075])  # Position für den Reset-Button
ax_button_pause = plt.axes([0.1, 0.1, 0.2, 0.075])  # Position für den Pause-Button

button_1_mode_a = Button(ax_button_1_mode_a, 'Gerät 1 Mode A')
button_1_mode_b = Button(ax_button_1_mode_b, 'Gerät 1 Mode B')
button_2_mode_a = Button(ax_button_2_mode_a, 'Gerät 2 Mode A')
button_2_mode_b = Button(ax_button_2_mode_b, 'Gerät 2 Mode B')
button_reset = Button(ax_button_reset, 'Reset Daten')  # Reset-Button
button_pause = Button(ax_button_pause, 'Pause Plotting')  # Pause-Button

# Callback-Funktionen, die den Modus ändern
def set_device_1_mode_a(event):
    global mode_device_1
    mode_device_1 = "Mode A"
    print("Gerät 1 auf Mode A umgeschaltet")

def set_device_1_mode_b(event):
    global mode_device_1
    mode_device_1 = "Mode B"
    print("Gerät 1 auf Mode B umgeschaltet")

def set_device_2_mode_a(event):
    global mode_device_2
    mode_device_2 = "Mode A"
    print("Gerät 2 auf Mode A umgeschaltet")

def set_device_2_mode_b(event):
    global mode_device_2
    mode_device_2 = "Mode B"
    print("Gerät 2 auf Mode B umgeschaltet")

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
button_1_mode_a.on_clicked(set_device_1_mode_a)
button_1_mode_b.on_clicked(set_device_1_mode_b)
button_2_mode_a.on_clicked(set_device_2_mode_a)
button_2_mode_b.on_clicked(set_device_2_mode_b)
button_reset.on_clicked(reset_data)  # Reset-Button an die Funktion binden
button_pause.on_clicked(toggle_pause)  # Pause-Button an die Funktion binden

# Funktion, die ausgeführt wird, wenn das Fenster geschlossen wird
def on_close(event):
    global stop_threads
    stop_threads = True  # Threads stoppen
    plt.close('all')

# Event-Handler für das Schließen des Fensters binden
fig.canvas.mpl_connect('close_event', on_close)

# Funktion zum Mouseover-Event
def on_mouse_move(event):
    if event.inaxes == ax:  # Überprüfen, ob die Maus innerhalb der Achsen ist
        # Überprüfen, ob ein Punkt in der Nähe ist
        for i, (x, y) in enumerate(zip(range(len(data_1)), data_1)):
            if abs(event.xdata - x) < 0.2 and abs(event.ydata - y) < 0.2:
                annotation.xy = (x, y)
                annotation.set_text(f"{Geraet1}: {y:.2f}")
                annotation.set_visible(True)
                break
        else:  # Nur wenn kein Punkt gefunden wurde, wird die Annotation ausgeblendet
            annotation.set_visible(False)
        # Überprüfen für Gerät 2
        for i, (x, y) in enumerate(zip(range(len(data_2)), data_2)):
            if abs(event.xdata - x) < 0.2 and abs(event.ydata - y) < 0.2:
                annotation.xy = (x, y)
                annotation.set_text(f"{Geraet2}: {y:.2f}")
                annotation.set_visible(True)
                break

        fig.canvas.draw_idle()  # Zeichne das Fenster neu

# Event-Handler für Mouseover binden
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Endlos-Schleife zur Aktualisierung des Plots
try:
    while not stop_threads:
        if not pause_plotting:
            update_plot()
        plt.pause(1)
finally:
    # Sauberes Beenden der Threads
    stop_threads = True
    thread_1.join()
    thread_2.join()
    print("Programm beendet.")
