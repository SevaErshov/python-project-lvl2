import json
import gendiff as g


def test_plain_json():
    first_file = 'tests/fixtures/file1.json'
    second_file = 'tests/fixtures/file2.json'
    with open('tests/fixtures/expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()
    

def test_empty_json():
    first_file = 'tests/fixtures/file1.json'
    second_file = 'tests/fixtures/empty.json'
    with open('tests/fixtures/expected_with_empty.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()


def test_null_json():
    first_file = 'tests/fixtures/file1.json'
    second_file = 'tests/fixtures/with_null.json'
    with open('tests/fixtures/expected_with_null.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()


def test_yml_plain():
    first_file = 'tests/fixtures/file1.yml'
    second_file = 'tests/fixtures/file2.yml'
    with open('tests/fixtures/expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()


def test_empty_yml():
    first_file = 'tests/fixtures/file1.yml'
    second_file = 'tests/fixtures/empty.yml'
    with open('tests/fixtures/expected_with_empty.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()