import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from GLU.python import GLU

message = "The value of a is: "

a = GLU.GLUProperty(5)
print(f"{a.get()}^2 = {GLU.emit('py@DemoProject.app.pow', a.get(), 2)}")
print(f"a = {a.get()}")
a.bind('py@DemoProject.app.console', lambda: message)

a.set(10)
message = "The value of a has been changed to: "
a.set(4)

# GLU.emit(
#     "js@DemoProject.main.sendMessage",
#     message
# )

