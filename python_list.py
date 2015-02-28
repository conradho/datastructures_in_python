#!/usr/bin/env python3.4
import ctypes

class SampleList(object):
    """
    http://svn.python.org/projects/python/trunk/Objects/listobject.c
    """

    def __init__(self, list_of_items=[], list_type=None, starting_length=4):
        """initialize a fixed length array of integers"""
        if list_type is None:
            self.list_type = ctypes.c_int
        else:
            self.list_type = list_type
        length = len(list_of_items)
        self.allocated_length = length if length > starting_length else starting_length
        FixedArrayType = self.list_type * self.allocated_length
        self.c_array = FixedArrayType(*list_of_items)
        self.fill = length

    def append(self, value):
        if self.fill == self.allocated_length:
            self._resize()
        self.c_array[self.fill] = value
        self.fill += 1

    def pop(self):
        self.fill -= 1
        popped = self.c_array[self.fill]
        self.c_array[self.fill] = 0
        return popped

    def index(self, position):
        """
        returns a native python int instead of a c_int, because c_int is a "fundamental data type";
        but would return a py_object because that is not funamental
        """
        return self.c_array[position]

    def get_all(self):
        return self.c_array[:self.fill]

    def _resize(self):
        # allocated_length does not grow like this in python implementation
        self.allocated_length = int(self.allocated_length * 1.1) + 5
        empty_array = self.list_type * self.allocated_length
        self.c_array = empty_array(*self.c_array[:])

