import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from GLU.adapters.python import GLU

message = "Hello, World!"

GLU.emit(
    "py@APP.app.console",
    message
)