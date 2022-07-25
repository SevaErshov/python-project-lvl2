import json
import itertools
import yaml


def stringify(value: dict, replacer=' ', spaces_count=1):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(current_value)

        deep_indent_size = depth + spaces_count
        deep_indent = replacer * deep_indent_size
        current_indent = replacer * depth
        lines = []
        for key, val in current_value.items():
            lines.append(f'{deep_indent}{key}: {iter_(val, deep_indent_size)}')
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(value, 0)


def json_bool(value):
    if value is False:
        return 'false'
    elif value is True:
        return 'true'
    elif value is None:
        return 'null'
    return value


def compare(sign_read: dict, compare_read: dict, sign: str):
    view_difference = dict()
    for key in sign_read:
        if key in compare_read and sign_read[key] == compare_read[key]:
            view_difference['  ' + str(key)] = json_bool(sign_read[key])
        else:
            view_difference[sign + ' ' + str(key)] = json_bool(sign_read[key])
    return view_difference


def is_json(file):
    if file[-5:] == '.json':
        return True
    return False


def parse_file(file):
    if is_json(file):
        return json.load(open(file))
    else:
        parse_file = yaml.safe_load(open(file)) 
        return parse_file if parse_file is not None else {}

def generate_diff(first_file, second_file):
    first_read = parse_file(first_file)
    second_read = parse_file(second_file)
    first_diff = compare(first_read, second_read, '-')
    second_diff = compare(second_read, first_read, '+')
    first_diff.update(second_diff)
    second_diff.clear()
    sorted_tuple = sorted(first_diff.items(), key=lambda x: x[0][2:])
    first_diff.clear()
    difference = dict(sorted_tuple)
    return stringify(difference)
