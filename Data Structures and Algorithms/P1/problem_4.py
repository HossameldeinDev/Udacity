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

## Add your own test cases: include at least three test cases
## and two of them must include edge cases, such as null, empty or very large values


# Assuming the hierarchy is already built as in your provided structure

# Test Case 1: User is directly in the group
assert is_user_in_group("sub_child_user", sub_child) == True, "Test Case 1 Failed"

# Test Case 2: User is in a subgroup
assert is_user_in_group("sub_child_user", parent) == True, "Test Case 2 Failed"

# Test Case 3: User is not in the group or any subgroups
assert is_user_in_group("nonexistent", parent) == False, "Test Case 3 Failed"

# Test Case 4: Edge case - null user
assert is_user_in_group(None, parent) == False, "Test Case 4 Failed"

# Test Case 5: Edge case - very large number of users (performance)
large_group = Group("large")
for i in range(1000000):  # let's say we add a million users
    large_group.add_user(f"user_{i}")
assert is_user_in_group("user_999999", large_group) == True, "Test Case 5 Failed"

print("All test cases pass")