class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string


    def append(self, value):

        if self.head is None:
            self.head = Node(value)
            return

        node = self.head
        while node.next:
            node = node.next

        node.next = Node(value)

    def size(self):
        size = 0
        node = self.head
        while node:
            size += 1
            node = node.next

        return size

def union(llist_1, llist_2):
    # Create a set to store the elements
    union_set = set()

    # Helper function to add elements of a list to the set
    def add_elements(node):
        while node:
            union_set.add(node.value)
            node = node.next

    # Add elements for both linked lists
    add_elements(llist_1.head)
    add_elements(llist_2.head)

    # Create a new linked list from the union set
    result_list = LinkedList()
    for value in union_set:
        result_list.append(value)

    return result_list


def intersection(llist_1, llist_2):
    # Create sets to store the elements of both linked lists
    set_1 = set()
    set_2 = set()

    node = llist_1.head
    while node:
        set_1.add(node.value)
        node = node.next

    node = llist_2.head
    while node:
        set_2.add(node.value)
        node = node.next

    # Get the intersection of the sets
    intersection_set = set_1.intersection(set_2)

    # Create a new linked list from the intersection set
    result_list = LinkedList()
    for value in intersection_set:
        result_list.append(value)

    return result_list


# Test Case 1 (Standard Case)
linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,21]
element_2 = [6,32,4,9,6,1,11,21,1]

for i in element_1:
    linked_list_1.append(i)

for i in element_2:
    linked_list_2.append(i)

print(union(linked_list_1, linked_list_2))
# Expected output: elements in either linked_list_1 or linked_list_2, without duplicates

print(intersection(linked_list_1, linked_list_2))
# Expected output: elements common in both linked_list_1 and linked_list_2


# Test Case 2 (Standard Case)
linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,23]
element_2 = [1,7,8,9,11,21,1]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

print(union(linked_list_3, linked_list_4))
# Expected output: elements in either linked_list_3 or linked_list_4, without duplicates

print(intersection(linked_list_3, linked_list_4))
# Expected output: elements common in both linked_list_3 and linked_list_4


# Test Case 3 (Edge Case: Empty Lists)
linked_list_5 = LinkedList()
linked_list_6 = LinkedList()

print(union(linked_list_5, linked_list_6))
# Expected output: (empty list)

print(intersection(linked_list_5, linked_list_6))
# Expected output: (empty list)


# Test Case 4 (Edge Case: One List is Empty)
linked_list_7 = LinkedList()
linked_list_8 = LinkedList()

for i in [1, 2, 3, 4, 5]:
    linked_list_7.append(i)

print(union(linked_list_7, linked_list_8))
# Expected output: 1 -> 2 -> 3 -> 4 -> 5

print(intersection(linked_list_7, linked_list_8))
# Expected output: (empty list)


# Test Case 5 (Edge Case: Large Values)
linked_list_9 = LinkedList()
linked_list_10 = LinkedList()

for i in [999999999, 888888888]:
    linked_list_9.append(i)

for i in [999999999, 777777777]:
    linked_list_10.append(i)

print(union(linked_list_9, linked_list_10))
# Expected output: 888888888 -> 999999999 -> 777777777

print(intersection(linked_list_9, linked_list_10))
# Expected output: 999999999
