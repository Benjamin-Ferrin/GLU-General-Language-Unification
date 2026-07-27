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
    
def fromGLU(value):

    if not isinstance(value, dict):
        raise Exception("Invalid GLU value")

    value_type = value.get("type")
    data = value.get("data")
    if value_type == "bool": return bool(data)
    if value_type == "int": return int(data)
    if value_type == "float": return float(data)
    if value_type == "string": return str(data)
    if value_type == "null": return None
    if value_type == "list":
        return [
            fromGLU(x)
            for x in data
        ]

    if value_type == "map":
        return {
            k: fromGLU(v)
            for k, v in data.items()
        }

    if value_type == "property":
        return GLUProperty(
            fromGLU(data)
        )

    raise Exception(
        f"Unsupported GLU type: {value_type}"
    )