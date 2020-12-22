import collections
import enum
import logging

import yaml


LOG = logging.getLogger(__name__)


class States(enum.Enum):
    BLANK = enum.auto()
    GOOD = enum.auto()
    BAD = enum.auto()
    WEIRD = enum.auto()


class FunctionCheck:
    func = None

    def __init__(self, *pargs, **kwargs):
        self.pargs = pargs
        self.kwargs = kwargs

    def __str__(self):
        # TODO: Format as function call
        return self.func.__name__

    def __repr__(self):
        return f"<{type(self).__name__} pargs={self.pargs!r} kwargs={self.kwargs}>"

    def __call__(self):
        try:
            type(self).func(*self.pargs, **self.kwargs)
        except Exception:
            return States.BAD
        else:
            return States.GOOD

    @classmethod
    def from_yaml(cls, loader, node):
        pargs = ()
        kwargs = {}
        if isinstance(node, yaml.ScalarNode):
            args = loader.construct_scalar(node)
            if args is not None:
                pargs = args,
        elif isinstance(node, yaml.SequenceNode):
            pargs = loader.construct_sequence(node)
        elif isinstance(node, yaml.MappingNode):
            kwargs = loader.construct_mapping(node)
        return cls(*pargs, **kwargs)

    def to_yaml(cls, dumper, data):
        raise NotImplementedError


def check(func):
    """
    Flags a function as a check
    """
    return type(yaml.YAMLObject)(
        func.__name__,
        (FunctionCheck, yaml.YAMLObject),
        {
            '__doc__': func.__doc__,
            'yaml_tag': f"!{func.__name__}",
            'func': func,
            '__module__': func.__module__,
        }
    )


def load(root, stream):
    """
    Loads checks from a config file.

    Config files are yaml, in the form of:

        - Host name:
          - check name: !check args
          - !check args
    """
    # Checks are loaded implicitly when root is created
    raw_data = yaml.load(stream)
    data = collections.OrderedDict()
    for item in raw_data:
        (hostname, rawchecks), = item.items()
        hostchecks = collections.OrderedDict()
        if not rawchecks:
            data[hostname] = {}
            continue
        for check in rawchecks:
            if isinstance(check, dict):
                (checkname, obj), = check.items()
            else:
                obj = check
                checkname = str(check)
            hostchecks[checkname] = obj
        data[hostname] = hostchecks
    return data
