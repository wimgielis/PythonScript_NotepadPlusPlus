from Npp import notepad, editor
import time
import os
import re


BASE_FOLDER_PRO = r"D:\OneDrive - Aexis Belgium NV\Wim\TM1\TI processes"
BASE_FOLDER_LOG = r"D:\Z_Rest\TM1 Log files TI processes"


# Wim Gielis
# Apr. 2025
#
# OpenProcess script (Alt-g):
#       - For the selected text, open the TI process or log file that is found by:
#         * adding the file extension ".pro"
#         * but if the file extension ".pro" was part of the selection then we use it as such
#         * opening the file straight in the same Notepad++ window
#         * if the pro file could not be found, we still try opening the selection as a log file from the TM1 logging directory
#         * we can make abstraction of a part of the logging file, we will match with the most recent one


def find_latest_file_matching_string(search_string: str, folder: str):
    matched_files = []

    # Walk through all files in the folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            if search_string in file:
                if re.match(r'^TM1ProcessError_\d{14}_\d{5,}_', file):
                    file_path = os.path.join(root, file)
                    matched_files.append(file_path)

    if not matched_files:
        return None

    # Sort matched files by last modified time, descending
    matched_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Return the basename (without path)
    return os.path.basename(matched_files[0])


# Get selected text or word under cursor
selection = editor.getSelText()
if not selection:
    # No selection, get the word under the cursor
    current_pos = editor.getCurrentPos()
    start = editor.wordStartPosition(current_pos, True)
    end = editor.wordEndPosition(current_pos, True)
    selection = editor.getTextRange(start, end)

if not selection:
    notepad.messageBox("No text selected or under cursor.", "Error")
else:
    selected_text = selection.strip()

    # First, let's try a process
    if selected_text.endswith(".pro"):
        file_name = selected_text
    else:
        file_name = selected_text + ".pro"

    full_path = os.path.join(BASE_FOLDER_PRO, file_name)
    if os.path.exists(full_path):
        notepad.open(full_path)
    else:

        # Second, let's try a logfile
        if selected_text.endswith(".log"):
            file_name = selected_text
        else:
            file_name = selected_text + ".log"

        full_path = os.path.join(BASE_FOLDER_LOG, file_name)
        if os.path.exists(full_path):
            notepad.open(full_path)
        else:
            result = find_latest_file_matching_string(selected_text, BASE_FOLDER_LOG)
            if result:
                notepad.open(os.path.join(BASE_FOLDER_LOG, result))
            else:
                notepad.messageBox(f"Files not found as process nor log file.", "File not found")