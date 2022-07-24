import json
import gendiff as g


def test_generate_diff():
    first_file = 'tests/fixtures/file1.json'
    second_file = 'tests/fixtures/file2.json'
    with open('tests/fixtures/expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()