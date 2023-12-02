import numpy as np
import matplotlib.pyplot as plt

from model import Model


def plot(Z, delay, steps, title="", period=1, transient_process=300, abs_error=0.0001):
    fig, ax = plt.subplots(figsize=(30, 5))

    ds = Model(period, Z=Z, delay=delay, abs_err=abs_error)

    t, phases = ds.simulate(transient_process + steps)

    t = t[-steps:]
    phases = phases[-steps:]

    ax.plot(t, phases)

    minimum = min(t)

    ax.axhline(y=0, color='r', linestyle='-')
    ax.axvline(x=minimum, color='r', linestyle='-')

    ax.set_xticks(np.arange(min(t), max(t)+1, 1))
    ax.set_title(title)
    ax.set_xlim(left=minimum)

    ax.set_xlabel(r"$t$", fontsize=20)
    ax.set_ylabel(r"$\theta$", fontsize=20)

    ax.grid()
