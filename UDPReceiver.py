import socket
import struct
import wave
import numpy as np
import matplotlib.pyplot as plt
from interfaces.base_receiver import Receiver
from fft_utils import fft
from noise_filter import filter_noise, compute_snr


class UDPReceiver(Receiver):
    def __init__(self, host: str = "127.0.0.1", port: int = 5005, buffer_size: int = 65535):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self.audio = None
        self.filtered_audio = None
        self.fs = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"Receiver слушает: {self.host}:{self.port}")

    def receive(self):
        header_data, _ = self.socket.recvfrom(self.buffer_size)
        total_chunks, fs, sampwidth = struct.unpack("!III", header_data)
        self.fs = fs

        width_to_dtype = {1: np.int8, 2: np.int16, 4: np.int32}
        dtype = width_to_dtype[sampwidth]

        print(f"Получен заголовок: {total_chunks} пакетов, "
              f"fs={fs}, "
              f"sampwidth={sampwidth}, "
              f"dtype={dtype.__name__}")


        raw = b""
        received = 0
        while True:
            data, _ = self.socket.recvfrom(self.buffer_size)
            if data == b"END":
                print("Получен сигнал окончания")
                break
            raw += data
            received += 1
            print(f"Получен пакет {received}/{total_chunks} ({len(data)} байт)")

        self.audio = np.frombuffer(raw, dtype=dtype).astype(np.float64)
        print(f"Аудио собрано: {len(self.audio)} сэмплов")

    def close(self):
        if self.socket:
            self.socket.close()
            print("Соединение закрыто")

    def filter_audio(self):
        filtered_audio = filter_noise(self.audio)
        self.filtered_audio = filtered_audio

        filtered_audio_int16 = filtered_audio.astype(np.int16)
        with wave.open("audio/filtered_audio.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(filtered_audio_int16.tobytes())

    def plot_comparison(self):
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        t = np.arange(len(self.audio)) / self.fs

        axes[0, 0].plot(t, self.audio)
        axes[0, 0].set_xlabel("Время, c")
        axes[0, 0].set_ylabel("Амплитуда")
        axes[0, 0].set_title("Исходное аудио")

        t = np.arange(len(self.filtered_audio)) / self.fs

        axes[0, 1].plot(t, self.filtered_audio)
        axes[0, 1].set_xlabel("Время, c")
        axes[0, 1].set_ylabel("Амплитуда")
        axes[0, 1].set_title("Отфильтрованное аудио")

        N = 2 ** int(np.ceil(np.log2(len(self.audio))))
        audio_padded = np.zeros(N)
        audio_padded[:len(self.audio)] = self.audio

        X = fft(audio_padded)

        freqs = (np.arange(N) - N // 2) * self.fs / N
        axes[1, 0].plot(freqs, np.abs(np.roll(X, N // 2)))
        axes[1, 0].set_xlabel("Частота, Гц")
        axes[1, 0].set_ylabel("Амплитуда")
        axes[1, 0].set_title("Спектр исходного аудио")

        N = 2 ** int(np.ceil(np.log2(len(self.filtered_audio))))
        audio_padded = np.zeros(N)
        audio_padded[:len(self.filtered_audio)] = self.filtered_audio

        X = fft(audio_padded)

        freqs = (np.arange(N) - N // 2) * self.fs / N
        axes[1, 1].plot(freqs, np.abs(np.roll(X, N // 2)))
        axes[1, 1].set_xlabel("Частота, Гц")
        axes[1, 1].set_ylabel("Амплитуда")
        axes[1, 1].set_title("Спектр отфильтрованного аудио")

        snr = compute_snr(self.filtered_audio, self.audio - self.filtered_audio)

        fig.suptitle(f"SNR = {snr}")
        plt.tight_layout(h_pad=3.0)
        plt.savefig("results/comparison.png")
        plt.show()

if __name__ == "__main__":
    receiver = UDPReceiver()
    receiver.start()
    receiver.receive()
    receiver.close()
    receiver.filter_audio()
    receiver.plot_comparison()