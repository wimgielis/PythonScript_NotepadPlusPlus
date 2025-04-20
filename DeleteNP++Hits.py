from Npp import editor
import re
import os


# Wim Gielis
# Apr. 2025
#
# DeleteNP++Hits script (Alt-w):
#       - When we do a search in all files in Notepad++, the search results window contains filenames and number of hits
#       - We can select all and copy to a new text file
#       - But then removing the number of hits at the end of each line is easiest with a regular expression replace
#       - This script automates it for the selected lines
#       - Also, it will remove the largest common path from the left of each of the lines
#       - Lastly, it will remove the dot and the file extension IF, and only if, all lines share the same file extension


editor.beginUndoAction()

try:
    # Get the selected text (or all text if none is selected)
    selected_text = editor.getSelText()
    if not selected_text:
        selected_text = editor.getText()

    lines = selected_text.splitlines()
    cleaned_lines = []

    # Regex pattern: matches "(1 hit)" or "(23 hits)" at the end of the line
    # for line in lines:
        # cleaned_lines.append(re.sub(hit_pattern, '', line))
    hit_pattern = re.compile(r'\s\(\d+\s+hits?\)$')
    cleaned_lines = [re.sub(hit_pattern, '', line.lstrip()) for line in lines]

    # Compute the longest common path prefix
    common_path = os.path.commonprefix(cleaned_lines)

    # If the common path ends mid-folder or mid-filename, backtrack to the last full path separator
    if not os.path.isdir(common_path):
        common_path = os.path.dirname(common_path)

    # Remove the prefix and clean leading slashes
    stripped_lines = []
    for line in cleaned_lines:
        if line.startswith(common_path):
            remaining = line[len(common_path):].lstrip('/\\')
        else:
            remaining = line
        stripped_lines.append(remaining)

    # Check if all lines have the same extension
    extensions = [os.path.splitext(line)[1] for line in stripped_lines]
    unique_extensions = set(extensions)
    
    if len(unique_extensions) == 1 and list(unique_extensions)[0]:
        ext_to_remove = list(unique_extensions)[0]
        stripped_lines = [line[:-len(ext_to_remove)] if line.endswith(ext_to_remove) else line for line in stripped_lines]

    # Normalize slashes if needed (optional)
    # stripped_lines = [line.lstrip('/\\') for line in stripped_lines]

    new_text = '\r\n'.join(stripped_lines)
    if editor.getSelText():
        start_pos = editor.getSelectionStart()
        end_pos = editor.getSelectionEnd()
        editor.setTargetStart(start_pos)
        editor.setTargetEnd(end_pos)
        editor.setText(new_text)
finally:
    editor.endUndoAction()