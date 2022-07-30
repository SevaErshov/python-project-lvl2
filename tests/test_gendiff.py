import gendiff as g
from gendiff.formatter.plain import compose_diff
import pytest


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


def test_null_json():
    first_file = 'tests/fixtures/file1.yml'
    second_file = 'tests/fixtures/with_null.yml'
    with open('tests/fixtures/expected_with_null.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()


def test_nested_json():
    first_file = 'tests/fixtures/nested_file1.json'
    second_file = 'tests/fixtures/nested_file2.json'
    with open('tests/fixtures/nested_expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()


def test_nested_yml():
    first_file = 'tests/fixtures/nested_file1.yml'
    second_file = 'tests/fixtures/nested_file2.yml'
    with open('tests/fixtures/nested_expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file) == expected.read()


def test_json_plain_format():
    first_file = 'tests/fixtures/nested_file1.json'
    second_file = 'tests/fixtures/nested_file2.json'
    with open('tests/fixtures/plain_format_expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file, g.plain) == expected.read()


def test_yaml_plain_format():
    first_file = 'tests/fixtures/nested_file1.yml'
    second_file = 'tests/fixtures/nested_file2.yml'
    with open('tests/fixtures/plain_format_expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file, g.plain) == expected.read()


@pytest.fixture
def decompose():
    return {
        "+ cookie": 'milk',
        "- cookie": 'drink',
        "+ honey": 'bee',
        "  nested":{
            '- cool': 'wow',
            '+ cool': 'not wow',
            '  good': 'very'
        }
    }


@pytest.fixture
def expected_compose():
    return {
        "-+cookie": 'drink',
        "+ honey": 'bee',
        "  nested": {
            '-+cool': 'wow',
            '  good': 'very'
        }
    }

def test_compose_diff(decompose, expected_compose):
    value = decompose
    expected = expected_compose
    updated_expected = {
        "-+cookie": 'milk',
        '-+cool': 'not wow'
    }
    updated = compose_diff(value)
    assert updated == updated_expected
    assert value == expected
