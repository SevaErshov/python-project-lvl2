#!usr/bit/env python3
import argparse
from gendiff.parsing import generate_diff, stylish


def main():
    description = 'Compares two configuration files and shows a difference.'
    parser = argparse.ArgumentParser(description=description)
    format_h = 'set format of output'
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('--format', '-f', help=format_h, default=stylish)
    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == '__main':
    main()
