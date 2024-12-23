# typed-argparse

Type-hint your argument parsers in the eaiser way!

## Description

`typed_argparse` is a simple wrapper around the Python standard library's `argparse` module that allows you to define command-line arguments using type hints. It is similar to the famous [tap](https://github.com/swansonk14/typed-argument-parser) library, but `typed_argparse` is more lightweight and has the (possibly) simplest API.

## Installation

Install using `pip`:

```bash
pip install git+https://github.com/shi0rik0/typed-argparse.git
```

Or just copy the source code to your project.

## Tutorial

### Quick Start

There are only two classes in `typed_argparse`, namely `TypedArgumentParser` and `Argument`. Let's import them first:

```python
from typed_argparse import TypedArgumentParser, Argument
```

You initialize a `TypedArgumentParser` in the same way as you initialize an `argparse.ArgumentParser`. They accept the same arguments!

```python
parser = TypedArgumentParser(description='A simple example')
```

Instead of using the `add_argument()` method, you define arguments by creating a class with class variables with type hints and `Argument` values. Each class variable will be translated to an `add_argument()` call. For example:

```python
class MyArgs:
    name: str = Argument(help='Your name', required=True)
    age: int = Argument(short_name=True, help='Your age', required=True)
    height: float = Argument(positional=True, help='Your height')
    is_student: bool = Argument(help='Are you a student?', action='store_true')
```

This will be translated to the following `add_argument()` calls:

```python
parser.add_argument('--name', type=str, help='Your name', required=True)
parser.add_argument('-a', '--age', type=int, help='Your age', required=True)
parser.add_argument('height', type=float, help='Your height')
parser.add_argument('--is-student', action='store_true', help='Are you a student?')
```

Then you use `parse_args()` method to parse the arguments:

```python
args = MyArgs()
parser.parse_args(args)
print(args.name)
```

### More on Arguments

In most cases, the arguments that `Argument`'s constructor accepts will be forwarded to `add_argument()`, that is:

```python
foo: int = Argument(**kwargs)
# is equivalent to
parser.add_argument('--foo', type=int, **kwargs)
```

The exception is that `Argument` accept two additional arguments: `positional` and `short_name`. If `positional` is `True`, the argument will be added as a positional argument. If `short_name` is `True` or a `str`, the argument will be added with a short name (single dash). For example:

```python
foo: int = Argument(short_name=True) # parser.add_argument('-f', '--foo', type=int)
bar: int = Argument(short_name='r') # parser.add_argument('-r', '--bar', type=int)
baz: int = Argument(positional=True) # parser.add_argument('baz', type=int)
```

If the parameter name contains underscores, they will be replaced with dashes.

If the parameter name is a single character, it will be treated as a short name. For example:

```python
a: int = Argument() # parser.add_argument('-a', type=int)
```
