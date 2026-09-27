import pygame
import numpy as np
import tkinter as tk
from tkmacosx import Button

pygame.mixer.init(frequency=44100, size=-16, channels=2)

duration = 0.07
frequency1 = 880
sample_rate = 44100 

def make_click(frequency, duration=0.07):
    t = np.linspace(0, duration, int(sample_rate * duration))
    pitch_env = np.exp(-t * 400)
    pitch_env = pitch_env / pitch_env.max() * 0.4 + 0.8
    samples = np.sin(2 * np.pi * frequency * pitch_env * t)
    envelope = np.exp(-t * 100)
    samples = samples * envelope
    samples = (samples * 32767).astype(np.int16)
    samples = np.column_stack((samples, samples))
    return pygame.sndarray.make_sound(samples)

click_eins = make_click(880)
click = make_click(660)
click.set_volume(0.4)

mybg = "#D75932"   #"#C5522E"
mytext = "#FFFFFF"
mainfont = ('Helvetica', 11)

root = tk.Tk()
root.title('Metronom')
root.geometry('400x330')
root.maxsize(400, 450)
root.configure(bg=mybg)

laeuft = False
zaehler = 0

# BPM Logik
v_bpm = tk.StringVar(value="120")

def fokus_entfernen(event):
    # Nur Fokus entfernen, wenn NICHT das Eingabefeld angeklickt wurde
    if event.widget != e_bpm:
        root.focus_set()

root.bind("<Button-1>", fokus_entfernen)

def on_bpm_entry_change(*args):
    try:
        val = int(v_bpm.get())
        if 20 <= val <= 240:
            slider_bpm.set(val)
    except ValueError:
        pass

def on_slider_change(val):
    v_bpm.set(str(int(float(val))))

v_bpm.trace_add("write", on_bpm_entry_change)

def takt():
    global zaehler
    if laeuft:
        teiler = slider_takt.get()
        zaehler = (zaehler % teiler) + 1
        if zaehler == 1:
            click_eins.play()
        else:
            click.play()
        for p in punkte:
            p.config(fg=mybg)
        if zaehler == 1:
            punkte[0].config(fg='white')
        else:
            punkte[zaehler - 1].config(fg="#E9E9E9")
        root.after(100, lambda: punkte[zaehler - 1].config(fg=mybg))
        
        intervall = int(60000 / slider_bpm.get())
        root.after(intervall, takt)

def start_stop():
    global laeuft
    if laeuft == False:
        laeuft = True
        l_play.config(text='⏸')
        takt()
    else:
        laeuft = False
        l_play.config(text='▶')

def update_punkte(val=None):
    takt_anzahl = slider_takt.get()
    # Zentrierte Time-Anzeige aktualisieren
    l_takt_anzeige.config(text='Time: ' + str(takt_anzahl) + '/4')
    
    erste_zeile = min(takt_anzahl, 4)
    zweite_zeile = max(takt_anzahl - 4, 0)
    for i in range(len(punkte)):
        if i < takt_anzahl:
            zeile = i // 4
            spalte = i % 4
            if zeile == 0:
                relx = 0.5 - (erste_zeile - 1) * 0.08 + spalte * 0.16
            else:
                relx = 0.5 - (zweite_zeile - 1) * 0.08 + spalte * 0.16
            rely = 0.13 if zeile == 0 else 0.32
            punkte[i].place(relx=relx, rely=rely, anchor='center')
        else:
            punkte[i].place_forget()

# GUI Elemente
l_play = Button(root, text='▶', font=mainfont, bg=mybg, fg=mytext, 
                borderless=1, width=80, command=start_stop)

punkte = [tk.Label(root, text=str(i+1) if i > 0 else '①', font=('Helvetica', 40), bg=mybg, fg=mybg) for i in range(8)]

# BPM Bereich
f_bpm = tk.Frame(root, bg=mybg)
l_bpm_text = tk.Label(f_bpm, text="BPM: ", font=mainfont, bg=mybg, fg=mytext)
# Eingabefeld mit grauem Hintergrund und schwarzer Schrift
e_bpm = tk.Entry(f_bpm, textvariable=v_bpm, font=mainfont, width=4, justify='center', fg='white', bg=mybg, borderwidth=0, highlightthickness=0)
l_bpm_text.pack(side='left')
e_bpm.pack(side='left')
f_bpm.place(relx=0.5, rely=0.51, anchor='center')

slider_bpm = tk.Scale(root, from_=20, to=240, bg=mybg, fg=mytext, orient='horizontal', 
                      showvalue=0, highlightthickness=0, command=on_slider_change)
slider_bpm.set(120)
slider_bpm.place(relx=0.5, rely=0.60, anchor='center', width=int(400*0.37))

# Time Bereich (Zentriertes Label + Slider ohne eigenes Label)
l_takt_anzeige = tk.Label(root, text='Time: 4/4', font=mainfont, bg=mybg, fg=mytext)
l_takt_anzeige.place(relx=0.5, rely=0.68, anchor='center')

slider_takt = tk.Scale(root, from_=1, to=8, bg=mybg, fg=mytext, 
                       orient='horizontal', font=mainfont, highlightthickness=0, 
                       command=update_punkte, showvalue=0)
slider_takt.set(4)
slider_takt.place(relx=0.5, rely=0.75, anchor='center', width=int(400*0.37))

l_play.place(relx=0.5, rely=0.90, anchor='center')

update_punkte()
root.mainloop()
