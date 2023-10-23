import heapq
from collections import Counter
from typing import List
import sys


class Node:
    def __init__(self, frequency=0, key=None, left_child=None, right_child=None):
        self.frequency = frequency
        self.left_child = left_child
        self.right_child = right_child
        self.key = key

    def set_left_child(self, node):
        self.left_child = node

    def get_left_child(self):
        return self.left_child

    def set_right_child(self, node):
        self.right_child = node

    def get_right_child(self):
        return self.right_child

    def get_frequency(self):
        return self.frequency

    def is_leaf(self):
        return not (self.get_left_child() or self.get_right_child())

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __repr__(self):
        return f"Node({self.key}, {self.frequency})"


def build_frequency_heap(text: str) -> List[Node]:
    frequency_counter = Counter(text)
    nodes = [Node(key=key, frequency=frequency) for key, frequency in frequency_counter.items()]
    heapq.heapify(nodes)
    return nodes


def build_huffman_tree(heap: List[Node]) -> Node:
    if len(heap) == 1:
        return Node(frequency=heap[0].frequency, left_child=heap[0])
    while len(heap) > 1:
        min_element_1 = heapq.heappop(heap)
        max_element_2 = heapq.heappop(heap)
        new_node = Node(frequency=min_element_1.get_frequency() + max_element_2.get_frequency())
        new_node.set_left_child(min_element_1)
        new_node.set_right_child(max_element_2)
        heapq.heappush(heap, (new_node))
    return heap.pop()


def compute_key_codes(node: Node, code="", code_dict=None) -> dict:
    if code_dict is None:
        code_dict = {}
    left_child = node.get_left_child()
    right_child = node.get_right_child()
    if left_child:
        compute_key_codes(node=left_child, code=code + '0', code_dict=code_dict)
    if right_child:
        compute_key_codes(node=right_child, code=code + '1', code_dict=code_dict)
    if not (right_child or left_child):
        code_dict[node.key] = code
    return code_dict


def build_encode_message(text: str, code_dict: dict) -> str:
    encode = ""
    for character in text:
        encode += code_dict[character]
    return encode


def decode_huffman_code(text: str, root: Node):
    output = ""
    current_node = root
    for bit in text:
        if bit == '0':
            current_node = current_node.get_left_child()
        elif bit == '1':
            current_node = current_node.get_right_child()
        if current_node.is_leaf():
            output += current_node.key
            current_node = root
    return output


def huffman_encoding(data):
    if not data:  # Check if the data is null or empty
        return "", None  # You might choose to return a message or raise an exception

    heap = build_frequency_heap(data)
    root = build_huffman_tree(heap)
    code_dict = compute_key_codes(node=root)
    return build_encode_message(data, code_dict), root


def huffman_decoding(data, tree):
    if not data or tree is None:  # Check if the data or tree is null or empty
        return ""  # You might choose to return a message or raise an exception

    return decode_huffman_code(data, tree)


def perform_test(test_input):
    print("Original size:", sys.getsizeof(test_input))

    encoded_data, tree = huffman_encoding(test_input)

    if encoded_data:  # Proceed only if there's data
        encoded_size = sys.getsizeof(int(encoded_data, base=2))
    else:
        encoded_size = 0  # For empty string, the encoded data size is 0

    print("Encoded size:", encoded_size)

    decoded_data = huffman_decoding(encoded_data, tree)
    decoded_size = sys.getsizeof(decoded_data)

    print("Decoded size:", decoded_size)

    # Verifying the integrity of the data
    assert test_input == decoded_data, "Mismatch in the original and decoded data."

    # For non-empty strings, the encoded size should generally be smaller than the original size
    # For empty strings or single-character strings, this might not hold due to overhead or minimal input.
    if test_input:
        assert encoded_size <= sys.getsizeof(test_input), "Encoded data is larger than original data."

    print("Test Passed.\n")


if __name__ == "__main__":
    codes = {}

    a_great_sentence = "The bird is the word"

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))

    # Add your own test cases: include at least three test cases
    # and two of them must include edge cases, such as null, empty or very large values

    # Test Case 1: Empty String (Edge Case)
    print("Test Case 1: Empty String")
    test_input = ""
    perform_test(test_input)

    # Test Case 2: Single Character String (Edge Case)
    print("\nTest Case 2: Single Character String")
    test_input = "a"
    perform_test(test_input)

    # Test Case 3: Very Large Input (Edge Case)
    print("\nTest Case 3: Very Large Input")
    test_input = "ab" * 1000000  # creates a 2 million character string
    perform_test(test_input)
