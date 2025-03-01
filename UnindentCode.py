from Npp import notepad, editor

NUMBER_OF_INDENT_SPACES = 4


# Wim Gielis
# Mar. 2025
#
# UnindentCode script (Alt-Shift-i):
#       - The selected text is unindented
#       - We remove 4 spaces from the beginning of every non-empty line


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
        if line.startswith('\t'):
            new_lines.append(line[1:])
        elif line.startswith(' ' * NUMBER_OF_INDENT_SPACES):
            new_lines.append(line[NUMBER_OF_INDENT_SPACES:])
        else:
            new_lines.append(line)

if new_lines:
    # Join the processed lines back together
    new_text = '\r\n'.join(new_lines)

    # Replace the content in the editor
    editor.replaceSel(new_text)