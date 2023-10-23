from collections import OrderedDict


class LRU_Cache(object):

    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


# Test cases
def test_lru_cache():
    print("## Test Case 1: Basic Functionality Testing")
    cache = LRU_Cache(2)

    cache.set(1, 1)
    cache.set(2, 2)
    assert cache.get(1) == 1  # returns 1
    cache.set(3, 3)  # evicts key 2
    assert cache.get(2) == -1  # returns -1 (not found)

    print("\n## Test Case 2: Edge Case with Large Values")
    large_cache = LRU_Cache(2)
    large_value = 'x' * 1000000
    large_cache.set('large', large_value)
    assert large_cache.get('large') == large_value

    print("\n## Test Case 3: Edge Cases with Null and Empty Values")
    special_cache = LRU_Cache(3)
    special_cache.set(None, 'value_for_none')
    special_cache.set('', 'value_for_empty_string')
    assert special_cache.get(None) == 'value_for_none'
    assert special_cache.get('') == 'value_for_empty_string'
    special_cache.set(1, None)
    assert special_cache.get(1) is None

    print("All test cases pass")


if __name__ == "__main__":
    test_lru_cache()
