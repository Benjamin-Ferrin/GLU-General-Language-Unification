from ...events import bus
from ...property import GLUProperty


def emit(endpoint, *args):
    return bus.emit(endpoint, *args)