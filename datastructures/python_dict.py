#!/usr/bin/env python3.4
from collections import namedtuple

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
    DictItem = namedtuple('DictItem', ['key', 'value'])

    def __init__(self):
        """initialize a dict taking strings as keys and ints as values"""
        self.allocated_length = self.starting_length
        self.c_dict_array = [None] * self.allocated_length
        self.fill = 0

    def _resize(self):
        dict_items = filter(bool, self.c_dict_array)
        self.allocated_length = self.allocated_length * 4
        self.c_dict_array = [None] * self.allocated_length
        for dict_item in dict_items:
            self.insert(dict_item.key, dict_item.value)

    @staticmethod
    def _hash(value):
        return hash(value)

    def _get_position_generator(self, key):
        j = self._hash(key)
        perturb = j
        mask = self.allocated_length - 1
        for _ in range(self.allocated_length):
            yield j & mask  # modulo the allocated_length
            j = ((j << 2 ) + j + perturb + 1)
            perturb >>= 5  # right shift by 2^5

    def insert(self, key, value):
        if float(self.fill) / self.allocated_length > 0.667:
            self._resize()
        new_object = self.DictItem(key, value)
        position = self.find_blank_position(key)
        self.c_dict_array[position] = new_object
        self.fill += 1

    def get_value(self, key):
        position = self.find_position_of_inserted_key(key)
        return self.c_dict_array[position].value

    def pop(self, key):
        position = self.find_position_of_inserted_key(key)
        value = self.c_dict_array[position].value
        self.c_dict_array[position] = None
        self.fill -= 1
        return value

    def find_blank_position(self, key):
        position_generator = self._get_position_generator(key)
        for _ in range(self.allocated_length):
            position = next(position_generator)
            pointer = self.c_dict_array[position]
            if not pointer:
                return position
            if pointer.key == key:
                raise KeyAlreadyExistsInDictError('({}, {})'.format(key, pointer.value))
        raise DictIsFullError('{}'.format(key))

    def find_position_of_inserted_key(self, key):
        position_generator = self._get_position_generator(key)
        for _ in range(self.allocated_length):
            position = next(position_generator)
            pointer = self.c_dict_array[position]
            if not pointer:
                raise KeyDoesNotExistInDictError
            if pointer.key == key:
                return position
        raise KeyDoesNotExistInDictError
