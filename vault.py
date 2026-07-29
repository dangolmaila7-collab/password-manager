"""A custom hash table used to store password entries instead of
Python's built-in dict, using open addressing with linear probing.
"""


class HashEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.deleted = False


class PasswordVault:
    """Custom hash table mapping a site name to (username, password)."""

    def __init__(self, capacity=64):
        self.capacity = capacity
        self.size = 0
        self.slots = [None] * capacity

    def _hash(self, key):
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % self.capacity
        return h

    def _probe(self, key):
        index = self._hash(key)
        start = index
        while self.slots[index] is not None and self.slots[index].key != key:
            index = (index + 1) % self.capacity
            if index == start:
                raise Exception("Vault is full")
        return index

    def insert(self, key, value):
        if self.size / self.capacity > 0.7:
            self._resize()
        index = self._probe(key)
        if self.slots[index] is None:
            self.size += 1
        self.slots[index] = HashEntry(key, value)

    def get(self, key):
        index = self._hash(key)
        start = index
        while self.slots[index] is not None:
            if self.slots[index].key == key and not self.slots[index].deleted:
                return self.slots[index].value
            index = (index + 1) % self.capacity
            if index == start:
                break
        return None

    def delete(self, key):
        index = self._hash(key)
        start = index
        while self.slots[index] is not None:
            if self.slots[index].key == key:
                self.slots[index].deleted = True
                self.size -= 1
                return True
            index = (index + 1) % self.capacity
            if index == start:
                break
        return False

    def items(self):
        return [(s.key, s.value) for s in self.slots if s and not s.deleted]

    def _resize(self):
        old_slots = self.items()
        self.capacity *= 2
        self.slots = [None] * self.capacity
        self.size = 0
        for key, value in old_slots:
            self.insert(key, value)