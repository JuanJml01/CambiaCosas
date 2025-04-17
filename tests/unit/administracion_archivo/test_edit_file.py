import unittest
import os
from src.cambiacosas.administracion_archivo import edit_file
from src.cambiacosas.administracion_archivo import file_info

class TestModifyFileLines(unittest.TestCase):

    def setUp(self):
        self.test_file_path = "test_file.txt"
        with open(self.test_file_path, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_modify_lines_with_string_content(self):
        edit_file.modify_file_lines(self.test_file_path, (2, 4), "New Line 2\nNew Line 3\nNew Line 4")
        with open(self.test_file_path, 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines, ["Line 1\n", "New Line 2\n", "New Line 3\n", "New Line 4\n", "Line 5\n"])

    def test_modify_lines_with_list_content(self):
        edit_file.modify_file_lines(self.test_file_path, (2, 4), ["New Line 2", "New Line 3", "New Line 4"])
        with open(self.test_file_path, 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines, ["Line 1\n", "New Line 2\n", "New Line 3\n", "New Line 4\n", "Line 5\n"])

    def test_modify_lines_at_beginning(self):
        edit_file.modify_file_lines(self.test_file_path, (1, 2), "New Line 1\nNew Line 2")
        with open(self.test_file_path, 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines, ["New Line 1\n", "New Line 2\n", "Line 3\n", "Line 4\n", "Line 5\n"])

    def test_modify_lines_at_end(self):
        edit_file.modify_file_lines(self.test_file_path, (4, 5), "New Line 4\nNew Line 5")
        with open(self.test_file_path, 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines, ["Line 1\n", "Line 2\n", "Line 3\n", "New Line 4\n", "New Line 5\n"])

    def test_modify_lines_single_line(self):
        edit_file.modify_file_lines(self.test_file_path, (3, 3), "New Line 3")
        with open(self.test_file_path, 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines, ["Line 1\n", "Line 2\n", "New Line 3\n", "Line 4\n", "Line 5\n"])

    def test_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            edit_file.modify_file_lines("non_existent_file.txt", (1, 2), "New lines")

    def test_invalid_parameter_types(self):
        with self.assertRaises(TypeError):
            edit_file.modify_file_lines(123, (1, 2), "New lines") # Invalid file_path type
        with self.assertRaises(TypeError):
            edit_file.modify_file_lines(self.test_file_path, "invalid", "New lines") # Invalid line_range type
        with self.assertRaises(TypeError):
            edit_file.modify_file_lines(self.test_file_path, (1, 2), 123) # Invalid new_content type

    def test_invalid_line_range_values(self):
        with self.assertRaises(ValueError):
            edit_file.modify_file_lines(self.test_file_path, (2, 1), "New lines") # start_line > end_line
        with self.assertRaises(ValueError):
            edit_file.modify_file_lines(self.test_file_path, (0, 2), "New lines") # start_line <= 0
        with self.assertRaises(ValueError):
            edit_file.modify_file_lines(self.test_file_path, (1, 0), "New lines") # end_line <= 0
        with self.assertRaises(ValueError):
            edit_file.modify_file_lines(self.test_file_path, (6, 7), "New lines") # line_range exceeds file lines

    def test_modify_lines_with_slice_object(self):
        edit_file.modify_file_lines(self.test_file_path, slice(2, 5), ["New Line 2", "New Line 3", "New Line 4"])
        with open(self.test_file_path, 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines, ["Line 1\n", "New Line 2\n", "New Line 3\n", "New Line 4\n"])

    def test_invalid_slice_step(self):
        with self.assertRaises(ValueError):
            edit_file.modify_file_lines(self.test_file_path, slice(1, 5, 2), "New lines") # Slice step is not None

if __name__ == '__main__':
    unittest.main()