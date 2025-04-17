import pytest
import os
import json
import stat
from src.cambiacosas.administracion_archivo.file_info import get_file_info

@pytest.fixture
def temp_dir(tmp_path):
    d = tmp_path / "test_files"
    d.mkdir()
    return d

@pytest.fixture
def temp_file_txt(temp_dir):
    p = temp_dir / "test_file.txt"
    p.write_text("Hello content")
    return p

@pytest.fixture
def temp_file_json(temp_dir):
    p = temp_dir / "test_file.json"
    data = {"key": "value"}
    p.write_text(json.dumps(data))
    return p

@pytest.fixture
def temp_file_empty(temp_dir):
    p = temp_dir / "empty_file.txt"
    p.write_text("")
    return p

@pytest.fixture
def temp_file_special_chars(temp_dir):
    p = temp_dir / "file_with_ç特殊 characters.txt"
    p.write_text("Special characters content")
    return p

@pytest.fixture
def temp_file_long_path(temp_dir):
    long_name = "long_file_name_" + "a" * 200 + ".txt"
    p = temp_dir / long_name
    p.write_text("Long path test")
    return p

def test_get_file_info_txt(temp_file_txt):
    file_info = get_file_info(temp_file_txt)
    assert file_info["name"] == "test_file.txt"
    assert file_info["full_path"] == str(temp_file_txt.resolve())
    assert file_info["content"] == "Hello content"
    assert "metadata" in file_info
    assert file_info["metadata"]["size"] == len("Hello content")
    assert file_info["metadata"]["file_type"] == "file"
    assert "modification_date" in file_info["metadata"]

def test_get_file_info_json(temp_file_json):
    file_info = get_file_info(temp_file_json)
    assert file_info["name"] == "test_file.json"
    assert file_info["full_path"] == str(temp_file_json.resolve())
    assert file_info["content"] == json.dumps({"key": "value"})
    assert "metadata" in file_info
    assert file_info["metadata"]["size"] == len(json.dumps({"key": "value"}))
    assert file_info["metadata"]["file_type"] == "file"
    assert "modification_date" in file_info["metadata"]

def test_get_file_info_empty(temp_file_empty):
    file_info = get_file_info(temp_file_empty)
    assert file_info["name"] == "empty_file.txt"
    assert file_info["content"] == ""
    assert file_info["metadata"]["size"] == 0

def test_get_file_info_special_chars(temp_file_special_chars):
    file_info = get_file_info(temp_file_special_chars)
    assert file_info["name"] == "file_with_ç特殊 characters.txt"
    assert file_info["content"] == "Special characters content"

def test_get_file_info_long_path(temp_file_long_path):
    file_info = get_file_info(temp_file_long_path)
    assert file_info["name"] == temp_file_long_path.name
    assert file_info["full_path"] == str(temp_file_long_path.resolve())
    assert file_info["content"] == "Long path test"

def test_get_file_info_non_existent():
    with pytest.raises(FileNotFoundError):
        get_file_info("non_existent_file.txt")

def test_get_file_info_permission_denied(temp_dir):
    file_path = temp_dir / "permission_denied.txt"
    file_path.write_text("This file is protected")
    os.chmod(file_path, stat.S_IRWXO) # Remove all permissions for others
    with pytest.raises(PermissionError):
        get_file_info(file_path)

def test_get_file_info_invalid_path_directory(temp_dir):
    with pytest.raises(Exception): # Or FileNotFoundError, depending on desired behavior
        get_file_info(temp_dir)