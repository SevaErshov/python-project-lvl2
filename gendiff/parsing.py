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


def compare(sign_read: dict, compare_read: dict, sign: str):
    view_difference = dict()
    for key in sign_read:
        if not isinstance(sign_read[key], dict):
            if key in compare_read and sign_read[key] == compare_read[key]:
                view_difference['  ' + str(key)] = tree_bool(sign_read[key])
            else:
                view_difference[sign + ' ' + str(key)] = tree_bool(sign_read[key])
        else:
            if key not in compare_read or not isinstance(compare_read[key], dict): 
                compare_sign_value = compare(sign_read[key], sign_read[key], ' ')
                view_difference[sign + ' ' + str(key)] = compare_sign_value
            elif key in compare_read and isinstance(compare_read[key], dict):
                compare_sign_value = compare(sign_read[key], compare_read[key], sign)
                view_difference['  ' + str(key)] = compare_sign_value
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


def recursive_update(first_dict, second_dict):
    for key in second_dict:
        if key not in first_dict:
            first_dict[key] = second_dict[key]
        elif key in first_dict:
            if isinstance(first_dict[key], dict) and isinstance(second_dict[key], dict):
                recursive_update(first_dict[key], second_dict[key])
                first_dict[key] = sort_dict(first_dict[key])
            else:
                first_dict[key] = second_dict[key]


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

