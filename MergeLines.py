from Npp import notepad, editor
import os
import configparser


SCRIPT_NAME = "MergeLines"


# Wim Gielis
# Feb. 2025
#
# MergeLines script (Alt-m):
#       - The selected lines are merged with a chosen separator
#       - The separator is asked from the user in a prompt
#       - If the selected text contains empty lines, these can be retained or not in the final merged string.
#         A message box will ask the user to retain the empty lines or not. Default: not retain empty lines.
#       - The chosen separator will be stored/retrieved from an ini configuration file


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

# Get the stored separator, if it exists
# Remove the first and last character (double quotes)
stored_separator = config.get(script_section, "separator", fallback=None)[1:-1]

# Define the separator you want between merged lines
separator = notepad.prompt("Please enter the separator (1 is comma, 2 is pipe, 3 is plus sign)", "Separator", stored_separator if stored_separator else ', ')

if not separator is None:
    # the user did not cancel the prompt
    
    # if separator:
        # # the user provided a separator

    match separator:
        case '1':
            separator = ', '
        case '2':
            separator = '|'
        case '3':
            separator = ' + '

    # Get the selection start position
    selection_start = editor.getSelectionStart()
    
    # Get the selected lines of text
    selected_text = editor.getSelText()

    # If there is no selection, do nothing
    if not selected_text.strip():
        notepad.messageBox("Please select multiple lines to merge!", "Merge Lines", 0)
    else:
        # Check if there are empty lines in the selection
        selection_has_empty_lines = any(line.strip() == "" for line in selected_text.splitlines())
        if selection_has_empty_lines:
            # Ask the user whether to remove (1) or retain (not 1) empty lines
            remove_empty_lines = notepad.messageBox(
                "Your selection contains empty lines.\nDo you want to  REMOVE  them in the merged text?", 
                "Empty Lines", MESSAGEBOXFLAGS.YESNO ) == 6  # 6 = Yes, 7 = No
        else:
            remove_empty_lines = False  # No empty lines, so just proceed

        # Merge lines based on user's choice
        if remove_empty_lines:
            merged_text = separator.join([line for line in selected_text.splitlines() if line.strip()])
        else:
            merged_text = separator.join(selected_text.splitlines())

        # Replace the selected text with the merged version
        editor.replaceSel(merged_text)

        # Move the cursor back to the start of the original selection
        editor.setSelection(selection_start, selection_start)

        # Update the configuration file
        # Ensure the section exists before writing
        if not config.has_section(script_section):
            config.add_section(script_section)

        # Store the separator in the INI file
        config.set(script_section, "separator", f'"{separator}"')

        # Write changes to the INI file
        with open(ini_file, "w") as configfile:
            config.write(configfile)