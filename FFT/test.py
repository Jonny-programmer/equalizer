# Работа с графиками
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties

# Работа с данными
import numpy as np

# Работа с аудио
import librosa

# Анимация
from matplotlib import animation
import os

NAMES = {1 : "Junge_Junge_feat_Jamie_Hartman_-_Wicked_Hearts",
         2 : "Naked_Giants_-_Turns_Blue",
         3 : "Still_Corners_-_The_Trip"}
PATH = f'./Data_example/{NAMES[1]}.mp3'
FPS = 30

sample, sr = librosa.load(PATH)
sample = sample[20*sr:30*sr]
FFT_WINDOW_SIZE = int(sr/FPS)

S_DURATION = len(sample)/sr # длительность трека в секундах
S_MINUTES = int(S_DURATION/60)
if S_MINUTES<10: S_MINUTES = f"0{S_MINUTES}"
S_SECONDS = int((S_DURATION/60-int(S_DURATION/60))*60)
if S_SECONDS<10: S_SECONDS = f"0{S_SECONDS}"

yf = np.fft.rfft(sample)
xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1/sr)

labels_font = FontProperties(family='monospace', size=12, weight='normal', style='normal')
title_font = FontProperties(family='monospace', size=11, weight='normal', style='normal')
ann_font = FontProperties(family='monospace', size=10, weight='normal', style='italic')

fig= plt.figure(figsize=[13.5, 7.45])
gs = GridSpec(1, 1, figure=fig)

ax1 = fig.add_subplot(gs[0,0])

line, = ax1.plot([], [], color='#219ebc', linestyle='-', linewidth=1.2)

timecode = ax1.annotate(f"Timecode - : / {S_MINUTES}:{S_SECONDS}",
                        linespacing=1.5,
                        xy=(0.05, 0.95),
                        xycoords='axes fraction',
                        fontproperties=ann_font,
                        alpha=1)

ax1.grid(which='major', linewidth=1, alpha=0.6)
ax1.grid(which='minor', axis='both', linewidth=1, alpha=0.6)

ax1.tick_params(axis='both', which='both', direction="in", pad=7)

ax1.set_axisbelow(True)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax1.set_xlabel('$\\mu$ , Hz', fontproperties=labels_font)
ax1.set_ylabel('Normalized altitude', fontproperties=labels_font)

ax1.set_xlim(-500, 11500)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(2000))
ax1.xaxis.set_minor_locator(ticker.MultipleLocator(1000))

ax1.set_ylim(0, 1.1)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

plt.subplots_adjust(left=0.055,
                    bottom=0.065, 
                    right=0.975, 
                    top=0.975, 
                    wspace=0.4, 
                    hspace=0.4)

def init():
  return line, timecode

def update(frame):
  yf = abs(np.fft.rfft(sample[FFT_WINDOW_SIZE*frame: FFT_WINDOW_SIZE*(frame+1)]))
  yf = yf/np.linalg.norm(yf)
  xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1/sr)

  
  line.set_data(xf, yf)

  TIME_PASSED = int(frame/FPS)
  MINUTES_PASSED = int(TIME_PASSED/60)
  if MINUTES_PASSED<10: MINUTES_PASSED = f"0{MINUTES_PASSED}"
  SECONDS_PASSED = int((TIME_PASSED/60-int(TIME_PASSED/60))*60)
  if SECONDS_PASSED<10: SECONDS_PASSED = f"0{SECONDS_PASSED}"

  timecode.set(text=f"{MINUTES_PASSED}:{SECONDS_PASSED} / {S_MINUTES}:{S_SECONDS}")

  return line, timecode

ani = animation.FuncAnimation(fig, update, init_func=init, frames=int(len(sample)/sr)*FPS-1, interval=1/FPS, blit=True)
FFwriter = animation.FFMpegWriter(fps=FPS)
ani.save('./Plots_example/Animation.mp4', writer=FFwriter, dpi=100)