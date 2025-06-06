import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from IPython.display import display, HTML


def smooth(scalars):
    if not scalars: return []
    weight = 1.8 * (1 / (1 + np.exp(-0.05 * len(scalars))) - 0.5)
    smoothed, last = [], scalars[0]

    for val in scalars:
        last = last * weight + (1 - weight) * val
        smoothed.append(last)

    return smoothed


def plot_loss(log_file, keys=['loss', 'eval_loss', 'lr', 'accuracy']):
    try:
        info = pd.read_json(log_file, lines=True)
    except: return

    keys = [k for k in keys if k in info.columns]
    fig, axes = plt.subplots(1, len(keys), figsize=(7 * len(keys), 5))
    if len(keys) == 1: axes = [axes]

    temp = []
    for i, key in enumerate(keys):
        df = info.dropna(subset=[key])
        steps = df['current_steps'].tolist()
        metrics = df[key].tolist()

        axes[i].plot(steps, metrics, color='#1f77b4', alpha=0.4, label='original')
        axes[i].plot(steps, smooth(metrics), color='#1f77b4', label='smoothed')
        axes[i].set_title(f'training {key}')
        axes[i].set_xlabel('step')
        axes[i].set_ylabel(key)
        axes[i].legend()

        if key == 'eval_loss':
            temp.extend([
                df.loc[df[key].idxmin()],
                df.iloc[-1]
            ])

    html = pd.DataFrame(temp + [info.iloc[-1]]).to_html()
    display(HTML("<div style='display: flex; justify-content: center;'>" + html + "</div>"))

    plt.tight_layout()
    plt.show()
