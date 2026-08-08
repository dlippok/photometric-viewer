import datetime
import os

def profiled(warn_above: int | None = None):
    def inner(func):
        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            ret = func(*args, **kwargs)
            duration: datetime.timedelta = datetime.datetime.now() - start
            millis = duration.microseconds * 0.001

            if 'ENABLE_PROFILING' in os.environ.keys() or (warn_above is not None and millis > warn_above):
                print(f"Duration of {func.__qualname__}: {millis} ms")
            return ret

        return wrapper
    return inner
