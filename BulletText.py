from Npp import editor


# Wim Gielis
# Apr. 2025
#
# BulletText script (Alt-b):
#       - The selected text receives a bulleting in front: - and a space
#       - Empty lines also receive them


# If there is no selection, do nothing
# if selected_text.strip():
# if editor.getSelectionEmpty():
    # current_position = editor.getCurrentPos()
    # current_line_number = editor.lineFromPosition(current_position)
    # start_of_curr_line_pos = editor.positionFromLine(current_line_number)
    # editor.setSel(start_of_curr_line_pos, start_of_curr_line_pos + len(editor.getLine(current_line_number)) - 1)

# Get the start and end positions of the current selection
sel_start = editor.getSelectionStart()
sel_end = editor.getSelectionEnd()

# Extend the selection to the start of the first selected line
line_start = editor.lineFromPosition(sel_start)
sel_start = editor.positionFromLine(line_start)

# Extend the selection to the end of the last selected line
line_end = editor.lineFromPosition(sel_end)
sel_end = editor.getLineEndPosition(line_end)

# Set the new selection range
editor.setSelection(sel_end, sel_start)


# Get the selected lines of text
selected_text = editor.getSelText()

# Split into lines and process
lines = selected_text.splitlines()
if lines:
    new_lines = [f'- {line.rstrip()}' for line in lines]
    new_text = '\r\n'.join(new_lines)
    editor.replaceSel(new_text)
    editor.setCurrentPos(sel_start + 2)
    editor.gotoPos(sel_start + 2)