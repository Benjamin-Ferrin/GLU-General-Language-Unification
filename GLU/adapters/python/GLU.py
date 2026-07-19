from ...events import bus
from ...property import GLUProperty


def emit(endpoint, *args, **kwargs):
    return bus.emit(endpoint, *args, **kwargs)