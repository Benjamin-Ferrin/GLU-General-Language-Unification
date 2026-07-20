from .events import bus
from .property import GLUProperty # Necessary so that GLUProperty is imported when GLU is imported


def emit(endpoint, *args, **kwargs):
    return bus.emit(endpoint, *args, **kwargs)