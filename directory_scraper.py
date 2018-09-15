#!/usr/bin/env python3
import re
import os

EMAIL_PATTERN = re.compile(r'''
[a-zA-Z0-9_.+]+
@
[a-zA-Z0-9_.+]+
''', re.VERBOSE)


DIR_PATH = str(os.getcwd()) + "/10.10.10.70"


def read_file(file_path):
    result = []
    with open(file_path, 'r', encoding='latin-1') as reading:
        for file in reading:
            if "10.10.10.70" in file and not file.endswith("css"):
                print(file)
            else:
                continue
            """
            extractedEmail = EMAIL_PATTERN.findall(file)
            for email in extractedEmail:
                result.append(email)
            return result
            """


def walk_thru():
    for dirpath, dirnames, filenames in os.walk(DIR_PATH):
        for file in filenames:
            current_file = os.path.join(dirpath, file)
            file_array = read_file(current_file)
            if not file_array:
                continue
            else:
                print(file_array)


def main():
    if __name__ == "__main__":
        walk_thru()


main()
