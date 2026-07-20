from .property import GLUProperty

def toGLU(value):

    if isinstance(value, bool):
        return {
            "type": "bool",
            "data": value
        }

    if isinstance(value, int):
        return {
            "type": "int",
            "data": value
        }

    if isinstance(value, float):
        return {
            "type": "float",
            "data": value
        }

    if isinstance(value, str):
        return {
            "type": "string",
            "data": value
        }

    if value is None:
        return {
            "type": "null",
            "data": None
        }

    if isinstance(value, list):
        return {
            "type": "list",
            "data": [
                toGLU(x)
                for x in value
            ]
        }

    if isinstance(value, dict):
        return {
            "type": "map",
            "data": {
                k: toGLU(v)
                for k, v in value.items()
            }
        }
        
    if isinstance(value, GLUProperty):
        return {
            "type": "property",
            "data": toGLU(value.get())
        }
        
    raise Exception(
        f"Unsupported type: {type(value)}. If you want to use use a custom type, you can implement it here: https://github.com/Benjamin-Ferrin/GLU-General-Language-Unification"
    )