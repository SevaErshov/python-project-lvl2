import json
import gendiff as g


def test_stringify():
    test_json = json.load(open('gendiff/tests/fixtures/file1.json'))
    assert g.stringify(test_json) == '{\n host: hexlet.io\n timeout: 50\n proxy: 123.234.53.22\n follow: False\n}'