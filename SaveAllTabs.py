from Npp import notepad, editor, console
import os
import re


SAVE_FOLDER = r'D:\_\Notepad++tabs'
FILE_PATTERN = r'^\d{2}\.txt$'


# Wim Gielis
# Feb. 2025
#
# SaveAllTabs script (Alt-s):
#       - All tabs in Notepad++ are evaluated for persistance to disk
#         * if the file was saved previously, we simply save the file
#         * if the file was not saved previously, we create a .txt text file in a given folder
#           (the text file will receive an incrementing number with 2 digits and we fill up any gaps in the numbering that might happen)
#       - This code can reduce the risk of losing valuable information
#         although Notepad++ will open all files (even unsaved) in case you close and open Notepad++ entirely
#       - The script will run through all tabs, visually too, so you will see it flicker for a split second


# Get the currently active tab to be able to select it as the last step in the macro
active_buffer_id = notepad.getCurrentBufferID()

# Ensure the save folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Get a list of existing files matching the pattern
existing_numbers = sorted(int(f[:2]) for f in os.listdir(SAVE_FOLDER) if re.match(FILE_PATTERN, f))

# Find the first missing number in the sequence
counter = 1
for num in existing_numbers:
    if num != counter:
        break
    counter += 1

for (full_file_name, bufferID, file_index, view) in notepad.getFiles():
    notepad.activateBufferID(bufferID)
    do_saveas = True
    if os.path.isfile(full_file_name) and os.sep in full_file_name:
        if os.path.exists(full_file_name):
            notepad.save()
            do_saveas = False

    if do_saveas:
        new_file_path = os.path.join(SAVE_FOLDER, f"{counter:02}.txt")
        notepad.saveAs(new_file_path)

        # Find the next missing number for subsequent saves
        counter += 1
        while counter in existing_numbers:
            counter += 1

notepad.activateBufferID(active_buffer_id)