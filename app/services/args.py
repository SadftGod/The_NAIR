import argparse

class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Start NAIR")
        
        self.parser.add_argument("--ui", action="store_true", help="Start NAIR Admin Panel UI (NiceGUI)")
        self.parser.add_argument("--debug", action="store_true", help="Debug mode")
        self.parser.add_argument("--host", type=str, default="127.0.0.1", help="Host for UI (default 127.0.0.1)")
        self.parser.add_argument("--port", type=int, default=8080, help="Port for UI (default 8080)")

        self.args = self.parser.parse_args()

    def ui_enabled(self) -> bool:
        return self.args.ui

    def is_debug(self) -> bool:
        return self.args.debug

    def host(self) -> str:
        return self.args.host

    def port(self) -> int:
        return self.args.port

