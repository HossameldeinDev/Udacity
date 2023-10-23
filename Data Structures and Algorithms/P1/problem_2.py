import os


def find_files(suffix, path):
    """
    Recursively finds all files beneath the path with the given file name suffix.

    Args:
      suffix(str): suffix of the file name to be found.
      path(str): path of the file system.

    Returns:
       a list of paths.
    """
    files_found = []

    if not os.path.exists(path):
        return files_found

    if os.path.isfile(path):
        if path.endswith(suffix):
            files_found.append(path)
        return files_found

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        files_found.extend(find_files(suffix, item_path))

    return files_found


def test_find_files():
    print("=== Test Cases for find_files Function ===\n")

    # Test Case 1: Standard scenario with a specific directory structure
    print("Test Case 1: Standard scenario - Known directory structure")
    result = find_files('.c', "./testdir")  # Assume './testdir' is a directory with test files
    print(result)
    # Expected output: ['list of .c files present in the directory']

    # Test Case 2: Edge Case - Trying a non-existent directory
    print("\nTest Case 2: Edge Case - Non-existent directory")
    result = find_files('.c', "./non_existent_directory")
    print(result)
    # Expected output: []

    # Test Case 3: Edge Case - Using an empty string for the file suffix
    print("\nTest Case 3: Edge Case - Empty suffix (should match all files theoretically)")
    result = find_files('', "./testdir")
    print(result)
    # Expected output: ['list of all files within the directory']

    # Test Case 4: Edge Case - Input path is actually a file, not a directory
    print("\nTest Case 4: Edge Case - Path is a file, not a directory")
    result = find_files('.c', "./testdir/t1.c")  # Assume './testdir/t1.c' is an actual file path
    print(result)
    # Expected output: ['./testdir/t1.c']

    print("\n=== All Test Cases Executed ===")


# The following will run the test function when the script is executed
if __name__ == "__main__":
    test_find_files()
