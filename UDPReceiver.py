import socket
import struct
import numpy as np
import matplotlib.pyplot as plt
from interfaces.base_receiver import Receiver
from fft_utils import fft


class UDPReceiver(Receiver):
    def __init__(self, host: str = "127.0.0.1", port: int = 5005, buffer_size: int = 65535):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self.audio = None
        self.n_frames = None
        self.fs = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"Receiver слушает: {self.host}:{self.port}")

    def receive(self):
        header_data, _ = self.socket.recvfrom(self.buffer_size)
        total_chunks, fs, n_frames, sampwidth = struct.unpack("!IIII", header_data)
        self.n_frames = n_frames
        self.fs = fs

        width_to_dtype = {1: np.int8, 2: np.int16, 4: np.int32}
        dtype = width_to_dtype[sampwidth]

        print(f"Получен заголовок: {total_chunks} пакетов, "
              f"fs={fs}, "
              f"n_frames={n_frames}, "
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

    def plot_audio(self):
        t = np.arange(self.n_frames) / self.fs

        plt.plot(t, self.audio)
        plt.xlabel("Время, c")
        plt.ylabel("Амплитуда")
        plt.title("Аудио")
        plt.savefig("results/audio.png")
        plt.show()

    def plot_spectrum(self):

        N = 2 ** int(np.ceil(np.log2(len(self.audio))))
        audio_padded = np.zeros(N)
        audio_padded[:len(self.audio)] = self.audio

        X = fft(audio_padded)

        freqs = (np.arange(N) - N // 2) * self.fs / N
        plt.plot(freqs, np.abs(np.roll(X, N // 2)))
        plt.xlabel("Частота, Гц")
        plt.ylabel("Амплитуда")
        plt.title("Спектр")
        plt.savefig("results/spectrum.png")
        plt.show()

if __name__ == "__main__":
    receiver = UDPReceiver()
    receiver.start()
    receiver.receive()
    receiver.close()
    receiver.plot_audio()
    receiver.plot_spectrum()