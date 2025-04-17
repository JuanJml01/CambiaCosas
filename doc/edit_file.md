# Documentation for `modify_file_lines` function

## Function: `modify_file_lines(file_path, line_range, new_content)`

Modifies a text file, replacing a specified range of lines with new content. If `line_range` is not provided, the entire file will be modified.

### Parameters:

-   `file_path` (str): The path to the file to be modified.
-   `line_range` (tuple or slice, optional): A tuple `(start_line, end_line)` or a slice object that defines the range of lines (1-based) to replace (inclusive). If not provided, the entire file range is used.
-   `new_content` (str or list of str): The content to replace the specified lines.
    -   If it is a string, it is treated as a single block of text.
    -   If it is a list of strings, each string is a line of new content.

### Returns:

This function modifies the file in place and does not return any value.

### Raises:

-   `FileNotFoundError`: If the specified `file_path` does not exist.
-   `ValueError`:
    -   If `start_line` \> `end_line`.
    -   If line numbers are not positive integers.
    -   If the line range is invalid for the file content.
-   `TypeError`: If the parameters are of incorrect types.

### Example:

```python
from src.cambiacosas.administracion_archivo.edit_file import modify_file_lines

# Example 1: Replace lines 2 to 4 with a single string
modify_file_lines("my_file.txt", (2, 4), "This is the new line 2.\\nThis is the new line 3.\\nThis is the new line 4.")

# Example 2: Replace lines 2 to 4 with a list of strings
modify_file_lines("my_file.txt", slice(2, 5), ["New line 2", "New line 3", "New line 4"])

# Example 3: Replace the entire file content
modify_file_lines("my_file.txt", None, "This replaces the entire file content")