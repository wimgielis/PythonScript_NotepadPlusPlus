from Npp import notepad, editor

NUMBER_OF_INDENT_SPACES = 4


# Wim Gielis
# Mar. 2025
#
# IndentCode script (Alt-i):
#       - The selected text is indented
#       - We add 4 spaces to the beginning of every non-empty line
#       - Empty lines are unaffected so as to not introduce unnecessary whitespace


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
new_lines = []

for line in lines:

    line = line.rstrip()
    if line == '':
        new_lines.append('')
    else:
        new_lines.append(f"{' ' * NUMBER_OF_INDENT_SPACES}{line}")

if new_lines:
    # Join the processed lines back together
    new_text = '\r\n'.join(new_lines)

    # Replace the content in the editor
    editor.replaceSel(new_text)