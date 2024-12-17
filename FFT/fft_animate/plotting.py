# Audio
import librosa

# Plotting
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties

# Animation
from matplotlib import animation

# Source code
import numpy as np
from . import source
from pathlib import Path
import os

# Typing
from typing import Union
from matplotlib.axes import Axes

def _ax_apply_default_settings(ax : Axes) -> None:

    ax.grid(which='major', linewidth=1, alpha=0.6)
    ax.grid(which='minor', axis='both', linewidth=1, alpha=0.6)

    ax.tick_params(axis='both', which='both', direction="in", pad=7)

    ax.set_axisbelow(True)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlim(-500, 11500)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2000))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1000))

    ax.set_ylim(0, 1.1)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

    plt.subplots_adjust(left=0.055,
                        bottom=0.065, 
                        right=0.975, 
                        top=0.975, 
                        wspace=0.4, 
                        hspace=0.4)
    return None

def Convert_to_mp4(path : str,
                   #text : str,
                   fps : int = 30,
                   out_path : str = None):
    labels_font = FontProperties(family='monospace', size=12, weight='normal', style='normal')
    title_font = FontProperties(family='monospace', size=11, weight='normal', style='normal')
    ann_font = FontProperties(family='monospace', size=10, weight='normal', style='italic')
    
    sample, rate = librosa.load(path)
    FFT_window_width = int(rate/fps)

    fig= plt.figure(figsize=[13.5, 7.45])
    gs = GridSpec(1, 1, figure=fig)
    ax = fig.add_subplot(gs[0,0])

    line, = ax.plot([], [], color='#219ebc', linestyle='-', linewidth=1.2)

    duration = source._timecode_convert(len(sample)/rate)
    timecode = ax.annotate(f"Timecode - : / {duration}",
                        linespacing=1.5,
                        xy=(0.05, 0.95),
                        xycoords='axes fraction',
                        fontproperties=ann_font,
                        alpha=1)
    
    ax.set_xlabel('$\\mu$ , Hz', fontproperties=labels_font)
    ax.set_ylabel('Normalized altitude', fontproperties=labels_font)

    _ax_apply_default_settings(ax=ax)

    def init():
        return line, timecode

    def update(frame):
        yf = abs(np.fft.rfft(sample[FFT_window_width*frame: FFT_window_width*(frame+1)]))
        yf = yf/np.linalg.norm(yf)
        xf = np.fft.rfftfreq(FFT_window_width, 1/rate)

        line.set_data(xf, yf)
        timecode.set(text=f"{source._timecode_convert(int(frame/fps))} / {duration}")

        return line, timecode

    ani = animation.FuncAnimation(fig,
                                  update,
                                  init_func=init,
                                  frames=int(len(sample)/rate)*fps-1,
                                  interval=1/fps,
                                  blit=True)
    FFwriter = animation.FFMpegWriter(fps=fps)

    if not out_path:
        ani.save(f'{str(Path.home()/"Downloads")}/{Path(path).stem}', writer=FFwriter, dpi=100)
    else:
        ani.save(out_path, writer=FFwriter, dpi=100)