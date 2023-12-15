from abc import ABC, abstractmethod

class Software(ABC):
    @abstractmethod
    def start(self):
        """"""

    @abstractmethod
    def stop(self):
        """"""


class DefaultSoftware(Software):
    def start(self):
        pass

    def stop(self):
        pass