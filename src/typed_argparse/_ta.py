import argparse
from typing import Any, overload, Optional, get_type_hints, Sequence, Union


class TypedArgumentParser:

    @overload
    def __init__(self,
                 *,
                 prog: Optional[str] = None,
                 description: Optional[str] = None,
                 epilog: Optional[str] = None,
                 **kwargs) -> None:
        ...

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def parse_args(self, out: Any, args: Optional[Sequence[str]] = None):
        parser = argparse.ArgumentParser(**self._kwargs)

        hints = {}
        for i in out.__class__.__mro__:
            hints.update(get_type_hints(i))

        for name, hint in hints.items():
            value = getattr(out, name, None)
            if not isinstance(value, Argument):
                continue

            arg_name = self._var_name_to_arg_name(name)
            kwargs = value._kwargs
            if kwargs.get('action') not in ['store_true', 'store_false']:
                kwargs['type'] = hint
            if value._positional:
                parser.add_argument(arg_name, **kwargs)
                continue
            if len(arg_name) == 1:
                parser.add_argument(f'-{arg_name}', **kwargs)
                continue
            if value._short_name:
                short_name = value._short_name if isinstance(
                    value._short_name, str) else arg_name[0]
                parser.add_argument(f'-{short_name}', f'--{arg_name}',
                                    **kwargs)
                continue
            parser.add_argument(f'--{arg_name}', **kwargs)

        args1 = parser.parse_args(args)

        for name in hints:
            if hasattr(args1, name):
                setattr(out, name, getattr(args1, name))

    def _var_name_to_arg_name(self, var_name: str) -> str:
        return var_name.replace("_", "-")


class Argument:

    @overload
    def __init__(self,
                 *,
                 positional: bool = False,
                 short_name: Union[bool, str] = False,
                 required: bool = False,
                 default: Any = None,
                 help: Optional[str] = None,
                 **kwargs) -> None:
        ...

    def __init__(self,
                 *,
                 positional: bool = False,
                 short_name: Union[bool, str] = False,
                 **kwargs):
        self._positional = positional
        self._short_name = short_name
        self._kwargs = kwargs
