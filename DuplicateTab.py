from Npp import notepad, editor
import ctypes
import os
import shutil
import tempfile


# Wim Gielis
# Mar. 2025
#
# DuplicateTab script (Alt-t):
#       - Duplicate the current tab as a new tab
#       - The new tab is immediately to the right of the previous tab
#       - The new tab has the same language syntax applied as the previous tab (if any language was applied there)
#       - The new tab is active


def get_cursor_position():
    position = editor.getCurrentPos()
    line = editor.lineFromPosition(position) + 1
    column = editor.getColumn(position)
    return (position, line, column)

def set_cursor_position(position):
    editor.gotoPos(position)

def get_number_of_tabs(view=None):
    retval = 0
    if view is None:
        retval = len(notepad.getFiles())
    else:
        for (pathname, buffer_id, index, v) in notepad.getFiles():
            if v == view: retval += 1
        return retval

def is_current_tab_saved():
    # Get the full path of the current file
    file_path = notepad.getCurrentFilename()

    # If the tab has never been saved (e.g. "new 1"), the filename is empty
    if not file_path or not os.path.isfile(file_path):
        return False

    # If there are unsaved changes in the current document
    if editor.getModify():
        return False

    # File exists and there are no unsaved changes
    return True


# Get the built-in language type (if any)
current_lang_id = notepad.getLangType()

# Get other information about the active tab
current_view = notepad.getCurrentView()
current_tab_index = notepad.getCurrentDocIndex(current_view)
cursor_position_info = get_cursor_position()
cursor_position = cursor_position_info[0]

# Get the User-Defined Language (UDL) name, if applicable
udl_name = notepad.getLanguageName(current_lang_id) if current_lang_id != -1 else notepad.getLangTypeAsString()

# Get the content of the current tab
try:
    current_content = editor.getText()
    stop = 0
except:

    if is_current_tab_saved():

        current_path = notepad.getCurrentFilename()
        file_name = os.path.basename(current_path)

        # Get system temp directory
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file_name)

        # Copy the file to temp
        shutil.copy2(current_path, temp_path)

        # Open the copied file in Notepad++
        notepad.open(temp_path)
    else:
        notepad.messageBox("An error was produced while getting the text of the file. Probably an encoding issue.", "Issue", 0)

    stop = 1

if stop == 0:
    # Create a new document (opens a new tab)
    notepad.new()

    # Insert the copied content into the new tab
    editor.setText(current_content)

    # Set the cursor position
    set_cursor_position(cursor_position)
    editor.charRight()
    editor.charLeft()

    # Apply the language syntax
    if udl_name == 'Normal text':
        # No action needed
        pass
    elif str(current_lang_id) == "USER":
        # User-defined language
        if udl_name:
            # Cut off the first part 'udf - '
            if udl_name[6:]:
                notepad.runMenuCommand('Language', udl_name[6:])
    else:
        # Built-in language
        notepad.runMenuCommand(udl_name[0], udl_name)
        udl_name_2 = notepad.getLanguageName(notepad.getLangType()) if notepad.getLangType() != -1 else notepad.getLangTypeAsString()
        if udl_name_2 != udl_name:
            notepad.menuCommand('Language', udl_name)

    # Position the new tab to the right of the old tab
    positions_to_move = get_number_of_tabs(current_view) - current_tab_index - 2
    if positions_to_move > 0:
        for _ in range(positions_to_move):
            notepad.menuCommand(MENUCOMMAND.VIEW_TAB_MOVEBACKWARD)