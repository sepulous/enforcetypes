from inspect import signature

class TypeMismatchError(Exception):
    def __init__(self, message):
        super().__init__(message)

class MissingTypeError(Exception):
    def __init__(self, message):
        super().__init__(message)

def enforce_types(func):
    def enforce(*func_args):
        func_name = func.__qualname__
        annotations = func.__annotations__
        arity = len(signature(func).parameters)

        # Ensure return type and parameters are annotated
        if len(annotations) != arity + 1:
            raise MissingTypeError(f"One or more types have not been specified for '{func_name}'.")

        # Check argument types
        for (arg, param_name) in zip(func_args, annotations):
            param_type = annotations[param_name]
            if param_type != any:
                if param_type == callable:
                    if not callable(arg):
                        raise TypeMismatchError(f"Parameter '{param_name}' of '{func_name}' expected <callable> but got {type(arg)}.")
                elif not isinstance(arg, param_type):
                    raise TypeMismatchError(f"Parameter '{param_name}' of '{func_name}' expected {param_type} but got {type(arg)}.")

        # Check default arguments
        if func.__defaults__: # (i.e. is not a lambda expression)
            first_default_index = arity - len(func.__defaults__)
            for (default_arg, param_name) in zip(func_args[first_default_index:], annotations[first_default_index:]):
                param_type = annotations[param_name]
                if param_type != any:
                    if param_type == callable:
                        if not callable(default_arg):
                            raise TypeMismatchError(f"Default argument '{param_name}' of '{func_name}' expected <callable> but got {type(default_arg)}.")
                    elif not isinstance(default_arg, param_type):
                        raise TypeMismatchError(f"Default argument '{param_name}' of '{func_name}' expected {param_type} but got {type(default_arg)}.")

        # Check return type
        return_type = list(annotations.values())[-1]
        returned = func(*func_args)
        if return_type != any:
            if return_type is None and returned is not None:
                raise TypeMismatchError(f"'{func_name}' expected to return {return_type} but instead returned {type(returned)}.")
            elif return_type == callable:
                if not callable(returned):
                    raise TypeMismatchError(f"'{func_name}' expected to return <callable> but instead returned {type(returned)}.")
            elif not isinstance(returned, return_type):
                raise TypeMismatchError(f"'{func_name}' expected to return {return_type} but instead returned {type(returned)}.")

        return returned

    return enforce
