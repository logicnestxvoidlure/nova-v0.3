# Nova v3

Nova is a lightweight general-purpose programming language with its own lexer, parser, interpreter, bytecode compiler layer, virtual-machine support, functions, classes, modules, error handling, file utilities, JSON support, and interactive REPL.

## Table of Contents

1. Installation
2. Running Nova
3. Command Line Commands
4. Command Line Flags
5. REPL
6. Variables
7. Constants
8. Data Types
9. Operators
10. Conditions
11. Loops
12. Functions
13. Lambdas
14. Arrays
15. Maps
16. Classes
17. Inheritance
18. Error Handling
19. Modules
20. File Operations
21. JSON
22. Built-in Functions
23. String Interpolation
24. Math
25. Examples
26. Project Structure
27. Debugging
28. Common Errors

---

# 1. Installation

Nova v3 currently runs through Python.

Requirements:

```text
Python 3.10+
```

Check your Python version:

```bash
python --version
```

On some systems:

```bash
python3 --version
```

No external Python packages are required.

---

# 2. Running Nova

The basic command is:

```bash
python nova.py program.nova
```

Example:

```bash
python nova.py examples/hello.nova
```

Nova reads the `.nova` file, parses it, and executes the program.

---

# 3. Command Line Commands

## Run a program

```bash
python nova.py program.nova
```

Example:

```bash
python nova.py examples/hello.nova
```

---

## Start the REPL

Run Nova without a file:

```bash
python nova.py
```

You will see:

```text
Nova 3.0.0 REPL
Type exit to quit
nova>
```

You can now enter Nova code directly.

Example:

```text
nova> let x = 10
nova> print(x)
10
```

Exit with:

```text
exit
```

---

## Show the Nova version

```bash
python nova.py --version
```

or:

```bash
python nova.py -v
```

Example output:

```text
3.0.0
```

---

## Check a program

Use:

```bash
python nova.py --check program.nova
```

This parses the program without executing it.

Successful output:

```text
OK
```

This is useful for checking syntax before running a large program.

---

## Show tokens

Use:

```bash
python nova.py --tokens program.nova
```

Example:

```bash
python nova.py --tokens examples/hello.nova
```

Nova will display the tokens produced by the lexer.

Example:

```text
KW('let')@1:1
IDENT('name')@1:5
OP('=')@1:10
STRING('Nova')@1:12
```

This is useful when developing the Nova parser or debugging syntax.

---

## Show the AST

Use:

```bash
python nova.py --ast program.nova
```

Example:

```bash
python nova.py --ast examples/hello.nova
```

This displays the Abstract Syntax Tree created by the parser.

The AST represents the structure of the program.

---

## Show a full traceback

Use:

```bash
python nova.py program.nova --trace
```

If an error occurs, Python's traceback is displayed in addition to Nova's error message.

This is mainly useful when developing Nova itself.

---

# 4. Command Summary

| Command | Purpose |
|---|---|
| `python nova.py` | Start REPL |
| `python nova.py file.nova` | Run program |
| `python nova.py --version` | Show version |
| `python nova.py -v` | Show version |
| `python nova.py --check file.nova` | Check syntax |
| `python nova.py --tokens file.nova` | Display lexer tokens |
| `python nova.py --ast file.nova` | Display AST |
| `python nova.py file.nova --trace` | Show detailed traceback |

---

# 5. REPL

The REPL lets you execute Nova interactively.

Start it:

```bash
python nova.py
```

Then:

```text
nova> let x = 25
nova> let y = 15
nova> print(x + y)
40
```

Functions can also be created:

```text
nova> fn square(x) { return x * x }
nova> print(square(8))
64
```

Exit:

```text
nova> exit
```

---

# 6. Variables

Create a variable using `let`:

```nova
let name = "Nova"
let age = 15
let online = true
```

Variables can be changed:

```nova
let score = 10
score = 20
```

Compound assignment is supported:

```nova
score += 5
score -= 2
score *= 2
score /= 2
score %= 3
```

---

# 7. Constants

Use `const` for values that should not be changed:

```nova
const PI = 3.14159
const NAME = "Nova"
```

Attempting to modify a constant produces an error.

```nova
const VERSION = 3
VERSION = 4
```

---

# 8. Data Types

Nova supports:

### Numbers

```nova
let integer = 100
let decimal = 3.14
```

### Strings

```nova
let message = "Hello Nova"
```

### Booleans

```nova
let enabled = true
let disabled = false
```

### Null

```nova
let value = null
```

### Arrays

```nova
let numbers = [1, 2, 3, 4]
```

### Maps

```nova
let user = {
    name: "Nova",
    age: 15
}
```

---

# 9. Operators

## Arithmetic

```text
+
-
*
/
%
**
```

Example:

```nova
let a = 10
let b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a % b)
print(a ** b)
```

---

## Comparison

```text
==
!=
<
<=
>
>=
```

Example:

```nova
print(10 > 5)
print(10 == 10)
print(10 != 20)
```

---

## Logical

```text
&&
||
!
```

Example:

```nova
let age = 20
let has_id = true

if age >= 18 && has_id {
    print("Allowed")
}
```

---

# 10. Conditions

Basic `if`:

```nova
if score >= 50 {
    print("Pass")
}
```

`else`:

```nova
if score >= 50 {
    print("Pass")
} else {
    print("Fail")
}
```

Conditions can contain expressions:

```nova
if x > 10 && x < 100 {
    print("Between 10 and 100")
}
```

---

# 11. Loops

## While

```nova
let x = 0

while x < 5 {
    print(x)
    x += 1
}
```

---

## For

```nova
let numbers = [1, 2, 3, 4, 5]

for number in numbers {
    print(number)
}
```

---

## Range

```nova
for number in range(5) {
    print(number)
}
```

Output:

```text
0
1
2
3
4
```

Range with start and end:

```nova
for number in range(2, 7) {
    print(number)
}
```

---

## Break

Stop a loop:

```nova
for number in range(100) {
    if number == 5 {
        break
    }

    print(number)
}
```

---

## Continue

Skip the current iteration:

```nova
for number in range(10) {
    if number == 5 {
        continue
    }

    print(number)
}
```

---

# 12. Functions

Define a function:

```nova
fn add(a, b) {
    return a + b
}
```

Call it:

```nova
let result = add(10, 20)
print(result)
```

Output:

```text
30
```

Functions can have no parameters:

```nova
fn hello() {
    print("Hello!")
}
```

Call:

```nova
hello()
```

---

# 13. Recursion

Nova functions can call themselves.

Example factorial:

```nova
fn factorial(n) {
    if n <= 1 {
        return 1
    }

    return n * factorial(n - 1)
}

print(factorial(6))
```

Output:

```text
720
```

Fibonacci:

```nova
fn fib(n) {
    if n <= 1 {
        return n
    }

    return fib(n - 1) + fib(n - 2)
}

print(fib(10))
```

---

# 14. Lambdas

Functions can be created anonymously:

```nova
let add = fn(a, b) {
    return a + b
}

print(add(5, 7))
```

Lambdas can capture variables from their surrounding environment:

```nova
fn make_adder(x) {
    return fn(y) {
        return x + y
    }
}

let add10 = make_adder(10)

print(add10(5))
```

Output:

```text
15
```

---

# 15. Arrays

Create an array:

```nova
let numbers = [10, 20, 30]
```

Access an element:

```nova
print(numbers[0])
print(numbers[1])
```

Modify an element:

```nova
numbers[0] = 100
```

Loop through an array:

```nova
for number in numbers {
    print(number)
}
```

Get its size:

```nova
print(len(numbers))
```

---

# 16. Maps

Create a map:

```nova
let player = {
    name: "Nova",
    score: 100,
    level: 5
}
```

Access values:

```nova
print(player["name"])
print(player["score"])
```

Modify values:

```nova
player["score"] = 200
```

Maps can store arrays:

```nova
let data = {
    name: "Nova",
    scores: [10, 20, 30]
}
```

---

# 17. Classes

Define a class:

```nova
class Player {
    fn init(name) {
        this.name = name
    }

    fn greet() {
        print(this.name)
    }
}
```

Create an object:

```nova
let player = new Player("Nova")
```

Call a method:

```nova
player.greet()
```

---

# 18. Constructors

Nova uses the `init` method as the object initializer.

```nova
class User {
    fn init(name, age) {
        this.name = name
        this.age = age
    }
}
```

Create:

```nova
let user = new User("Nova", 15)
```

Properties can then be accessed:

```nova
print(user.name)
print(user.age)
```

---

# 19. Inheritance

Classes can extend other classes:

```nova
class Animal {
    fn init(name) {
        this.name = name
    }

    fn speak() {
        print(this.name)
    }
}

class Dog extends Animal {
    fn bark() {
        print("Woof!")
    }
}
```

Create the child object:

```nova
let dog = new Dog("Buddy")

dog.speak()
dog.bark()
```

---

# 20. Error Handling

Nova supports:

```text
try
catch
finally
throw
```

Example:

```nova
try {
    throw "Something went wrong"
} catch (error) {
    print("Error:", error)
} finally {
    print("Finished")
}
```

`throw` creates an exception:

```nova
throw "Invalid value"
```

The `catch` block receives the thrown value.

---

# 21. Modules

Nova programs can import another `.nova` file.

Example:

```nova
import "stdlib/math.nova" as mathlib
```

If `stdlib/math.nova` contains:

```nova
fn double(x) {
    return x * 2
}
```

You can use:

```nova
print(mathlib["double"](20))
```

Output:

```text
40
```

Modules are useful for separating large programs into multiple files.

---

# 22. File Operations

Nova includes basic file functions.

## Read a file

```nova
let text = read_file("data.txt")
print(text)
```

---

## Write a file

```nova
write_file("data.txt", "Hello from Nova!")
```

This creates or replaces the file.

---

## Append to a file

```nova
append_file("data.txt", "\nAnother line")
```

---

# 23. JSON

Nova supports JSON encoding and decoding.

Convert a Nova value to JSON:

```nova
let data = {
    name: "Nova",
    version: 3
}

let json = json_encode(data)

print(json)
```

Convert JSON back:

```nova
let data = json_decode(json)

print(data["name"])
```

JSON is useful for configuration files, saved data, and communication between programs.

---

# 24. Built-in Functions

## print

```nova
print("Hello")
```

Multiple values:

```nova
print("Score:", 100)
```

---

## input

```nova
let name = input("Name: ")
print(name)
```

---

## len

Get the length of an array or string:

```nova
print(len("Nova"))
```

Output:

```text
4
```

---

## type

Get the runtime type:

```nova
print(type(10))
print(type("hello"))
```

---

## str

Convert a value to a string:

```nova
let value = str(123)
```

---

## num

Convert a value to a number:

```nova
let value = num("123")
```

---

## bool

Convert a value to a boolean:

```nova
let value = bool(1)
```

---

## range

Create a sequence:

```nova
range(5)
```

or:

```nova
range(2, 10)
```

or:

```nova
range(2, 10, 2)
```

---

# 25. Math Functions

Nova provides:

```text
sqrt()
abs()
floor()
ceil()
round()
min()
max()
```

Examples:

```nova
print(sqrt(25))
print(abs(-10))
print(floor(3.9))
print(ceil(3.1))
print(round(3.5))
print(min(5, 2))
print(max(5, 2))
```

---

# 26. String Interpolation

Nova supports `${...}` inside strings.

Example:

```nova
let name = "Nova"
let version = 3

print("Language: ${name}")
print("Version: ${version}")
```

Expressions can also be used:

```nova
let x = 10
let y = 20

print("Result: ${x + y}")
```

Output:

```text
Result: 30
```

---

# 27. Complete Example

```nova
class Player {
    fn init(name, score) {
        this.name = name
        this.score = score
    }

    fn show() {
        print("${this.name}: ${this.score}")
    }
}

fn factorial(n) {
    if n <= 1 {
        return 1
    }

    return n * factorial(n - 1)
}

let player = new Player("Nova", 100)

player.show()

for number in range(1, 6) {
    print("Factorial ${number} =", factorial(number))
}

try {
    throw "Demo error"
} catch (error) {
    print("Caught:", error)
}
```

---

# 28. Project Structure

A recommended Nova project can look like:

```text
MyProject/
├── nova.py
├── nova.toml
├── main.nova
├── examples/
├── stdlib/
└── tests/
```

A simple project configuration:

```toml
name = "MyProject"
version = "1.0.0"
entry = "main.nova"
```

Run the entry file:

```bash
python nova.py main.nova
```

---

# 29. Debugging

If your program doesn't work, first run:

```bash
python nova.py --check program.nova
```

Then inspect the tokens:

```bash
python nova.py --tokens program.nova
```

Then inspect the AST:

```bash
python nova.py --ast program.nova
```

For runtime problems:

```bash
python nova.py program.nova --trace
```

---

# 30. Common Errors

## Undefined variable

```text
NovaError: Undefined variable: x
```

This means Nova cannot find the variable.

Example:

```nova
print(x)
```

Fix:

```nova
let x = 10
print(x)
```

---

## Cannot modify constant

```text
NovaError: Cannot modify constant: VERSION
```

Example:

```nova
const VERSION = 3
VERSION = 4
```

Constants cannot be reassigned.

---

## Value is not callable

```text
NovaError: Value is not callable
```

This usually means something that isn't a function was called:

```nova
let x = 10
x()
```

---

## Unexpected token

```text
NovaError: Unexpected token ...
```

This normally means the parser encountered invalid Nova syntax.

Run:

```bash
python nova.py --check program.nova
```

---

## Unclosed block

Example:

```nova
if true {
    print("Hello")
```

The closing `}` is missing.

Correct:

```nova
if true {
    print("Hello")
}
```

---

# 31. Recommended Workflow

For a new Nova program:

### Step 1

Create:

```text
main.nova
```

### Step 2

Write your program:

```nova
print("Hello Nova!")
```

### Step 3

Check it:

```bash
python nova.py --check main.nova
```

### Step 4

Run it:

```bash
python nova.py main.nova
```

### Step 5

If something breaks, inspect the AST:

```bash
python nova.py --ast main.nova
```

or tokens:

```bash
python nova.py --tokens main.nova
```

---

# 32. Nova v3 Command Cheat Sheet

```text
RUN
python nova.py file.nova

REPL
python nova.py

VERSION
python nova.py --version
python nova.py -v

CHECK
python nova.py --check file.nova

TOKENS
python nova.py --tokens file.nova

AST
python nova.py --ast file.nova

TRACE
python nova.py file.nova --trace
```

---

# 33. Nova v3 Feature Overview

```text
Variables             ✓
Constants             ✓
Numbers               ✓
Strings               ✓
Booleans              ✓
Null                  ✓
Arrays                ✓
Maps                  ✓
Arithmetic             ✓
Comparisons            ✓
Logical operators      ✓
Compound assignment    ✓
If / Else              ✓
While                  ✓
For / In               ✓
Break                  ✓
Continue               ✓
Functions              ✓
Recursion              ✓
Closures               ✓
Lambdas                ✓
Classes                ✓
Objects                ✓
Constructors           ✓
Inheritance            ✓
Exceptions             ✓
Try / Catch / Finally   ✓
Throw                  ✓
Modules                ✓
File I/O               ✓
JSON                   ✓
String interpolation   ✓
Math functions         ✓
REPL                   ✓
Lexer inspection       ✓
AST inspection         ✓
Syntax checking        ✓
Bytecode compiler layer ✓
Virtual machine layer  ✓
```

Nova v3 is intended to be a compact, extensible programming language that can grow into a larger ecosystem while remaining easy to learn.
v2 : https://github.com/logicnestxvoidlure/nova-v2
