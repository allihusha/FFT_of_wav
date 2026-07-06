from abc import ABC, abstractmethod


class Receiver(ABC):
    @abstractmethod
    def start(self): pass

    @abstractmethod
    def receive(self): pass

    @abstractmethod
    def plot_spectrum(self): pass

    @abstractmethod
    def plot_audio(self): pass

    @abstractmethod
    def close(self): pass