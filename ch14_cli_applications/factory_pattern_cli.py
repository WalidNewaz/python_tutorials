from abc import ABC, abstractmethod
import sys

class Renderer(ABC):
    @abstractmethod
    def render(self, data: dict) -> None:
        pass


class JsonRenderer(Renderer):
    def render(self, data: dict) -> None:
        import json
        print(json.dumps(data, indent=2))


class TextRenderer(Renderer):
    def render(self, data: dict) -> None:
        for key, value in data.items():
            print(f"{key:<8}: {value:<3}")


class RendererFactory:
    @staticmethod
    def create(fmt: str) -> Renderer:
        if fmt == "json":
            return JsonRenderer()
        elif fmt == "text":
            return TextRenderer()
        else:
            raise ValueError(f"Unknown renderer: {fmt}")


data = {"status": "ok", "version": "1.0", "link": "https://www.google.com/"}

def main():
    if len(sys.argv) < 2:
        print("Usage: {} [text|json]".format(sys.argv[0]))
        return

    command = sys.argv[1]
    render_cmd = RendererFactory.create(command)
    render_cmd.render(data)


if __name__ == "__main__":
    main()
