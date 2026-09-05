# Nova v3

Nova is a small general-purpose programming language implemented in Python.

## Requirements

Python 3.10 or newer.

## Run a program

```bash
python nova.py examples/hello.nova
```

## REPL

```bash
python nova.py
```

## CLI

```bash
python nova.py file.nova
python nova.py --check file.nova
python nova.py --tokens file.nova
python nova.py --ast file.nova
python nova.py --version
```

## Nova syntax

```nova
let name = "Nova"
let nums = [1, 2, 3, 4]

fn add(a, b) {
    return a + b
}

for x in nums {
    print(x)
}

if len(nums) > 2 {
    print(add(10, 20))
}
```

## Features

- Variables and constants
- Numbers, strings, booleans and null
- Arrays and maps
- Arithmetic and comparison operators
- Logical operators
- Functions, recursion and closures
- Lambdas
- Classes, objects and inheritance
- Methods and constructors
- if, else, while and for
- break and continue
- try, catch, finally and throw
- File I/O
- JSON encode/decode
- String utilities
- Math utilities
- Ranges
- Modules
- Built-in testing helpers
- Interactive REPL
- Token and AST inspection
- Syntax checking
- Bytecode-style instruction compiler and virtual machine

## Operators

```text
+ - * / % **
== != < <= > >=
&& || !
= += -= *= /= %= 
.. 
```

## Built-ins

```text
print()
input()
len()
type()
str()
num()
bool()
range()
read_file()
write_file()
append_file()
json_encode()
json_decode()
sqrt()
abs()
floor()
ceil()
round()
min()
max()
```

## Examples

See the `examples` directory.

Nova v3 is designed as an educational and extensible language runtime
old v2 : https://github.com/logicnestxvoidlure/nova-v2
