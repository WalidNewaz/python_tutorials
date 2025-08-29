from abc import ABC, abstractmethod

class ProcessorStrategy(ABC):
    @abstractmethod
    def process(self, data):
        raise NotImplementedError()