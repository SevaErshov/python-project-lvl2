#!usr/bit/env python3
import argparse
from gendiff.parsing import generate_diff


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
