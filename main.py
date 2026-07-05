import wave
import numpy as np
import matplotlib.pyplot as plt

with wave.open("audio/new.wav", "rb") as f:
    width_to_dtype = {1: np.int8, 2: np.int16, 4: np.int32}
    dtype = width_to_dtype[f.getsampwidth()]
    fs = f.getframerate()
    n_frames = f.getnframes()
    raw = f.readframes(n_frames)

audio = np.frombuffer(raw, dtype=dtype).astype(np.float64)

t = np.arange(n_frames) / fs

plt.plot(t, audio)
plt.xlabel("Время, c")
plt.ylabel("Амплитуда")
plt.title("Аудио")
plt.savefig("results/audio.png")
plt.show()

def fft(x):
    N = len(x)

    if N == 1:
        return x

    even = fft(x[0::2])
    odd  = fft(x[1::2])

    W = np.exp(-2j * np.pi * np.arange(N//2) / N)

    return np.concatenate([even + W * odd,
                           even - W * odd])

N = 2 ** int(np.ceil(np.log2(len(audio))))
audio_padded = np.zeros(N)
audio_padded[:len(audio)] = audio

X = fft(audio_padded)

freqs = (np.arange(N) - N // 2) * fs / N
plt.plot(freqs, np.abs(np.roll(X, N // 2)))
plt.xlabel("Частота, Гц")
plt.ylabel("Амплитуда")
plt.title("Спектр")
plt.savefig("results/spectrum.png")
plt.show()