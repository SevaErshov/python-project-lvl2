import gendiff as g
from gendiff.formatter.plain import compose_diff
from gendiff.formatter.json import into_bool
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
        "+ cookie": 'null',
        "- cookie": 'drink',
        "+ honey": 'bee',
        "  nested":{
            '- cool': 'wow',
            '+ cool': 'not wow',
            '  good': 'true'
        }
    }


@pytest.fixture
def expected_compose():
    return {
        "-+cookie": 'drink',
        "+ honey": 'bee',
        "  nested": {
            '-+cool': 'wow',
            '  good': 'true'
        }
    }

def test_compose_diff(decompose, expected_compose):
    value = decompose
    expected = expected_compose
    updated_expected = {
        "-+cookie": 'null',
        '-+cool': 'not wow'
    }
    updated = compose_diff(value)
    assert updated == updated_expected
    assert value == expected


def test_into_bool(decompose):
    value = decompose
    into_bool(value)
    assert value == {
        "+ cookie": None,
        "- cookie": 'drink',
        "+ honey": 'bee',
        "  nested":{
            '- cool': 'wow',
            '+ cool': 'not wow',
            '  good': True
        }
    }


def test_json():
    first_file = 'tests/fixtures/nested_file1.json'
    second_file = 'tests/fixtures/nested_file2.json'
    with open('tests/fixtures/json_format_expected.txt', 'r') as expected:
        assert g.generate_diff(first_file, second_file, g.json) == expected.read()