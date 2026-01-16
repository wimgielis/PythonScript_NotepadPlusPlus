from Npp import editor, console
import re


# Wim Gielis
# Jan. 2026
#
# DuplicateAndIncrease script (Alt-<):
#       - Duplicate the currently selected line
#       - With regex identify all numbers
#       - Increase each number with 1 (a number can be single digit but not negative)

# import ctypes

# # Get the state of the left or right Ctrl key
# VK_LCONTROL = 0xA2
# VK_RCONTROL = 0xA3

# # GetAsyncKeyState returns a nonzero value if key is pressed
# ctrl_pressed = ctypes.windll.user32.GetAsyncKeyState(VK_LCONTROL) & 0x8000 or \
               # ctypes.windll.user32.GetAsyncKeyState(VK_RCONTROL) & 0x8000

# if ctrl_pressed:
    # console.write("Ctrl is being held down!")
# else:
    # console.write("Ctrl is NOT pressed.")



# Get the current selection
start_pos = editor.getSelectionStart()
end_pos = editor.getSelectionEnd()

# Determine the line number of the first selected character (or caret if no selection)
line_num = editor.lineFromPosition(start_pos)

# Get the text of that line
line_text = editor.getLine(line_num).rstrip('\r\n')

# Function to increment numbers in a string
def increment_numbers(match):
    return str(int(match.group()) + 1)

# Duplicate the line
editor.beginUndoAction()
try:
    # Insert the original line below
    insert_pos = editor.getLineEndPosition(line_num)
    editor.insertText(insert_pos, '\r\n' + line_text)

    # Update the line number of the duplicate
    duplicate_line_num = line_num + 1
    duplicate_line_start = editor.positionFromLine(duplicate_line_num)
    duplicate_line_end = editor.getLineEndPosition(duplicate_line_num)
    
    # Get duplicate line text
    duplicate_text = editor.getTextRange(duplicate_line_start, duplicate_line_end)

    # Increment all numbers using regex
    incremented_text = re.sub(r'\d+', increment_numbers, duplicate_text)

    # Replace the duplicate line with incremented numbers
    editor.setTargetStart(duplicate_line_start)
    editor.setTargetEnd(duplicate_line_end)
    editor.replaceTarget(incremented_text)

    # Move caret to the first character of the new line
    editor.gotoPos(duplicate_line_start)
finally:
    editor.endUndoAction()