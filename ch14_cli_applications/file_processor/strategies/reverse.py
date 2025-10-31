from .base import ProcessorStrategy

class ReverseStrategy(ProcessorStrategy):
    def process(self, data):
        return data[::-1]