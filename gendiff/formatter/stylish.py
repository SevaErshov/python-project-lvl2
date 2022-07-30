import itertools


def sort_diff(dictionary):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            dictionary[key] = sort_diff(dictionary[key])

    sorted_tuple = sorted(dictionary.items(), key=lambda x: x[0][2:])
    return dict(sorted_tuple)


def stylish(value: dict, replacer=' ', spaces_count=2):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(current_value)
        deep_indent_size = depth + spaces_count
        current_indent = replacer * depth
        deep_indent = replacer * deep_indent_size
        lines = []
        for key, val in current_value.items():
            line = f'{deep_indent}{key}: {iter_(val, deep_indent_size + 2)}'
            lines.append(line)
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(sort_diff(value), 0)
