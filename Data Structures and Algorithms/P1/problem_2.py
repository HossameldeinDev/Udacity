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
    print("=== Test Cases for find_files function ===\n")

    # Test Case 1: Normal Case
    print("Test Case 1: Normal Case - Directory with known structure")
    path_normal = "./testdir"  # Use a relevant directory path
    result = find_files('.c', path_normal)
    print(f"Expected: ['List of .c files'], Actual: {result}\n")

    # Test Case 2: Edge Case - Non-existent Directory
    print("Test Case 2: Edge Case - Non-existent directory")
    path_non_existent = "./non_existent_directory"
    result = find_files('.c', path_non_existent)
    print(f"Expected: [], Actual: {result}\n")

    # Test Case 3: Edge Case - Empty Suffix
    print("Test Case 3: Edge Case - Empty suffix, which should theoretically match all files")
    path_empty_suffix = "./testdir"  # Use a relevant directory path
    result = find_files('', path_empty_suffix)
    print(f"Expected: ['List of all files'], Actual: {result}\n")

    # Test Case 4: Edge Case - Path to a file, not a directory
    print("Test Case 4: Edge Case - Path provided is a file, not a directory")
    path_not_directory = "./testdir/t1.c"  # Use an actual file path
    result = find_files('.c', path_not_directory)
    print(f"Expected: [path_not_directory], Actual: {result}\n")

    print("=== Test Execution Completed ===")


if __name__ == "__main__":
    test_find_files()
