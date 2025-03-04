from Npp import notepad, editor
import os
import configparser


SCRIPT_NAME = "SplitText"


# Wim Gielis
# Mar. 2025
#
# SplitText script (Alt-e):
#       - The selected text is split/unmerged with a chosen separator
#       - For the separator, we first inspect the selected text. If not good candidate is found, the user should enter a separator.
#       - The chosen separator will be stored/retrieved from an ini configuration file


# Get the selection start position
selection_start = editor.getSelectionStart()

# Get the selected lines of text
selected_text = editor.getSelText()

# If there is no selection, do nothing
if not selected_text.strip():
    notepad.messageBox("Please select the text to split!", "Split Text", 0)
else:

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
    stored_separator = config.get(script_section, "separator", fallback=None)
    if stored_separator:
        # Remove the first and last character (double quotes)
        stored_separator = stored_separator[1:-1]

    main_separators = ['\t', ', ', ',', '|', '+ ', '+']
    separator = next((sep for sep in main_separators if selected_text.count(sep) > 2), None)
    separator = separator or stored_separator or ''
    separator = notepad.prompt("Please enter the separator", "Separator", separator)

    if not separator is None:
        # the user did not cancel the prompt

        # if separator:
            # # the user provided a separator

        if separator == '1':
            separator = ', '
        elif separator == '2':
            separator = '|'
        elif separator == '3':
            separator = ' + '

        # Unmerge the selected text based on user's choice
        if separator in selected_text:
            unmerged_text = selected_text.split(separator)
            unmerged = 1
        elif separator.strip() in selected_text:
            unmerged_text = selected_text.split(separator.strip())
            unmerged = 1
        else:
            unmerged = 0

        if unmerged == 1:
            # Replace the selected text with the merged version
            editor.replaceSel('\n'.join(unmerged_text))

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