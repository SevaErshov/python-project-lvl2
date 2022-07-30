from gendiff.formatter.stylish import sort_diff


def into_line(sign, property, add=None, update=None):
    signs = {
            '- ': f'Property \'{property}\' was removed',
        }
    if isinstance(add, dict):
        signs['+ '] = f'''Property \'{property}\' was added \
with value: [complex value]'''
        signs['-+'] = f'''Property \'{property}\' was updated. \
From [complex value] to {de_bool(update)}'''
    elif isinstance(update, dict):
        signs['+ '] = f'''Property \'{property}\' was added \
with value: {de_bool(add)}'''
        signs['-+'] = f'''Property \'{property}\' was updated. \
From {de_bool(add)} to [complex value]'''
    else:
        signs['+ '] = f'''Property \'{property}\' was added \
with value: {de_bool(add)}'''
        signs['-+'] = f'''Property \'{property}\' was updated. \
From {de_bool(add)} to {de_bool(update)}'''
    return signs.get(sign)


def de_bool(value):
    if value == 'false' or value == 'true' or value == 'null':
        return value
    return '\'' + str(value) + '\''


def compose_diff(value: dict):
    updated = {}

    def _iter(value):
        to_del = []
        to_add = {}
        for key in value:
            if key[0] == '-' and ('+' + key[1:]) in value:
                updated['-+' + key[2:]] = value['+' + key[1:]]
                to_add['-+' + key[2:]] = value[key]
                to_del.append(key)
                to_del.append('+' + key[1:])
            if key[0] == ' ' and isinstance(value[key], dict):
                _iter(value[key])

        for key in to_del:
            del value[key]
        value.update(to_add)

    _iter(value)
    return updated


def get_symbol(string, index):
    if len(string) - 1 < index:
        return None
    else:
        return string[index]


def delete_dote(value):
    if get_symbol(value, 0) == '.':
        return value[1:]
    return value


def plain(diff: dict):
    updated = compose_diff(diff)
    diff = sort_diff(diff)
    lines = []

    def _iter(value, property):
        for k, v in value.items():
            new_property = delete_dote(property + '.' + str(k[2:]))
            if not isinstance(v, dict) or k[0] != ' ':
                line = into_line(k[:2], new_property, v, updated.get(k))
                lines.append(line)
            else:
                _iter(v, new_property)

    _iter(diff, '')
    lines = list(filter(lambda x: x is not None, lines))
    result = '\n'.join(lines)
    return result
