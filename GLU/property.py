from .events import bus

class GLUProperty:
    def __init__(self, value):
        self.value = value
        self.bindings = {}

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

        for endpoint, callbacks in self.bindings.items():
            for args, kwargs in callbacks:

                resolved_args = [
                    arg() if callable(arg) else arg
                    for arg in args
                ]

                resolved_kwargs = {
                    key: value() if callable(value) else value
                    for key, value in kwargs.items()
                }

                bus.emit(
                    endpoint,
                    self.value,
                    *resolved_args,
                    **resolved_kwargs
                )

    def bind(self, endpoint, *args, **kwargs):
        if endpoint not in self.bindings:
            self.bindings[endpoint] = []

        self.bindings[endpoint].append((args, kwargs))

    def unbind(self, endpoint):
        if endpoint in self.bindings:
            del self.bindings[endpoint]