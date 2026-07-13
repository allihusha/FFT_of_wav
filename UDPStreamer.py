import wave
import socket
import struct
import time
from interfaces.base_streamer import Streamer


class UDPStreamer(Streamer):
    def __init__(self, host: str = "127.0.0.1", port: int = 5005, chunk_size: int = 320):
        self.host = host
        self.port = port
        self.chunk_size = chunk_size
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Streamer подключён: {self.host}:{self.port}")

    def send(self, filepath):
        with wave.open(filepath, "rb") as f:
            fs = f.getframerate()
            sampwidth = f.getsampwidth()
            n_frames = f.getnframes()
            raw = f.readframes(n_frames)

        chunks = [raw[i:i + self.chunk_size] for i in range(0, len(raw), self.chunk_size)]
        total_chunks = len(chunks)

        header = struct.pack("!III", total_chunks, fs, sampwidth)
        self.socket.sendto(header, (self.host, self.port))
        print(f"Отправлен заголовок: {total_chunks} пакетов, fs={fs}")
        time.sleep(0.01)

        for i, chunk in enumerate(chunks):
            self.socket.sendto(chunk, (self.host, self.port))
            print(f"Отправлен пакет {i + 1}/{total_chunks} ({len(chunk)} байт)")
            time.sleep(0.001)

        self.socket.sendto(b"END", (self.host, self.port))
        print("Передача завершена")

    def close(self):
        if self.socket:
            self.socket.close()
            print("Соединение закрыто")


if __name__ == "__main__":
    streamer = UDPStreamer()
    streamer.connect()
    streamer.send("audio/audio.wav")
    streamer.close()