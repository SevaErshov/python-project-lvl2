#!usr/bit/env python3
import argparse
import json
import itertools


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


def generate_diff(first_file, second_file):
    first_read = json.load(open(first_file))
    second_read = json.load(open(second_file))
    first_diff = compare(first_read, second_read, '-')
    second_diff = compare(second_read, first_read, '+')
    first_diff.update(second_diff)
    second_diff.clear()
    sorted_tuple = sorted(first_diff.items(), key=lambda x: x[0][2:])
    first_diff.clear()
    difference = dict(sorted_tuple)
    return stringify(difference)


def main():
    description = 'Compares two configuration files and shows a difference.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('--format', '-f', help='set format of output')
    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file)
    print(diff)


if __name__ == '__main':
    main()
