#!/usr/bin/env python3.4

import argparse
import subprocess
import sys
import os.path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Profiles the files two function.')
    parser.add_argument('file_name_pattern', type=str,
                        help='file name inside the profiling folder')
    args = parser.parse_args()
    file_name_regex = args.file_name_pattern
    file_name = file_name_regex
    project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    shell_command = ('export PYTHONPATH=PYTHONPATH:{proj_dir};'
    'python3.4 -m cProfile -s cumulative profiling/{file_name}')
    output = subprocess.check_output(shell_command.format(
        proj_dir=project_dir, file_name=file_name
    ), shell=True)

    for line in output.decode('UTF-8').split('\n')[:15]:
        print(line)
    print('...')

