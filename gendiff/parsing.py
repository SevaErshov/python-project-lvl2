import json
import yaml
from gendiff.formatter.stylish import stylish
from gendiff.formatter.plain import plain
from gendiff.formatter.json import json as json_format


def tree_bool(value):
    if value is False:
        return 'false'
    elif value is True:
        return 'true'
    elif value is None:
        return 'null'
    return value


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
        if isinstance(first.get(key), dict) and isinstance(second[key], dict):
            recursive_update(first[key], second[key])
        else:
            first[key] = second[key]


def compare_two_keys(key, sign_read: dict, comp_read: dict, sign: str):
    difference = dict()
    if key in comp_read and sign_read[key] == comp_read[key]:
        difference['  ' + str(key)] = tree_bool(sign_read[key])
    else:
        difference[sign + ' ' + str(key)] = tree_bool(sign_read[key])
    return difference


def compare_two_dict(key, sign_read: dict, comp_read: dict, sign: str):
    difference = dict()
    if key not in comp_read or not isinstance(comp_read[key], dict):
        compare_value = compare(sign_read[key], sign_read[key], ' ')
        difference[sign + ' ' + str(key)] = compare_value
    elif isinstance(comp_read.get(key), dict):
        compare_value = compare(sign_read[key], comp_read[key], sign)
        difference['  ' + str(key)] = compare_value
    return difference


def compare(sign_read: dict, comp_read: dict, sign: str):
    diff = dict()

    for key in sign_read:
        if not isinstance(sign_read[key], dict):
            diff.update(compare_two_keys(key, sign_read, comp_read, sign))
        else:
            diff.update(compare_two_dict(key, sign_read, comp_read, sign))
    return diff


def generate_diff(first_file, second_file, format='stylish'):
    first_read = parse_file(first_file)
    second_read = parse_file(second_file)
    first_diff = compare(first_read, second_read, '-')
    second_diff = compare(second_read, first_read, '+')
    recursive_update(first_diff, second_diff)
    if format == 'plain':
        return plain(first_diff)
    elif format == 'stylish':
        return stylish(first_diff)
    elif format == 'json':
        return json_format(first_diff)
    return format(first_diff)
