#!/usr/bin/env python3.4

import argparse
import subprocess
import sys
import os.path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Profiles the files two function.')
    parser.add_argument('file_paths', type=str, nargs='+',
                        help='file or files')
    args = parser.parse_args()
    project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    export_env = 'export PYTHONPATH=PYTHONPATH:{};'.format(project_dir)

    for file_path in args.file_paths:
        if file_path[-3:] != '.py':
            continue
        subprocess.call(export_env + 'time python3.4 ' + file_path, shell=True)
        print('*' * 80, '\nRe-running with cProfile... ...')
        output = subprocess.check_output(
            export_env + 'python3.4 -m cProfile -s cumulative ' + file_path,
            shell=True
        )

        for line in output.decode('UTF-8').split('\n')[:20]:
            print(line)
        print('*' * 80)

