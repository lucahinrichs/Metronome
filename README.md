# Metronome

A simple, minimalist metronome built with Python, Tkinter, and pygame for real-time sound synthesis.

## Why this project?

I've been playing bass and needed a metronome - so instead of grabbing an app, I built my own as a practice project while learning Python.

https://github.com/user-attachments/assets/b31af8ce-519f-43ee-a54c-84a2f5625ce0

## Features

- Adjustable tempo (BPM), via slider or direct text input
- Adjustable time signature (1/4 up to 8/4)
- Visual beat indicator with accented downbeat
- Custom click sounds synthesized in real time with `pygame` and `numpy` (no audio samples needed)

## Tech stack

- **Python 3**
- **Tkinter** – GUI
- **tkmacosx** – for a borderless, styled button on macOS
- **pygame** – audio playback
- **numpy** – generating the click sound waveforms

## How the sound works

Each click is synthesized on the fly: a sine wave with a quick pitch drop and volume envelope, turned into raw audio samples and handed to `pygame.mixer`. The downbeat and the other beats use different pitches so you can hear the "1" of each bar.

## Running it

```bash
pip3 install pygame numpy tkmacosx
python3 Metronom_3.py
```

## Status

Practice project - built to learn GUI programming and basic audio synthesis, and to get playing.
