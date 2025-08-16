# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import webbrowser
import os
#filename="ADC20250730_211456_100KHz"
#filename="ADC20250730_211231_1KHz.csv"
#filename="ADC20250730_211758_500KHz"
filename="ADC20250730_212443_1MHz.csv"

# === 1. Считываем CSV ===
df = pd.read_csv("ADC20250730_211231_1KHz.csv", header=None)
sensor1 = df[0].values
sensor2 = df[1].values

# Создаём ось времени (если в файле нет времени, шаг = 1)
t = np.arange(len(sensor1))

# === 2. Sensor signals plot ===
fig_signals = go.Figure()
fig_signals.add_trace(go.Scatter(x=t, y=sensor1, mode='lines', name='Sensor 1'))
fig_signals.add_trace(go.Scatter(x=t, y=sensor2, mode='lines', name='Sensor 2'))

fig_signals.update_layout(
    title="Sensor Readings",
    xaxis_title="Time (samples)",
    yaxis_title="Amplitude",
    template="plotly_white"
)

# === 3. Фурье (амплитуда + фаза) ===
# БПФ
fft1 = np.fft.fft(sensor1)
fft2 = np.fft.fft(sensor2)
freqs = np.fft.fftfreq(len(sensor1), d=1)  # d — шаг времени (1 отсчёт)

# Оставляем положительные частоты
mask = freqs >= 0
freqs = freqs[mask]
amp1 = np.abs(fft1[mask])
amp2 = np.abs(fft2[mask])
phase1 = np.angle(fft1[mask])
phase2 = np.angle(fft2[mask])

# === 4. Amplitude plot ===
fig_fft = go.Figure()

fig_fft.add_trace(go.Scatter(x=freqs, y=amp1, mode='lines', name='Amplitude Sensor 1'))
fig_fft.add_trace(go.Scatter(x=freqs, y=amp2, mode='lines', name='Amplitude Sensor 2'))

# === 5. Phase plot ===
fig_fft.add_trace(go.Scatter(x=freqs, y=phase1, mode='lines', name='Phase Sensor 1', yaxis="y2"))
fig_fft.add_trace(go.Scatter(x=freqs, y=phase2, mode='lines', name='Phase Sensor 2', yaxis="y2"))

# === 6. Two Y axes ===
fig_fft.update_layout(
    title="Fourier Spectrum: Amplitude and Phase",
    xaxis_title="Frequency (Hz)",
    yaxis=dict(title="Amplitude"),
    yaxis2=dict(title="Phase (rad)", overlaying="y", side="right"),
    template="plotly_white"
)


# === 4. Генерация имён выходных файлов ===
base_name = os.path.splitext(os.path.basename(filename))[0]
signals_file = f"{base_name}_signals.html"
fft_file = f"{base_name}_fft.html"

# === 5. Сохраняем HTML ===
fig_signals.write_html(signals_file)
fig_fft.write_html(fft_file)


# =============================================================================
# fig_signals.show()
# fig_fft.show()
# 
# =============================================================================
webbrowser.open(signals_file)
webbrowser.open(fft_file)

