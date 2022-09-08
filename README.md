# enforcetypes
enforcetypes is a simple Python decorator for enforcing type hinting. It currently supports the basic data types of Python, as well as callables and objects of arbitrary type. It does not currently support all types available in the `typing` library, nested types such as `list[list[int]]`, or general types such as `Number` or `Collection`.

# Usage
To enforce type hints on a function, simply apply the decorator. The decorator requires that all parameters be type hinted, as well as the return type. Below is an example for a function that applies a callback to an integer and returns a result of any type:
```
@enforce_types
def apply_callback(f: callable, x: int) -> any:
    return f(x)

test(lambda x: x + 1, 5)   # Valid
test(12, 0)                # Throws exception; first argument must be callable
test(lambda x: x + 1, 5.0) # Throws exception; second argument must be int
```
Here's another example where the function is improperly defined:
```
@enforce_types
def add(x: float, y: float) -> int:
    return x + y

add(5.0, 12.0) # Throws exception; function promises to return an int but instead returns a float
```