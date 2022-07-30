from gendiff.formatter.stylish import sort_diff
from json import dumps


def into_bool(value):
    for k, v in value.items():
        if v == 'true':
            value[k] = True
        elif v == 'false':
            value[k] = False
        elif v == 'null':
            value[k] = None
        elif isinstance(v, dict):
            into_bool(v)


def json(diff: dict):
    into_bool(diff)
    diff = sort_diff(diff)
    return dumps(diff, indent=4)
