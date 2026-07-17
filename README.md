# GLU

**GLU (General Language Unification)** is an inter-language communication framework that allows programs written in different languages to communicate through simple path-based addressing.

GLU provides a unified way to connect functions, variables, and events across languages without requiring custom integrations.

---

## Concept

GLU represents program components using endpoints:

```
language@filePath.member
```

Examples:

```
js@app.src.main.displayMessage
py@main.user.username
rust@src.engine.start
```

An endpoint identifies:

- The programming language
- The file path containing the component
- The function or variable being accessed

Example:

```
js@app.src.main.displayMessage
```

represents:

- Language: JavaScript
- File: `app/src/main.js`
- Function: `displayMessage`

### Multiple targets are allowed:

A single source can trigger multiple endpoints.

Example:
```
BIND:

py@main.username -> py@main.updateGreeting, js@app.displayUsername
```
This is equivalent to:
```
BIND:

py@main.username -> py@main.updateGreeting
py@main.username -> js@app.displayUsername
```
---

# Direct Function Calls

Functions can be called directly using `GLU.emit()`.

### Python

```python
import GLU

GLU.emit(
    "js@app.src.main.displayMessage",
    "Hello from Python"
)
```

### JavaScript

```javascript
export function displayMessage(message) {
    console.log(message);
}
```

Output:

```
Hello from Python
```

Direct calls allow one language to explicitly execute functionality from another language.

---

# Reactive Bindings

GLU can automatically connect variables and functions using a `.glu` configuration file.

Instead of manually calling a function, GLU can watch for changes and react automatically.

Example:

`main.glu`

```glu
BIND:

py@main.username -> js@app.updateUsername
```

This creates a connection:

```
main.py username variable
            |
            v
app.js updateUsername()
```

Whenever `username` changes, GLU automatically calls `updateUsername()` with the new value.

---

# Multiple Reactions

A single variable can trigger multiple functions.

Example:

```glu
BIND:

py@main.username -> py@main.updateGreeting
py@main.username -> js@app.displayUsername
```

A change to:

```
py@main.username
```

can update multiple parts of an application.

---

## WATCH

Reactive variable-to-function communication.

Example:

```glu
WATCH:

py@main.score -> js@app.updateScore
```

Used when a change in data should automatically trigger behavior.

---

# Why GLU?

Modern applications often use multiple programming languages:

- Python for backend logic
- JavaScript for interfaces
- Rust/C++ for performance-critical systems
- Other languages for specialized tasks

Connecting these systems often requires custom APIs, wrappers, or duplicated logic.

GLU provides a common communication layer where components can be connected through simple declarations.

---

# Endpoint Format

Endpoints follow this structure:

```
language@filePath.member
```

Examples:

```
py@main.calculate
js@app.src.renderer.update
rust@src.engine.start
```

Each endpoint identifies:

1. The language runtime
2. The file or module path
3. The function or variable being accessed

---

# Current Status

GLU is currently in early development.

## Implemented

- Endpoint parsing
- Language adapters
- Basic function addressing
- Binding file parser

## Planned

- Variable watching system
- Cross-process communication
- Additional language adapters
- Automatic function discovery
- Improved error handling
- Generated language bridges

---

# License

MIT License
