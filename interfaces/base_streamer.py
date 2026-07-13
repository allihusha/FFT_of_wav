from abc import ABC, abstractmethod


class Streamer(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def send(self, filepath): pass

    @abstractmethod
    def close(self): pass