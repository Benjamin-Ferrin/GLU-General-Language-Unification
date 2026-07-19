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
            
    def bind(self, variable, endpoint, *args):
        pass
    
    def removeBinding(self, enpoint):
        pass