# GLU

**GLU (General Language Unification)** is an inter-language communication framework built around simple endpoint-based addressing.

GLU allows different parts of an application to communicate through a unified system for calling functions, reacting to changes, and connecting components without writing custom integration layers.

---

# Core Concept

GLU represents application components using **endpoints**.

Endpoints follow this format:

```
language@modulePath.member
```

Example:

```
py@app.main.displayMessage
```

An endpoint contains:

| Part | Description |
|---|---|
| `py` | The language runtime |
| `app.main` | The module path |
| `displayMessage` | The function, variable, or property |

GLU uses these endpoints to locate and communicate with application components.

---

# Python Endpoint Paths

Python endpoints use module paths relative to your **project root**.

The endpoint path must match the way Python imports the module.

Example project:

```
Project/
│
├── app.py
├── main.py
│
└── utils/
    └── math.py
```

If `app.py` contains:

```python
def console(message):
    print(message)
```

The endpoint is:

```
py@Project.app.console
```

If `utils/math.py` contains:

```python
def add(a, b):
    return a + b
```

The endpoint is:

```
py@Project.utils.math.add
```

The project folder name is **always included**.

Correct:

```
py@Project.app.console
```

Incorrect:

```
py@app.console
```

GLU resolves Python endpoints using Python's import system.

---

# Argument Forwarding

`GLU.emit()` accepts positional and keyword arguments and forwards them directly to the target function.

The function signature is:

```python
GLU.emit(endpoint, *args, **kwargs)
```

Where:

- `*args` contains positional arguments.
- `**kwargs` contains keyword arguments.

GLU does not modify, reorder, or convert these arguments. They are passed directly into the target function.

---

# Positional Arguments (`*args`)

Positional arguments are passed in the same order they are provided.

Example:

```python
GLU.emit(
    "py@Project.math.add",
    5,
    10
)
```

Target:

```python
def add(a, b):
    return a + b
```

GLU performs the equivalent of:

```python
add(
    5,
    10
)
```

The order is preserved:

```
First argument  -> a
Second argument -> b
```

---

# Keyword Arguments (`**kwargs`)

Keyword arguments are passed using their parameter names.

Example:

```python
GLU.emit(
    "py@Project.user.create",
    "Benjamin",
    age=25
)
```

Target:

```python
def create(name, age):
    ...
```

GLU performs the equivalent of:

```python
create(
    "Benjamin",
    age=25
)
```

Keyword names are preserved.

---

# Combining Positional and Keyword Arguments

Both argument types can be used together.

Example:

```python
GLU.emit(
    "py@Project.player.create",
    "Dragon",
    100,
    health=500,
    level=10
)
```

Target:

```python
def create(name, position, health, level):
    ...
```

Equivalent Python call:

```python
create(
    "Dragon",
    100,
    health=500,
    level=10
)
```

---

# Internal Argument Flow

When `emit()` is called, GLU follows this process:

```
GLU.emit(
    endpoint,
    *args,
    **kwargs
)
        |
        v
Resolve endpoint
        |
        v
Find target function
        |
        v
Call function(*args, **kwargs)
        |
        v
Return result
```

The target function is executed exactly like a normal Python function call.

---

# Return Values

`GLU.emit()` returns the value returned by the target function.

Example:

```python
result = GLU.emit(
    "py@Project.math.add",
    5,
    10
)

print(result)
```

Target:

```python
def add(a, b):
    return a + b
```

Output:

```
15
```

Internally:

```python
return function(*args, **kwargs)
```

The returned value is passed directly back to the caller.

---

# Local and External Resolution

GLU first checks whether the target function exists in the caller's current file.

This allows functions in the same file to be called without importing the module again.

Example:

```python
def hello():
    print("Hello")

GLU.emit(
    "py@Project.main.hello"
)
```

If the target is not found in the current file, GLU imports the target module using Python's import system.

Example:

```
py@Project.utils.math.add
```

resolves to:

```python
from Project.utils.math import add
```

Then the function is executed.

---

# Endpoint Resolution Errors

If GLU cannot find the target, it raises an error.

Possible errors include:

```
Module not found
Function not found
Invalid endpoint
```

The endpoint must correctly match the Python module path and object name.

---

# Reactive Properties

GLU provides `GLUProperty` for values that need automatic change notifications.

A `GLUProperty` stores a value and allows other endpoints to react whenever its value changes.

Unlike normal variables, `GLUProperty` objects can notify GLU when their data changes. This allows components to communicate without directly calling each other.

Example:

```python
from GLU import GLUProperty

score = GLUProperty(0)

score.bind(
    "py@Project.display.updateScore"
)

score.set(100)
```

When the value changes, GLU automatically calls:

```python
updateScore(100)
```

The changed value is always passed as the **first argument**.

The first parameter of any function receiving a property update should represent the new value.

---

# Variable Bindings

Only `GLUProperty` objects can create automatic variable bindings.

Normal variables cannot be observed by GLU because the language runtime does not know when their values change.

This will not work:

```python
score = 0

score.bind(
    "py@Project.display.updateScore"
)
```

`score` is only a normal Python integer. Changing it does not create an event that GLU can detect.

Instead, create a `GLUProperty`:

```python
from GLU import GLUProperty

score = GLUProperty(0)

score.bind(
    "py@Project.display.updateScore"
)
```

Now changes can be detected:

```python
score.set(100)
```

Any value that needs to trigger GLU bindings must be stored inside a `GLUProperty`.

---

# Property Data Types

`GLUProperty` can store any supported data value.

In Python, the data type is automatically determined from the initial value.

Example:

```python
number = GLUProperty(10)
text = GLUProperty("Hello")
enabled = GLUProperty(True)
items = GLUProperty([1, 2, 3])
```

Python automatically provides the type information:

```
10          -> int
"Hello"     -> string
True        -> bool
[1, 2, 3]   -> list
```

No additional type declaration is required.

Other language runtimes may require additional type information because some languages handle values differently or do not provide the same runtime type information.

Future GLU language adapters may support explicit type tags for cross-language communication.

Example of a possible future format:

```
(int)
(String)
(bool)
(float)
```

These tags are not currently required or implemented in GLU's Python runtime.

---

# Reading and Updating Properties

The current value of a property can be retrieved using `get()`.

Example:

```python
currentScore = score.get()
```

Properties should be updated using `set()`.

Example:

```python
score.set(200)
```

Using `set()` allows GLU to notify all connected endpoints.

Directly changing internal values bypasses the notification system.

Incorrect:

```python
score.value = 200
```

Correct:

```python
score.set(200)
```

---

# Property Bindings

Bindings connect a `GLUProperty` to one or more endpoints.

Whenever the property changes, GLU automatically calls every connected endpoint.

Example:

```python
score.bind(
    "py@Project.display.updateScore"
)
```

When:

```python
score.set(50)
```

GLU calls:

```python
updateScore(50)
```

The binding format is:

```
function(changed_value)
```

The changed value is automatically provided by GLU.

---

# Binding Additional Arguments

Bindings can include additional arguments.

Example:

```python
score.bind(
    "py@Project.display.console",
    "Player Score"
)
```

When:

```python
score.set(50)
```

GLU calls:

```python
console(50, "Player Score")
```

The binding format is:

```
function(changed_value, additional_arguments...)
```

The changed value is always inserted as the first argument.

---

# Dynamic Binding Arguments

Binding arguments can be dynamically evaluated using `lambda` functions.

Normal binding arguments are stored when the binding is created.

Example:

```python
message = "The value is:"

score.bind(
    "py@Project.display.console",
    message
)
```

The binding stores the current value:

```
"The value is:"
```

Changing the variable later does not update the binding.

Example:

```python
message = "The value is:"

score.bind(
    "py@Project.display.console",
    message
)

message = "The value changed:"
```

The binding will still use:

```
"The value is:"
```

---

To retrieve the latest value when the binding executes, use a `lambda` function:

```python
message = "The value is:"

score.bind(
    "py@Project.display.console",
    lambda: message
)

score.set(100)

message = "The value changed:"

score.set(200)
```

The lambda is evaluated when the property changes.

The first update sends:

```python
console(
    100,
    "The value is:"
)
```

The second update sends:

```python
console(
    200,
    "The value changed:"
)
```

---

Dynamic arguments are useful when a binding depends on values that may change over time.

Example:

```python
username = "Player"

score.bind(
    "py@Project.display.update",
    lambda: username
)
```

When `score` changes, GLU evaluates:

```python
lambda: username
```

and sends the current value.

---

Dynamic arguments can also be used with keyword arguments:

```python
score.bind(
    "py@Project.display.update",
    label=lambda: username
)
```

Before calling the endpoint, GLU evaluates the lambda and passes the result:

```python
update(
    score_value,
    label="Player"
)
```

Dynamic arguments are evaluated only when the property changes. They do not continuously track the referenced variable.

---

# Multiple Bindings

A single `GLUProperty` can trigger multiple endpoints.

Example:

```python
score.bind(
    "py@Project.display.updateScore"
)

score.bind(
    "py@Project.game.checkAchievements"
)
```

When:

```python
score.set(100)
```

GLU calls:

```python
updateScore(100)
checkAchievements(100)
```

Each binding operates independently.

---

# Unbinding

Bindings can be removed when they are no longer needed.

Example:

```python
score.unbind(
    "py@Project.display.updateScore"
)
```

After unbinding, the endpoint will no longer receive property updates.

Other bindings remain active.

Example:

```python
score.bind(
    "py@Project.display.updateScore"
)

score.bind(
    "py@Project.game.checkAchievements"
)

score.unbind(
    "py@Project.display.updateScore"
)
```

After unbinding:

```
py@Project.display.updateScore
```

will no longer receive updates, but:

```
py@Project.game.checkAchievements
```

will continue receiving updates.

---

# Why GLU?

Modern applications often combine multiple technologies:

- Python for application logic
- JavaScript for interfaces
- Rust/C++ for performance-critical systems
- Other languages for specialized tasks

Connecting these systems often requires custom APIs, wrappers, and duplicated communication code.

GLU provides a unified communication layer where components can be connected through simple endpoint references.

---

# Endpoint Format

All endpoints follow:

```
language@modulePath.member
```

Examples:

```
py@app.main.calculate
py@utils.math.add
py@Project.renderer.display
```

An endpoint identifies:

1. The language runtime
2. The module path
3. The component being accessed

---

# Current Status

GLU is currently in early development.

## Implemented

- Endpoint parsing
- Python endpoint resolution
- Function calls through endpoints
- Return values
- Positional and keyword argument forwarding
- Reactive properties
- Property bindings
- Multiple bindings

## Planned

- Additional language runtimes
- Cross-process communication
- Automatic component discovery
- Improved error handling
- Generated language bridges

---

# License

Apache 2.0