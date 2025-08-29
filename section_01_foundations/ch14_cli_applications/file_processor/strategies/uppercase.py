from .base import ProcessorStrategy

class UppercaseStrategy(ProcessorStrategy):
    def process(self, data):
        return data.upper()