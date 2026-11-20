# Slap Bot

Smart boxing dummy that scores strikes by force and location.
Cornerstone of Engineering team project, Spring 2026. Three-person team.

## My contribution

Sensor integration, the analog signal path, and all software in this repo.
I embedded the force-sensitive resistors, designed the multiplexed read
circuit, and wrote the MicroPython firmware and MATLAB analysis.

## How it works

Three FSRs are embedded in a head-shaped target, each in a voltage divider.
The Raspberry Pi Pico exposes only three ADC channels, so the sensors are
routed through a CD4051 eight-channel analog multiplexer, reading all of
them through a single ADC pin using four pins total.

Before each trial the firmware averages a fresh baseline over fifteen
samples per channel, then tracks the peak change from that baseline across
a one-second window. The strongest cheek reading is scaled to a readable
score. Chin strikes are illegal in the sport, so a third sensor zeroes the
score when it exceeds both cheek sensors by a set margin. Results display
on a 16x2 LCD over I2C.

## Files

- `slapbot.py` — MicroPython firmware
- `analysis.m` — MATLAB script, reads the logged CSV and plots the channels
- `fsr_data.csv` — sample logged session

## Hardware

Raspberry Pi Pico, CD4051 8:1 analog mux, 3x FSRs in voltage dividers,
16x2 I2C LCD at 0x27.

## Known limitations

Measured sampling rate was about 14 Hz per channel, roughly 71 ms between
samples. The serial logging accounted for more of that than the sampling
itself. That was adequate for scoring relative strike force but too slow
to characterize the impact event.

Channels are read sequentially through the multiplexer, about 7 ms apart,
so the three are not sampled simultaneously.

Peak readings reached about 93% of the ADC's full scale, so a harder strike
would have clipped.

FSRs creep: in a logged session the resting floor between strikes climbed
from roughly 2,700 to 22,000 counts. Recalibrating the baseline before each
trial handled most of this, but a small percentage of clean cheek strikes
still registered as chin hits.
