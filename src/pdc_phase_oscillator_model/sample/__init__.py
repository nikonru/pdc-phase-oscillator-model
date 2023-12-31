import numpy as np
import matplotlib.pyplot as plt

from pdc_phase_oscillator_model.utility import plot as plot_system


def _get_parameters(k):
    a, c, b = 1, 4, -k/2
    return a, c, b


def Z(theta, k):
    a, c, b = _get_parameters(k)
    t = -np.tanh(k*theta+b)
    return (t+a)/c


def Z_inv(z, k):
    a, c, b = _get_parameters(k)
    t = np.arctanh(a-z*c)-b
    return t/k


def Z_der(theta, k):
    a, c, b = _get_parameters(k)
    return -k/c * (1/np.cosh(k*theta+b)**2)


def delay(n, T, k):
    return n*T + Z_inv(1-T, k)


def beta_and_p(delay, T, k):
    p = delay//T
    return Z_der(delay-p*T, k), p


def plot_Z(k):
    fig, ax = plt.subplots(figsize=(30, 5))

    scale = 100
    x = [x/scale for x in range(2*scale)]
    y = [Z(y/scale, k=k) for y in range(2*scale)]

    ax.plot(x, y)
    ax.axhline(y=0, color='r', linestyle='-')
    ax.axvline(x=0, color='r', linestyle='-')
    ax.set_title(f"$k = {k}$")
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$Z$")
    ax.grid()


def plot(T, k, n, steps=50):
    d = delay(n, T, k)
    beta, p = beta_and_p(d, T, k)
    plot_system(lambda theta: Z(theta, k), d, steps=steps, title=fr"$\tau={d}, k={k}, \beta={beta}, p={p}$")


def plot_delay_period(n_range=None, k_range=None, title=r"$Z(\theta)=\frac{\tanh(k\theta+b)+a}{c}$"):
    if k_range is None:
        k_range = [1, 5]
    if n_range is None:
        n_range = [0, 3]

    fig, ax = plt.subplots(figsize=(10, 10))

    linestyles = ["solid", "dashed", "dashdot", "dotted"]
    colors = ["blue", "green", "red", "orange", "pink", "violet", "yellow"]
    i = j = 0

    period = np.linspace(0,1,100)
    for n in n_range:
        linestyle = linestyles[ i % len(linestyles)]
        i += 1
        for k in k_range:
            color = colors[j % len(linestyles)]
            ax.plot(delay(n, period, k), period, label=fr"$k={k}, n={n}$", color=color, linestyle=linestyle)
            j += 1

    ax.axhline(y=0, color='r', linestyle='-')
    ax.axvline(x=0, color='r', linestyle='-')

    ax.set_title(title)
    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel(r"$T$")
    ax.legend(loc="upper right")
    ax.grid()


class Latex:

    @staticmethod
    def Z(k=None):
        '''
        from IPython.display import display, Math
        display(Math(Latex.Z()))
        '''
        a, c, _ = _get_parameters(0)
        k = f"{'k' if not k else k}"
        return fr"$Z(\theta) = \frac{{-\tanh({k} \theta - {k}/2) + {a}}}{{{c}}}$"

    @staticmethod
    def Z_inv(k=None):
        '''
        from IPython.display import display, Math
        display(Math(Latex.Z_inv()))
        '''
        a, c, _ = _get_parameters(0)
        k = f"{'k' if not k else k}"
        return fr"$\theta(Z) = \frac{{\tanh^{{-1}}({a} - {c}Z) + {k}/2 }}{{{k}}}$"

    @staticmethod
    def Z_der(k=None):
        '''
        from IPython.display import display, Math
        display(Math(Latex.Z_der()))
        '''
        a, c, _ = _get_parameters(0)
        k = f"{'k' if not k else k}"
        return fr"$\Z'(\theta) = -\frac{{{k}}}{{{c}}} \cdot \frac{{1}}{{\cosh^{{2}}({k}\theta - {k}/2)}}$"
