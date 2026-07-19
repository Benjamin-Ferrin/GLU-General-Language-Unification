import os
import inspect
import importlib
from .parser import Endpoint
# from .helpers import bcolors

class EventBus:
    def __init__(self):
        self.listeners = {}

    def emit(self,endpoint, *args):
        if isinstance(endpoint, str):
            endpoint = Endpoint(endpoint)

        target_module = endpoint.getFilePath()
        function_name = endpoint.getObject()

        # Check caller first
        frame = inspect.currentframe().f_back.f_back        
        caller_globals = frame.f_globals
        caller_file = caller_globals.get("__file__")

        if caller_file:
            caller_file = os.path.abspath(caller_globals["__file__"])
            target_file = os.path.abspath(endpoint.pathToFile())

            # print(f"Caller file: {os.path.normcase(caller_file)}")
            # print(f"Target file: {os.path.normcase(target_file)}")
    
            if os.path.normcase(caller_file) == os.path.normcase(target_file):                
                function = caller_globals.get(function_name)

                if function is None:
                    raise Exception(
                        f"Function '{function_name}' not found in current file"
                    )

                return function(*args)            
               
        # Import external modules
        try:
            module = importlib.import_module(target_module)
        except ModuleNotFoundError:
            raise Exception(
                f"Module '{target_module}' not found"
            )

        function = getattr(module, function_name, None)

        if function is None:
            raise Exception(
                f"Function '{function_name}' "
                f"not found in '{target_module}'"
            )

        return function(*args)
    
    
bus = EventBus()