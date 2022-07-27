import json
import itertools
import yaml


def stylish(value: dict, replacer=' ', spaces_count=2):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(current_value)
        if depth == 0:
            deep_indent_size = depth + spaces_count
            current_indent = replacer * depth
        else:
            deep_indent_size = depth + spaces_count + 2
            current_indent = replacer * (depth + 2)
        deep_indent = replacer * deep_indent_size
        lines = []
        for key, val in current_value.items():
            lines.append(f'{deep_indent}{key}: {iter_(val, deep_indent_size)}')
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(value, 0)


def tree_bool(value):
    if value is False:
        return 'false'
    elif value is True:
        return 'true'
    elif value is None:
        return 'null'
    return value


def compare(sign_read: dict, comp_read: dict, sign: str):
    difference = dict()
    for key in sign_read:
        if not isinstance(sign_read[key], dict):
            if key in comp_read and sign_read[key] == comp_read[key]:
                difference['  ' + str(key)] = tree_bool(sign_read[key])
            else:
                difference[sign + ' ' + str(key)] = tree_bool(sign_read[key])
        else:
            if key not in comp_read or not isinstance(comp_read[key], dict):
                compare_value = compare(sign_read[key], sign_read[key], ' ')
                difference[sign + ' ' + str(key)] = compare_value
            elif key in comp_read and isinstance(comp_read[key], dict):
                compare_value = compare(sign_read[key], comp_read[key], sign)
                difference['  ' + str(key)] = compare_value
    return difference


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


def recursive_update(first: dict, second: dict):
    for key in second:
        if key not in first:
            first[key] = second[key]
        elif key in first:
            if isinstance(first[key], dict) and isinstance(second[key], dict):
                recursive_update(first[key], second[key])
                first[key] = sort_dict(first[key])
            else:
                first[key] = second[key]


def sort_dict(dictionary):
    sorted_tuple = sorted(dictionary.items(), key=lambda x: x[0][2:])
    return dict(sorted_tuple)


def generate_diff(first_file, second_file, format=stylish):
    first_read = parse_file(first_file)
    second_read = parse_file(second_file)
    first_diff = compare(first_read, second_read, '-')
    second_diff = compare(second_read, first_read, '+')
    recursive_update(first_diff, second_diff)
    second_diff.clear()
    sorted_tuple = sorted(first_diff.items(), key=lambda x: x[0][2:])
    first_diff.clear()
    difference = dict(sorted_tuple)
    return format(difference)
