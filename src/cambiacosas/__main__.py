import sys
import os
import pathlib
# No longer need json import
from typing import List, Dict, Optional, Union, Tuple # Add necessary types
from src.cambiacosas.administracion_archivo.file_info import get_file_info
from src.cambiacosas.administracion_archivo.edit_file import modify_file_lines
from src.cambiacosas.googleapi.gemini_options import GeminisOptions
from src.cambiacosas.googleapi.api_client import call_gemini_api, parse_gemini_response


def scan_folder(folder_path: str) -> list[dict]:
    """
    Scans all files in the specified folder and retrieves file information.

    Args:
        folder_path (str): Path to the folder to scan.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains
                      file information obtained from get_file_info.
    """
    file_info_list = []
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"Invalid folder path: {folder_path}")

    for file_path_obj in folder.rglob('*'):
        if file_path_obj.is_file():
            try:
                file_info = get_file_info(str(file_path_obj)) # get_file_info expects string path
                file_info_list.append(file_info)
            except Exception as e:
                print(f"Error processing file {file_path_obj}: {e}") # Log error and continue
    return file_info_list


def process_files_with_gemini(file_info_list: List[Dict], prompt_content: str):
    """
    Processes each file using the Gemini API based on the provided prompt.

    Args:
        file_info_list (List[Dict]): A list of dictionaries, where each dictionary
                                     contains file information obtained from get_file_info.
        prompt_content (str): The content of the prompt to apply to each file.
    """
    for file_info in file_info_list:
        print(f"Processing file: {file_info['full_path']}...")
        try:
            # Create GeminisOptions instance (assuming it handles API key loading)
            gemini_config = GeminisOptions()

            # Format input text and set it
            input_text = f"You are a tool that reads a file, applies the following change — '{prompt_content}' — and rewrites the file with the modification.\n'{file_info['content']}'"
            gemini_config.set_input_text(input_text)

            # Call Gemini API
            api_response = call_gemini_api(gemini_config)
            if not api_response:
                print(f"  Error calling Gemini API for {file_info['name']}.")
                continue # Skip to next file

            # Parse response (assuming parse_gemini_response extracts the needed text)
            modified_content = parse_gemini_response(api_response)
            if not modified_content:
                 print(f"  Error parsing Gemini response for {file_info['name']}.")
                 continue # Skip to next file

            # Since modified_content is a dict, extract the text value dynamically.
            # Assuming the dict contains the response text as its primary value.
            if isinstance(modified_content, dict) and modified_content:
                # Get the first value from the dictionary
                text_content = next(iter(modified_content.values()), None)
                if text_content is None or not isinstance(text_content, str):
                    print(f"  Could not extract valid text content from Gemini response dict for {file_info['name']}: {modified_content}")
                    continue # Skip to next file
            else:
                print(f"  Invalid or empty dictionary received from parse_gemini_response for {file_info['name']}: {modified_content}")
                continue # Skip to next file

            # Rewrite the file using the extracted text content
            modify_file_lines(file_path=file_info['full_path'], line_range=None, new_content=text_content)
            print(f"  Successfully modified {file_info['name']}.")

        except Exception as e:
            print(f"  An error occurred while processing {file_info['name']}: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m cambiacosas <folder_name> <prompt_file>")
        sys.exit(1)

    folder_name = sys.argv[1]
    prompt_file_path = sys.argv[2] # Renamed for clarity

    # Read prompt file content
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()
        if not prompt_content:
             raise ValueError("Prompt file is empty.")
    except FileNotFoundError:
        print(f"Error: Prompt file not found at {prompt_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        sys.exit(1)

    try:
        print(f"Scanning folder: {folder_name}...")
        file_info_results = scan_folder(folder_name)
        print(f"Found {len(file_info_results)} files.")

        if file_info_results:
             print("Processing files with Gemini...")
             process_files_with_gemini(file_info_results, prompt_content) # Call the new function
             print("Finished processing files.")
        else:
             print("No files found to process.")

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()