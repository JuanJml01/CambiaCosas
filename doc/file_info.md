# Documentation for `get_file_info` function

## Function: `get_file_info(file_path)`

Obtains information about a file.

### Parameters:

-   `file_path` (str): The path to the file.

### Returns:

A dictionary containing file information, including:

-   `name` (str): The name of the file without the path.
-   `metadata` (dict): A dictionary containing file metadata (size, modification date, file type).
-   `full_path` (str): The absolute path to the file.
-   `content` (str): The content of the file as a text string.
-   `line_count` (int): The number of lines in the file.

### Raises:

-   `FileNotFoundError`: If the file does not exist.
-   `PermissionError`: If the file cannot be read due to permissions.
-   `Exception`: For other unexpected errors during file processing.

### Example:

```python
from src.cambiacosas.administracion_archivo.file_info import get_file_info

file_path = "my_file.txt"  # Replace with the actual file path
try:
    file_info_dict = get_file_info(file_path)
    print(file_info_dict)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except PermissionError:
    print(f"Permission denied to read file: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")