import numpy as np


def fft(x):
    N = len(x)

    if N == 1:
        return x

    even = fft(x[0::2])
    odd  = fft(x[1::2])

    W = np.exp(-2j * np.pi * np.arange(N//2) / N)

    return np.concatenate([even + W * odd, even - W * odd])