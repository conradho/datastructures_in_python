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

    def _get_position_generator(self, key):
        j = self._hash(key)
        perturb = j
        mask = self.allocated_length - 1
        for _ in range(self.allocated_length):
            yield j & mask  # modulo the allocated_length
            j = 5 * j + 1 + perturb
            perturb >>= 5  # right shift by 2^5

    def insert(self, key, value):
        if float(self.fill) / self.allocated_length > 0.667:
            self._resize()
        new_item_pointer = ctypes.pointer(DictItem(key, value))
        position = self.find_blank_position(key)
        self.c_dict_array[position] = new_item_pointer
        self.fill += 1

    def get_value(self, key):
        position = self.find_position_of_inserted_key(key)
        return self.c_dict_array[position].contents.value

    def pop(self, key):
        position = self.find_position_of_inserted_key(key)
        value = self.c_dict_array[position].contents.value
        null_pointer = ctypes.POINTER(DictItem)()
        self.c_dict_array[position] = null_pointer
        self.fill -= 1
        return value

    def find_blank_position(self, key):
        position_generator = self._get_position_generator(key)
        for _ in range(self.allocated_length):
            position = next(position_generator)
            pointer = self.c_dict_array[position]
            if not pointer:
                return position
            if pointer.contents.key == key:
                raise KeyAlreadyExistsInDictError
        raise DictIsFullError

    def find_position_of_inserted_key(self, key):
        position_generator = self._get_position_generator(key)
        for _ in range(self.allocated_length):
            position = next(position_generator)
            pointer = self.c_dict_array[position]
            if not pointer:
                raise KeyDoesNotExistInDictError
            if pointer.contents.key == key:
                return position
        raise KeyDoesNotExistInDictError
