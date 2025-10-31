# The Decorator Pattern lets you dynamically add behavior to an object
# without modifying its class.
# Think of it like “wrapping” an object with extra functionality.

class DataSource:
    def read(self) -> str:
        raise NotImplementedError

# --- Plain File Reader -------
class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self.filename = filename

    def read(self) -> str:
        with open(self.filename, "r") as f:
            return f.read()


class DataSourceDecorator(DataSource):
    """
    Base Decorator: This ensures all decorators behave like a `DataSource`.
    """
    def __init__(self, wrappee: DataSource):
        self.wrappee = wrappee

    def read(self) -> str:
        return self.wrappee.read()

# --- Concrete Decorators -------
class EncryptionDecorator(DataSourceDecorator):
    def read(self) -> str:
        data = self.wrappee.read()
        return "".join(chr(ord(c) + 1) for c in data)  # simple shift encryption


class CompressionDecorator(DataSourceDecorator):
    def read(self) -> str:
        data = self.wrappee.read()
        return data.replace(" ", "")  # naive "compression"


class LoggingDecorator(DataSourceDecorator):
    def read(self) -> str:
        print(f"[LOG] Reading from {self.wrappee.__class__.__name__}")
        return self.wrappee.read()

source = FileDataSource("example.txt")

# Add decorators dynamically
decorated = LoggingDecorator(
    CompressionDecorator(
        EncryptionDecorator(source)
    )
)

print(decorated.read())
