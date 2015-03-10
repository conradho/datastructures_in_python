#!/usr/bin/env python3.4

import argparse
import shlex
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
        if file_path[-3:] != '.py' or file_path[-11:] == '__init__.py':
            continue

        time_command = 'bash -c "' + export_env + 'time python3.4 ' + file_path + ' {implementation}"'

        cprofile_command = 'bash -c "{} python3.4 -m cProfile -s cumulative {} {{implementation}}"'.format(
            export_env, file_path
        )

        malloc_command = 'bash -c "{} python3.4 -X tracemalloc {} {{implementation}}"'.format(
            export_env, file_path
        )

        for implementation in (0, 1):
            subprocess.call(shlex.split(time_command.format(implementation=implementation)))
            print('*' * 80, '\nRe-running with cProfile... ...')
            output = subprocess.check_output(shlex.split(cprofile_command.format(implementation=implementation)))

            for line in output.decode('UTF-8').split('\n')[:20]:
                print(line)
            print('*' * 80)

            subprocess.call(shlex.split(malloc_command.format(implementation=implementation + 10)))
            print('*' * 80)
