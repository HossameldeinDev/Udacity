class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name


parent = Group("parent")
child = Group("child")
sub_child = Group("subchild")

sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)

child.add_group(sub_child)
parent.add_group(child)


def is_user_in_group(user, group):
    """
    Return True if user is in the group, False otherwise.

    Args:
      user(str): user name/id
      group(class:Group): group to check user membership against
    """
    if user is None or group is None:
        return False

    if user in group.get_users():
        return True
    else:
        for subgroup in group.get_groups():
            if is_user_in_group(user, subgroup):
                return True
    return False


# Assuming the setup for groups and users is already done.
# The groups 'parent', 'child', and 'sub_child' are already defined,
# and 'sub_child_user' is added into 'sub_child' group, as in your provided structure.

print("Running test cases for is_user_in_group function...\n")

# Test Case 1: User is directly in the group
print("Test Case 1: User is directly in the group:")
result = is_user_in_group("sub_child_user", sub_child)
print(result)
# Expected output: True

# Test Case 2: User is in a subgroup
print("\nTest Case 2: User is in a subgroup:")
result = is_user_in_group("sub_child_user", parent)
print(result)
# Expected output: True

# Test Case 3: User is not in the group or any subgroups
print("\nTest Case 3: User is not in the group or any subgroups:")
result = is_user_in_group("nonexistent", parent)
print(result)
# Expected output: False

# Test Case 4: Edge case - null user (assuming the function handles null input as "not in group")
print("\nTest Case 4: Edge case - null user:")
result = is_user_in_group(None, parent)
print(result)
# Expected output: False

# Test Case 5: Edge case - very large number of users (performance)
print("\nTest Case 5: Edge case - very large number of users (performance):")
large_group = Group("large")
for i in range(1000000):  # Simulating a large group by adding a million users
    large_group.add_user(f"user_{i}")
result = is_user_in_group("user_999999", large_group)
print(result)
# Expected output: True

print("\nAll test cases have been run.\n")
