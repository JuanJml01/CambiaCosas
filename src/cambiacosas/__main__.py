import sys
import os
import pathlib
import tempfile
import argparse # Add argparse import
# No longer need json import
from typing import List, Dict, Optional, Union, Tuple, Any # Add Any for Union return type
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


def process_large_file(file_info: Dict, prompt_content: str, divide: bool) -> Union[str, bool]:
    """
    Processes a large file (>300 lines).
    If divide is False, splits into chunks, processes each, combines results, and returns the combined string.
    If divide is True, splits into chunks, processes each, saves each chunk permanently, and returns True on success, False on failure.

    Args:
        file_info (Dict): File information ('full_path', 'name', 'content').
        prompt_content (str): The prompt to apply to each chunk.
        divide (bool): If True, save chunks as separate files instead of merging.

    Returns:
        Union[str, bool]: Combined content string if divide is False and successful.
                          True if divide is True and successful.
                          An empty string or False if processing fails.
    """

    lines = file_info['content'].splitlines(keepends=True)
    chunk_size = 300
    total_chunks = (len(lines) + chunk_size - 1) // chunk_size
    modified_chunks_content = []
    temp_files = []
    processed_chunk_paths = [] # Keep track of successfully saved permanent chunks if divide=True

    original_path = pathlib.Path(file_info['full_path'])
    original_name = file_info['name']

    try:
        for i in range(0, len(lines), chunk_size):
            chunk_index = i // chunk_size
            chunk_lines = lines[i:i + chunk_size]
            chunk_content = "".join(chunk_lines)
            chunk_num = chunk_index + 1

            print(f"    Processing chunk {chunk_num}/{total_chunks} for {original_name}...")

            # --- Gemini API Call ---
            gemini_config = GeminisOptions()
            input_text = f"You are a tool that reads a file, applies the following change — '{prompt_content}' — and rewrites the file with the modification.\n'{chunk_content}'"
            gemini_config.set_input_text(input_text)

            api_response = call_gemini_api(gemini_config)
            if not api_response:
                print(f"    Error calling Gemini API for chunk {chunk_num} of {original_name}.")
                # If dividing, we should ideally clean up previously saved chunks, but for simplicity, we just fail.
                return False if divide else ""

            modified_chunk_data = parse_gemini_response(api_response)
            if not modified_chunk_data:
                print(f"    Error parsing Gemini response for chunk {chunk_num} of {original_name}.")
                return False if divide else ""

            # Extract text content from response
            if isinstance(modified_chunk_data, dict) and modified_chunk_data:
                modified_text = next(iter(modified_chunk_data.values()), None)
                if modified_text is None or not isinstance(modified_text, str):
                    print(f"    Invalid text content in Gemini response for chunk {chunk_num} of {original_name}: {modified_chunk_data}")
                    return False if divide else ""
            else:
                 print(f"    Invalid or empty response from parse_gemini_response for chunk {chunk_num} of {original_name}: {modified_chunk_data}")
                 return False if divide else ""
            # --- End Gemini API Call ---

            if divide:
                # Save chunk permanently
                output_filename = f"{original_path.stem}.part{chunk_num}{original_path.suffix}"
                output_path = original_path.parent / output_filename
                metadata_header = f"# Original File: {original_name}\n" \
                                  f"# Part: {chunk_num} / {total_chunks}\n" \
                                  f"# Prompt Applied: {prompt_content}\n" \
                                  f"# ---\n"
                try:
                    with open(output_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(metadata_header)
                        f_out.write(modified_text)
                    processed_chunk_paths.append(output_path) # Track success
                    print(f"    Successfully processed and saved chunk {chunk_num} to {output_filename}.")
                except IOError as e:
                    print(f"    Error writing permanent chunk file {output_filename}: {e}")
                    # Clean up already saved chunks for this file? Maybe too complex for now. Fail explicitly.
                    return False # Indicate failure for divide mode
            else:
                # Use temporary file and store content for merging (existing logic)
                 # Create a temporary file for the chunk (needed for cleanup tracking)
                 with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt", encoding='utf-8') as temp_f:
                     # We don't strictly need to write the original chunk here anymore,
                     # but we need the temp file path for the finally block.
                     # Let's just keep track of paths without writing.
                     temp_path = temp_f.name
                     temp_files.append(temp_path) # Keep track for cleanup

                 modified_chunks_content.append(modified_text)
                 print(f"    Successfully processed chunk {chunk_num}.")

        # --- Loop finished ---
        if divide:
            # If we got here, all chunks were processed and saved successfully
            return True
        else:
            # Combine modified chunks
            return "".join(modified_chunks_content)

    except Exception as e:
        print(f"    An error occurred during large file processing for {original_name}: {e}")
        return False if divide else "" # Indicate failure
    finally:
        # Clean up temporary files ONLY if not dividing
        if not divide:
            for temp_path in temp_files:
                try:
                    os.remove(temp_path)
                except OSError as e:
                    print(f"    Warning: Could not remove temporary file {temp_path}: {e}")

def process_files_with_gemini(file_info_list: List[Dict], prompt_content: str, divide: bool):
    """
    Processes each file using the Gemini API. Handles large files by chunking.
    If divide is True, large files are split into permanent chunk files and the original is deleted on success.

    Args:
        file_info_list (List[Dict]): List of file info dictionaries.
        prompt_content (str): The prompt to apply.
        divide (bool): Whether to divide large files into permanent chunks.
    """
    for file_info in file_info_list:
        original_file_path = file_info['full_path'] # Store for potential deletion
        original_file_name = file_info['name']
        print(f"Processing file: {original_file_path}...")
        try:
            # Check the number of lines in the file
            line_count = len(file_info['content'].splitlines())
            text_content = "" # Initialize text_content for non-divide case
            process_as_large_file = line_count > 300
            skip_final_write = False # Flag to skip writing if dividing

            if process_as_large_file:
                print(f"  File {original_file_name} has {line_count} lines, exceeding 300 lines. Processing in chunks...")
                # Call process_large_file with the divide flag
                large_file_result = process_large_file(file_info, prompt_content, divide)

                if divide:
                    if large_file_result is True:
                        print(f"  Successfully processed and divided large file {original_file_name} into chunks.")
                        skip_final_write = True # Don't rewrite original
                        # Try deleting the original file
                        try:
                            os.remove(original_file_path)
                            print(f"  Successfully deleted original large file: {original_file_name}")
                        except OSError as e:
                            print(f"  Warning: Could not delete original large file {original_file_name}: {e}")
                        # Successfully divided, continue to next file in the list
                        continue
                    else: # large_file_result is False
                        print(f"  Failed to process and divide large file {original_file_name}.")
                        continue # Skip to next file
                else: # Not dividing, expect combined content string
                    # Check if the result is a non-empty string (success)
                    if isinstance(large_file_result, str) and large_file_result:
                         text_content = large_file_result # Use the combined content
                    else: # Result is empty string "" (failure)
                        print(f"  Failed to process large file {original_file_name} for merging.")
                        continue # Skip to next file

            else: # Process normally for files <= 300 lines
                # Create GeminisOptions instance
                gemini_config = GeminisOptions()

                # Format input text and set it
                input_text = f"You are a tool that reads a file, applies the following change — '{prompt_content}' — and rewrites the file with the modification.\n'{file_info['content']}'"
                gemini_config.set_input_text(input_text)

                # Call Gemini API
                api_response = call_gemini_api(gemini_config)
                if not api_response:
                    print(f"  Error calling Gemini API for {file_info['name']}.")
                    continue # Skip to next file

                # Parse response
                modified_content_data = parse_gemini_response(api_response)
                if not modified_content_data:
                    print(f"  Error parsing Gemini response for {file_info['name']}.")
                    continue # Skip to next file

                # Extract text content from response dict
                if isinstance(modified_content_data, dict) and modified_content_data:
                    extracted_text = next(iter(modified_content_data.values()), None)
                    if extracted_text is None or not isinstance(extracted_text, str):
                        print(f"  Could not extract valid text content from Gemini response dict for {file_info['name']}: {modified_content_data}")
                        continue # Skip to next file
                    text_content = extracted_text # Assign extracted text
                else:
                    print(f"  Invalid or empty dictionary received from parse_gemini_response for {file_info['name']}: {modified_content_data}")
                    continue # Skip to next file

            # --- End of if/else for large/small file processing ---

            # Write the final modified content back to the original file
            # This should only happen if we are NOT dividing a large file.
            if not skip_final_write:
                if text_content: # Ensure we have content to write (from small file or merged large file)
                    modify_file_lines(file_path=original_file_path, line_range=None, new_content=text_content)
                    print(f"  Successfully modified {original_file_name}.")
                else:
                    # This case implies an issue occurred in small file processing or merging large file
                    # (or large file processing failed before setting text_content)
                    if not process_as_large_file: # Only print if it wasn't a large file failure (already logged)
                        print(f"  No valid content generated for {original_file_name}, skipping modification.")

        except Exception as e:
            print(f"  An error occurred while processing {original_file_name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Process files using Gemini API, with optional chunking for large files.")
    parser.add_argument("folder_name", help="Path to the folder containing files to process.")
    parser.add_argument("prompt_file", help="Path to the file containing the processing prompt.")
    parser.add_argument("--divide", action="store_true", help="Divide large files (>300 lines) into separate processed chunk files instead of merging.")

    args = parser.parse_args()

    folder_name = args.folder_name
    prompt_file_path = args.prompt_file
    divide_flag = args.divide

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
             process_files_with_gemini(file_info_results, prompt_content, divide_flag) # Pass the divide flag
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