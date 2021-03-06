#!/usr/bin/env python3.4

import argparse
from functools import wraps
import time

from datastructures.python_dict import SampleDict

def get_time(func):
    @wraps(func)
    def inner_function(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        seconds = time.time() - start_time
        print('{func_name} took {seconds}s'.format(
            func_name=func.__name__,
            seconds=seconds
        ))
    return inner_function

@get_time
def insert_items_into_sample_dict():
    dictionary = SampleDict()
    for i in range(1, 1000):  # weird errors for chr(0): the null string (because we think it is null pointer)
        for j in range(1, 1000):
            key = bytes(chr(i) + chr(j), 'UTF-8')
            dictionary.insert(key, i)

@get_time
def insert_items_into_actual_python_dict():
    dictionary = {}
    def assign(key, value):
        if key in dictionary:
            print('key')
            raise
        dictionary[key] = value
    for i in range(1, 1000):
        for j in range(1, 1000):
            key = bytes(chr(i) + chr(j), 'UTF-8')
            assign(key, i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='0 for python version vs 1 for own custom implementation')
    parser.add_argument('implementation', type=int,
                        help='0 for python; 1 for own implementation')
    args = parser.parse_args()
    if args.implementation == 1:
        insert_items_into_sample_dict()
    else:
        insert_items_into_actual_python_dict()
