from Npp import notepad, editor
import os
import ctypes
import shutil


# Wim Gielis
# Mar. 2025
#
# DeleteTab script (Alt-del):
#       - This script will delete the current tab
#       - It will determine if the tab was already saved or not
#         * if the file was saved previously, we simply delete the file
#         * if the file was not saved previously, we close the tab without changes and without being asked
#       - Initially this script was a Notepad++ macro but it lacked some essential functionality like deleting/closing an unsaved tab.


# Function to move a file to the recycle bin
def move_to_recycle_bin(file_path):
    try:
        # SHFileOperation to move file to Recycle Bin
        ctypes.windll.shell32.SHFileOperationW(0, 3, file_path, None, 0x40 | 0x4, False)
    except Exception as e:
        notepad.messageBox(f"Error moving to Recycle Bin:\n{str(e)}", "Error", 0)


# Get the current file path
# Check if file exists on disk
file_path = notepad.getCurrentFilename()

# Close the current tab
editor.setSavePoint()  # Mark the current state as saved
notepad.menuCommand(41003)

# Delete the file from disk if the tab was already saved
if os.path.isfile(file_path) and os.sep in file_path:
    if os.path.exists(file_path):
        move_to_recycle_bin(file_path)