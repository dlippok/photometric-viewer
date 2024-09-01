from functools import wraps

def signal_handler(*args):
    def decorator(f):
        copy = [a for a in args]
        while len(copy) > 0:
            target = copy.pop(0)
            signal = copy.pop(0)
            target.connect(signal, f)
        return f
    return decorator
