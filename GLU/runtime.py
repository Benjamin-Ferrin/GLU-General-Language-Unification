import importlib
from .parser import parse, Endpoint

class GLURuntime:
    def __init__(self, config):
        self.bindings = parse(config)

    def emit(self, endpoint, *args):

        ep = Endpoint(endpoint)
        if ep.getLanguage() != "py":
            raise Exception(
                "Only py adapter is supported currently"
            )

        module = importlib.import_module(
            ep.getFilePath()
        )
        function = getattr(
            module,
            ep.getObject()
        )
        return function(*args)
    
    
class GLUProperty:
    def __init__(self, value):
        self.value = value
        self.changed = None

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        if self.changed:
            self.changed()
