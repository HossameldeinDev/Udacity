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


def test_huffman_coding():
    print("=== Huffman Coding: Test Cases ===\n")

    # Standard Test Case
    print("Test Case: Standard - Regular sentence with multiple characters")
    a_great_sentence = "The bird is the word"
    print(f"Original content: {a_great_sentence}")
    perform_test(a_great_sentence)
    # Expected: Encoded data is smaller than original data. Decoded data matches original content.

    # Edge Test Cases
    edge_cases = [
        ("", "Test Case: Edge - Empty String"),
        ("a", "Test Case: Edge - Single Character String"),
        ("ab" * 1000000, "Test Case: Edge - Very Large Input"),
    ]

    for test_input, description in edge_cases:
        print(description)
        perform_test(test_input)
        # For empty string: Expected encoded size is 0; no change after decoding.
        # For single character: Encoded data may not be smaller due to overhead, but decoding should match original.
        # For very large input: Encoded data should be significantly smaller, and decoding should reproduce the original input.

    print("=== All Test Cases Executed ===")


def perform_test(test_input):
    print(f"Original size: {sys.getsizeof(test_input)} bytes")

    encoded_data, tree = huffman_encoding(test_input)

    encoded_size = sys.getsizeof(int(encoded_data, base=2)) if encoded_data else 0  # Handling empty string scenario
    print(f"Encoded size: {encoded_size} bytes")

    decoded_data = huffman_decoding(encoded_data, tree)
    print(f"Decoded size: {sys.getsizeof(decoded_data)} bytes")

    # Data integrity check
    assert test_input == decoded_data, "Mismatch between original and decoded data."

    # Size efficiency check (Not applicable for very small strings due to overhead)
    if test_input and len(test_input) > 1:
        assert encoded_size <= sys.getsizeof(test_input), "Encoded data is larger than original data."

    print("Test Passed.\n")


# Triggering the test function when the script runs
if __name__ == "__main__":
    test_huffman_coding()
