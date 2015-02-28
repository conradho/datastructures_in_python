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
    export_env = 'export PYTHONPATH=PYTHONPATH:{};'.format(project_dir)
    file_path = 'profiling/{}'.format(file_name)

    subprocess.call(export_env + 'time python3.4 ' + file_path, shell=True)
    print('*' * 80, '\nRe-running with cProfile... ...')
    output = subprocess.check_output(
        export_env + 'python3.4 -m cProfile -s cumulative ' + file_path,
        shell=True
    )

    for line in output.decode('UTF-8').split('\n')[:15]:
        print(line)
    print('...')

