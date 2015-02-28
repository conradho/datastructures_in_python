#!/usr/bin/env python3.4

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
    for i in range(10000):
        key = bytes(chr(i), 'UTF-8')
        dictionary.insert(key, i)

@get_time
def insert_items_into_normal_dict():
    dictionary = {}
    for i in range(10000):
        key = bytes(chr(i), 'UTF-8')
        dictionary[key] = i

def main():
    insert_items_into_sample_dict()
    insert_items_into_normal_dict()
