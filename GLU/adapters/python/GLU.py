from ...events import bus

def emit(endpoint, *args):
    return bus.emit(endpoint, *args)