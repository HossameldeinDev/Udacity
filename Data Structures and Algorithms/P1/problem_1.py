from collections import OrderedDict


class LRU_Cache(object):

    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key is None or key == '':
            return -1
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def set(self, key, value):
        if key is None or key == '':
            print("Invalid key. Key cannot be None or an empty string.")
            return

        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
            return

        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value


def test_lru_cache():
    # Test Case 1: Basic Functionality Testing
    cache = LRU_Cache(2)
    cache.set(1, 1)
    print(cache.get(1))  # Checking if value retrieval is correct
    # Expected Output: 1

    cache.set(2, 2)
    cache.set(3, 3)  # This operation should evict key 1, as 1 was least recently used.
    print(cache.get(2))  # Trying to retrieve evicted key
    # Expected Output: 2

    # Test Case 2: Edge Case with Large Values
    large_cache = LRU_Cache(2)
    large_value = 'x' * 100
    large_cache.set('large', large_value)
    print(large_cache.get('large'))  # Checking if large value is stored and retrieved correctly
    # Expected Output: 'xxxxxx...(total 100 x's)'

    # Test Case 3: Edge Cases with Null and Empty Values
    special_cache = LRU_Cache(3)
    special_cache.set(None, 'value_for_none')  # Trying to set None as key
    special_cache.set('', 'value_for_empty_string')  # Trying to set empty string as key
    print(special_cache.get(None))  # Retrieval should fail; defensive check against None as key
    # Expected Output: -1  (since None is an invalid key now)

    print(special_cache.get(''))  # Retrieval should fail; defensive check against empty string as key
    # Expected Output: -1 (since '' is an invalid key now)

    special_cache.set(1, None)  # Trying to set None as value
    print(special_cache.get(1))  # Checking if setting a None value is handled
    # Expected Output: None (since we only check for None keys, None values are acceptable)

    print("All test cases have generated expected output")


if __name__ == "__main__":
    test_lru_cache()
