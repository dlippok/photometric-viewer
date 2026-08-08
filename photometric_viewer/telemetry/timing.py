import datetime

class Timing:
    def __init__(self):
        self._last_calls = {}

    def measure(self, name: str = 'main', action: str = "action"):
        last_call = self._last_calls.get(name)
        if not last_call:
            print(f"Initializing timer: {name}")
        else:
            timing  = datetime.datetime.now() - last_call
            print(f"{name}: Duration of {action}: {timing}")

        self._last_calls[name] = datetime.datetime.now()

_timing  = Timing()

def measure(*args, **kwargs):
    _timing.measure(*args, **kwargs)
