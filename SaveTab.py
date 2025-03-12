from Npp import notepad, editor
import os
import re


SAVE_FOLDER = r'D:\_\Notepad++tabs'
FILE_PATTERN = r'^\d{2}\.txt$'


# Wim Gielis
# Mar. 2025
#
# SaveTab script (Alt-x):
#       - For the current tab:
#         * we do Tab to space (42046)
#         * we do Trim trailing space (42024)
#         * we save the file (41006)
#         * we reload the file from disk (41014)
#       - This script will determine if the tab was already saved or not
#         * if the file was saved previously, we simply save the file
#         * if the file was not saved previously, we create a .txt text file in a given folder
#           (the text file will receive an incrementing number with 2 digits and we fill up any gaps in the numbering that might happen)
#           (see script SaveAllTabs too)
#       - Initially this script was a Notepad++ macro but it lacked some essential functionality.


# Tab to space
notepad.menuCommand(42046)

# Trim trailing spaces
notepad.menuCommand(42024)

# Save the file or write to disk
full_file_name = notepad.getBufferFilename(notepad.getCurrentBufferID())
do_saveas = True
if os.path.isfile(full_file_name) and os.sep in full_file_name:
    if os.path.exists(full_file_name):
        # Save the file
        notepad.save()
        # or: notepad.menuCommand(41006)
        do_saveas = False

if do_saveas:
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

    new_file_path = os.path.join(SAVE_FOLDER, f"{counter:02}.txt")
    notepad.saveAs(new_file_path)

# Reload from disk
# (to get rid of the green and orange vertical lines in the margin)
notepad.menuCommand(41014)