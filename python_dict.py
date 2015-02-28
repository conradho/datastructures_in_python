#!/usr/bin/env python3.4
import ctypes

class DictItem(ctypes.Structure):
    _fields_ = [
        ("key", ctypes.c_char_p),
        ('value', ctypes.c_int),
    ]

class KeyAlreadyExistsInDictError(Exception):
    pass

class KeyDoesNotExistInDictError(Exception):
    pass

class DictIsFullError(Exception):
    pass

class SampleDict(object):
    """
    http://svn.python.org/projects/python/trunk/Objects/dictobject.c
    """
    starting_length = 8

    def __init__(self):
        """initialize a dict taking strings as keys and ints as values"""
        self.allocated_length = self.starting_length
        FixedArrayType = ctypes.POINTER(DictItem) * self.allocated_length
        self.c_dict_array = FixedArrayType()
        self.fill = 0

    def _resize(self):
        pointers = filter(bool, self.c_dict_array)
        self.allocated_length = self.allocated_length * 4
        FixedArrayType = ctypes.POINTER(DictItem) * self.allocated_length
        self.c_dict_array = FixedArrayType()
        for pointer in pointers:
            self.insert(pointer.contents.key, pointer.contents.value)

    @staticmethod
    def _hash(value):
        return hash(value)

    def _compute_index_position(self, key):
        return self._hash(key) & (self.allocated_length - 1)

    def insert(self, key, value):
        item_ptr = ctypes.pointer(DictItem(key, value))
        position = self._compute_index_position(key)
        pointer = self.c_dict_array[position]
        if float(self.fill) / self.allocated_length > 0.667:
            self._resize()
        for _ in range(self.allocated_length):
            if not pointer:
                # pointer is null, we have blank space!
                self.c_dict_array[position] = item_ptr
                self.fill += 1
                return
            if pointer.contents.key == key:
                raise KeyAlreadyExistsInDictError
            # use open addressing to get next position
            position = (position + 1) % self.allocated_length
            pointer = self.c_dict_array[position]
        raise DictIsFullError

    def get_value(self, key):
        position = self._compute_index_position(key)
        pointer = self.c_dict_array[position]
        for _ in range(self.allocated_length):
            if not pointer:
                raise KeyDoesNotExistInDictError
            if pointer.contents.key == key:
                return pointer.contents.value
            position = (position + 1) % self.allocated_length
            pointer = self.c_dict_array[position]
        raise KeyDoesNotExistInDictError

