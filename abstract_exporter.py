from abc import ABC, abstractmethod

class AbstractExporter(ABC):
    @abstractmethod
    def export(self, data):
        pass

class JSONExporter(AbstractExporter):
    def export(self, data):
        import json
        return json.dumps(data)

class CSVExporter(AbstractExporter):
    def export(self, data):
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

def save_data(exporter: AbstractExporter, data):
    output = exporter.export(data)
    print(output)

data = [{"name": "ALice", "age": 30}, {"name": "Bob", "age": 25}]

save_data(JSONExporter(), data)
save_data(CSVExporter(), data)