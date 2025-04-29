from Npp import notepad, editor
import os
import re


BASE_FOLDER = r"D:\OneDrive - Aexis Belgium NV\Wim\TM1\TI processes"


# Wim Gielis
# Apr. 2025
#
# OpenProcess script (Alt-g):
#       - For the selected text: open the TI process that is found by:
#         * adding the file extension ".pro"
#         * opening the file straight in the same Notepad++ window


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
    file_name = selection.strip() + ".pro"
    console.write(file_name)
    full_path = os.path.join(BASE_FOLDER, file_name)
    if os.path.exists(full_path):
        notepad.open(full_path)
    else:
        notepad.messageBox(f"File not found:\n{full_path}", "File not found")