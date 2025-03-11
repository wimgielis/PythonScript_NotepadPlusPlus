from Npp import editor, notepad, console, MESSAGEBOXFLAGS
import re
import os
import configparser


SCRIPT_NAME = "SearchTextInFolderKeepOrDeleteFiles"


# Wim Gielis
# Mar. 2025
#
# SearchTextInFolderKeepOrDeleteFiles script (no shortcut, use the menu):
#       - Enter a search string, a folder path, text file extensions
#       - The script will look up the string in the files of the folder
#       - Enter if you want to delete the files where it is found (and keep   the other files),
#         or:   if you want to keep   the files where it is found (and delete the other files)
#       - A msgbox is shown when the search string is not found.
#       - The chosen settings will be stored/retrieved from an ini configuration file


PREFIX_REGEX = 're&'


# Function to find matching files
def find_matching_files(directory: str, search_text: str, file_extensions: list[str], search_mode: int):
    matching_files = []
    regex_pattern = None

    if search_mode == 1:
        try:
            regex_pattern = re.compile(search_text, re.IGNORECASE)
        except re.error:
            print("Error: Invalid regex pattern!")
            return []

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        contents = f.read()
                        if search_mode == 1:
                            if regex_pattern.search(contents):
                                matching_files.append(file_path)
                        if search_mode == 0:
                            if search_text in contents:
                                matching_files.append(file_path)
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

    return matching_files


# Get script directory (same as script location) for the configuration file
script_path = notepad.getPluginConfigDir()
ini_file = os.path.join(script_path, "config.ini")

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the INI file if it exists
if os.path.exists(ini_file):
    config.read(ini_file)

# Define the section for this script
script_section = SCRIPT_NAME


continue_script = True

if continue_script:
    # Ask for a search string, but try to get if from the configuration file
    search_string = config.get(script_section, "search_string", fallback=None)[1:-1]
    search_string = notepad.prompt("Enter the word or string to search:", "Search string", search_string)
    if not search_string:
        notepad.messageBox( "Error: No search string provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        search_string = search_string.strip()

if continue_script:
    # Ask for a valid folder path
    folder_path = config.get(script_section, "folder_path", fallback=None)
    folder_path = notepad.prompt("Paste the folder path to search in:", "Folder path", folder_path)
    if not folder_path:
        notepad.messageBox( "Error: No folder path provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        folder_path = folder_path.strip('"')

    if not os.path.isdir(folder_path):
        notepad.messageBox( "Error: Invalid folder path!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False

if continue_script:
    # Ask for file extensions
    extensions = config.get(script_section, "extensions", fallback=None)[1:-1]
    extensions = notepad.prompt("Enter file extension(s) (comma-separated, e.g.: txt,log):", "File extensions", extensions)
    if not extensions:
        notepad.messageBox( "Error: No file extension provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        extensions = extensions.strip()

if continue_script:
    # Ask for delete mode
    delete_option = config.get(script_section, "delete_option", fallback=None)[1:-1]
    delete_option = notepad.prompt("Do you want to DELETE files containing the search string? (yes/no):", "DELETE (yes) or KEEP (no) files", delete_option)
    if not delete_option:
        notepad.messageBox( "Error: No delete option provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        delete_option = delete_option.strip().lower()

    if delete_option not in ["yes", "no"]:
        notepad.messageBox( "Error: Invalid choice! Enter 'yes' or 'no'.", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False

if continue_script:
    # Get matching files
    extensions = [f".{ext.strip()}" for ext in extensions.split(",")]

    if search_string.startswith(PREFIX_REGEX):
        # prefix means a regex search
        search_mode = 1
        search_string = search_string[len(PREFIX_REGEX):]
    else:
        # default case is a literal search
        search_mode = 0

    files_to_keep = find_matching_files(folder_path, search_string, extensions, search_mode)
    if not files_to_keep:
        notepad.messageBox( "The search string was not found in the folder.\n\n" + search_string, "No hits", MESSAGEBOXFLAGS.OK )
    else:
        # Perform file deletion based on choice
        if delete_option == "yes":  # Delete files that contain the search string
            for file_path in files_to_keep:
                os.remove(file_path)
                console.write(f"Deleted: {file_path}")

            notepad.messageBox( "Files containing the search string have been deleted.", "No hits", MESSAGEBOXFLAGS.OK )

        else:  # Keep matching files, delete others
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        file_path = os.path.join(root, file)
                        if file_path not in files_to_keep:
                            os.remove(file_path)
                            console.write(f"Deleted: {file_path}")

            notepad.messageBox( "Files NOT containing the search string have been deleted.", "No hits", MESSAGEBOXFLAGS.OK )

        console.write("\nOperation complete.")

    # Update the configuration file
    # Ensure the section exists before writing
    if not config.has_section(script_section):
        config.add_section(script_section)

    # Store the settings in the INI file
    config.set(script_section, "search_string", f'"{search_string}"')
    config.set(script_section, "folder_path", f'"{folder_path}"')
    config.set(script_section, "delete_option", f'"{delete_option}"')
    # config.set(script_section, "extensions", f'"{', '.join(extensions)}"')

    # Write changes to the INI file
    with open(ini_file, "w") as configfile:
        config.write(configfile)